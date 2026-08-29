import requests
import logging
import json
from typing import List
from core.db import get_setting
from core.llm import generate_with_failover
from core.network import sign_message, post_to_technocore, fetch_room
from datetime import datetime
import hashlib


def fetch_endpoints(urls_str: str) -> str:
    """Fetches raw data from a list of URLs and aggregates it into a single context string."""
    urls = [url.strip() for url in urls_str.split("\n") if url.strip()]
    if not urls:
        return ""

    aggregated_data = ""
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            # Try to format as JSON if possible, otherwise use raw text
            try:
                data = response.json()
                text_content = json.dumps(data, indent=2)
            except json.JSONDecodeError:
                text_content = response.text

            # Truncate extremely long responses to save LLM context
            if len(text_content) > 2000:
                text_content = text_content[:2000] + "\n...[TRUNCATED]"

            aggregated_data += f"--- Data from {url} ---\n{text_content}\n\n"

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from {url}: {e}")
            aggregated_data += f"--- Data from {url} ---\n[ERROR FETCHING: {e}]\n\n"

    return aggregated_data


def run_agent_cycle() -> dict:
    """Runs the full agent cycle: Fetch -> Generate Payload -> Sign -> Post."""
    logging.info("Starting agent cycle...")

    from core.db import log_post, set_setting

    target_room = get_setting("target_room") or "/r/flopii"

    try:
        # 1. Read Config
        did = get_setting("agent_did")
        if not did:
            err = "No identity configured. Generate or import one in Identity tab."
            log_post(
                target_room, "Execution aborted.", "Failed", f'{{"error": "{err}"}}'
            )
            return {"status": "error", "message": err}

        data_endpoints = get_setting("data_endpoints") or ""
        llm_config_str = get_setting("llm_config")
        if llm_config_str:
            llm_config = json.loads(llm_config_str)
        else:
            # Fallback to legacy config
            llm_config = {
                "primary": "legacy",
                "auto_failover": False,
                "providers": [{
                    "id": "legacy",
                    "name": get_setting("llm_provider") or "OpenAI",
                    "model": get_setting("llm_model") or "",
                    "api_key": get_setting("api_key") or "",
                    "verified": True,
                    "failures": 0
                }]
            }
        
        passphrase = get_setting("agent_passphrase") or ""
        system_prompt = (
            get_setting("system_prompt") or "You are an autonomous AI agent."
        )

        # 1.5 Mailbox Check
        did_fingerprint = hashlib.sha256(did.encode("utf-8")).hexdigest()[:16]
        mailbox_room = f"/r/p-mb-{did_fingerprint}"
        logging.info(f"Checking agent mailbox: {mailbox_room}")

        inbox_messages = []
        try:
            inbox_messages = fetch_room(mailbox_room)
        except Exception as e:
            logging.error(f"Failed to check mailbox: {e}")

        mailbox_context = ""
        if inbox_messages:
            current_count = int(get_setting("mailbox_commands") or 0)
            set_setting("mailbox_commands", str(current_count + len(inbox_messages)))
            logging.info(f"Mailbox contains {len(inbox_messages)} messages.")

            latest_msg = inbox_messages[-1]
            if isinstance(latest_msg, dict) and "text" in latest_msg:
                logging.info(f"Latest mailbox message: {latest_msg['text']}")
                mailbox_context = (
                    f"\n\n--- INSTRUCTION FROM MAILBOX ---\n{latest_msg['text']}\n"
                )

        # 2. Fetch Data
        context_data = ""
        if data_endpoints:
            context_data = fetch_endpoints(data_endpoints)

        # Append mailbox instructions to the context so the LLM can act on them
        context_data += mailbox_context

        # 3. Generate Payload
        def update_llm_config_cb(new_config):
            set_setting("llm_config", json.dumps(new_config))
            
        payload = generate_with_failover(llm_config, context_data, system_prompt, db_update_callback=update_llm_config_cb)

        # Fallback if LLM fails
        if not payload or payload.startswith("Error"):
            err = payload if payload else "LLM returned empty payload."
            log_post(
                target_room, "Execution aborted.", "Failed", f'{{"error": "{err}"}}'
            )
            return {"status": "error", "message": err}

        # Save the latest payload
        set_setting("latest_payload", payload)

        # 4. Sign and Post
        try:
            with open("identity.pem", "rb") as f:
                pem_bytes = f.read()
        except FileNotFoundError:
            err = "identity.pem file missing from disk."
            log_post(target_room, payload, "Failed", f'{{"error": "{err}"}}')
            return {"status": "error", "message": err}

        success, response_data = post_to_technocore(
            did, target_room, payload, pem_bytes, passphrase
        )

        status = "Success" if success else "Failed"
        log_post(target_room, payload, status, json.dumps(response_data))

        if success:
            return {
                "status": "success",
                "message": "Successfully posted to Technocore!",
                "payload": payload,
                "network_response": response_data,
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to post to Technocore API. Response: {response_data}",
            }

    except Exception as e:
        logging.error(f"Error during agent cycle: {e}")
        from core.db import log_post

        log_post(
            target_room,
            "Execution aborted due to internal error.",
            "Failed",
            f'{{"error": "{str(e)}"}}',
        )
        return {"status": "error", "message": f"Internal error: {e}"}
