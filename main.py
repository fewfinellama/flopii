import uvicorn
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from contextlib import asynccontextmanager
import asyncio
import logging
import json

from core.db import (
    init_db,
    get_setting,
    set_setting,
    get_post_logs,
    get_dashboard_stats,
)
from core.identity import generate_identity, import_identity
from core.agent import run_agent_cycle




# Models for incoming JSON requests
class SettingsPayload(BaseModel):
    llm_config: dict
    target_room: str
    data_endpoints: str
    agent_status: str
    execution_interval: int
    system_prompt: str


class IdentityPayload(BaseModel):
    passphrase: str


async def autonomous_agent_loop():
    print("\n[AUTONOMOUS LOOP] Started.\n")
    while True:
        try:
            status = get_setting("agent_status") or "active"
            interval_str = get_setting("execution_interval")
            interval_min = int(interval_str) if interval_str else 1

            if status == "active":
                print(
                    f"\n[AUTONOMOUS LOOP] Agent ACTIVE. Executing workflow cycle at target room..."
                )
                result = await asyncio.to_thread(run_agent_cycle)
                print(
                    f"[AUTONOMOUS LOOP] Cycle complete. Result: {result.get('status')}\n"
                )
            else:
                pass

        except Exception as e:
            print(f"[AUTONOMOUS LOOP] Error in loop iteration: {e}")

        await asyncio.sleep(interval_min * 60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(autonomous_agent_loop())
    yield
    task.cancel()



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(autonomous_agent_loop())
    yield
    task.cancel()

app = FastAPI(title="Flopii Backend", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"active_page": "home"}
    )


@app.get("/identity", response_class=HTMLResponse)
async def read_identity(request: Request):
    return templates.TemplateResponse(
        request=request, name="identity.html", context={"active_page": "identity"}
    )


@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse(
        request=request, name="settings.html", context={"active_page": "settings"}
    )


@app.get("/logs", response_class=HTMLResponse)
async def read_logs(request: Request):
    return templates.TemplateResponse(
        request=request, name="logs.html", context={"active_page": "logs"}
    )


@app.get("/inbox", response_class=HTMLResponse)
async def read_inbox(request: Request):
    return templates.TemplateResponse(
        request=request, name="inbox.html", context={"active_page": "inbox"}
    )


@app.get("/api/state")
def get_state():
    """Returns the current state for the frontend to render"""
    did = get_setting("agent_did") or ""
    import hashlib

    agent_mailbox = (
        f"/r/p-mb-{hashlib.sha256(did.encode('utf-8')).hexdigest()[:16]}" if did else ""
    )

    return {
        "did": did,
        "agent_mailbox": agent_mailbox,
        "llm_config": json.loads(get_setting("llm_config")) if get_setting("llm_config") else {
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
        },
        "target_room": get_setting("target_room") or "/r/flopii",
        "data_endpoints": get_setting("data_endpoints") or "",
        "agent_status": get_setting("agent_status") or "active",
        "provider_usage": json.loads(get_setting("provider_usage")) if get_setting("provider_usage") else None,
        "execution_interval": int(get_setting("execution_interval") or 1),
        "system_prompt": get_setting("system_prompt")
        or "You are an autonomous AI agent in a zero-trust network...",
        "latest_payload": get_setting("latest_payload") or "",
        "identity_exists": os.path.exists("identity.pem"),
        "mailbox_commands": int(get_setting("mailbox_commands") or 0),
        "stats": get_dashboard_stats(),
        "logs": [
            {
                "timestamp": log[0],
                "target_room": log[1],
                "status": log[2],
                "response": log[3],
                "payload": log[4],
            }
            for log in get_post_logs(10)
        ],
    }


@app.get("/api/inbox")
def get_inbox():
    """Fetches messages from the agent's private mailbox"""
    did = get_setting("agent_did")
    if not did:
        return {"messages": [], "error": "No identity configured."}

    import hashlib
    from core.network import fetch_room

    did_fingerprint = hashlib.sha256(did.encode("utf-8")).hexdigest()[:16]
    mailbox_room = f"/r/p-mb-{did_fingerprint}"

    try:
        messages = fetch_room(mailbox_room)
        # Reverse to show newest first
        return {"messages": messages[::-1]}
    except Exception as e:
        import logging

        logging.error(f"Error fetching inbox: {e}")
        return {"messages": [], "error": str(e)}


@app.post("/api/settings")
def save_settings(payload: SettingsPayload):
    set_setting("llm_config", json.dumps(payload.llm_config))
    set_setting("target_room", payload.target_room)
    set_setting("data_endpoints", payload.data_endpoints)
    set_setting("agent_status", payload.agent_status)
    set_setting("execution_interval", str(payload.execution_interval))
    set_setting("system_prompt", payload.system_prompt)
    return {"status": "success"}

class LLMVerifyPayload(BaseModel):
    provider: str
    api_key: str
    llm_model: str

@app.post("/api/llm/verify")
def verify_llm(payload: LLMVerifyPayload):
    from core.llm import verify_llm_connection
    success, message, usage_stats = verify_llm_connection(payload.provider, payload.api_key, payload.llm_model)
    return {"verified": success, "message": message, "usage": usage_stats}


@app.post("/api/identity")
def create_identity(payload: IdentityPayload):
    try:
        new_did = generate_identity(payload.passphrase)
        set_setting("agent_did", new_did)
        set_setting("agent_passphrase", payload.passphrase)
        return {"status": "success", "did": new_did}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/identity/import")
async def upload_identity(file: UploadFile = File(...), passphrase: str = Form("")):
    try:
        contents = await file.read()
        new_did = import_identity(contents, passphrase)
        set_setting("agent_did", new_did)
        set_setting("agent_passphrase", passphrase)
        return {"status": "success", "did": new_did}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/identity/download")
def download_identity():
    if os.path.exists("identity.pem"):
        return FileResponse(
            "identity.pem", media_type="application/x-pem-file", filename="identity.pem"
        )
    return {"error": "No identity file found."}


@app.post("/api/run")
def force_run():
    result = run_agent_cycle()
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8502, reload=True)


class ManualPostPayload(BaseModel):
    room: str
    message: str


@app.post("/api/post")
def manual_post(payload: ManualPostPayload):
    """Post a manually written message to a Technocore room."""
    from core.network import post_to_technocore
    from core.db import log_post
    import json

    did = get_setting("agent_did")
    if not did:
        return {
            "status": "error",
            "message": "No identity configured. Generate or import one first.",
        }

    if not payload.message.strip():
        return {"status": "error", "message": "Message cannot be empty."}

    room = payload.room.strip() or get_setting("target_room") or "/r/flopii"

    try:
        with open("identity.pem", "rb") as f:
            pem_bytes = f.read()
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "identity.pem not found. Generate or import an identity first.",
        }

    passphrase = get_setting("agent_passphrase") or ""
    success, response_data = post_to_technocore(
        did, room, payload.message, pem_bytes, passphrase
    )

    status = "Success" if success else "Failed"
    log_post(room, payload.message, status, json.dumps(response_data))

    if success:
        return {"status": "success", "message": f"Posted to {room}"}
    else:
        return {
            "status": "error",
            "message": f"Technocore rejected the post: {response_data}",
        }
