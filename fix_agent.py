import re

with open("core/agent.py", "r") as f:
    agent_code = f.read()

new_agent_cycle = """
def run_agent_cycle() -> dict:
    \"\"\"Runs the full agent cycle: Fetch -> Summarize -> Sign -> Post.\"\"\"
    logging.info("Starting agent cycle...")
    
    from core.db import log_post, set_setting
    target_room = get_setting("target_room") or "/r/flopii"
    
    try:
        # 1. Read Config
        did = get_setting("agent_did")
        if not did:
            err = "No identity configured. Generate or import one in Identity tab."
            log_post(target_room, "Execution aborted.", "Failed", f'{{"error": "{err}"}}')
            return {"status": "error", "message": err}
            
        tickers = get_setting("crypto_tickers") or "BTC,ETH,SOL"
        rss = get_setting("rss_feeds") or "https://cryptopanic.com/news/rss/"
        llm_provider = get_setting("llm_provider") or "OpenAI"
        api_key = get_setting("api_key")
        passphrase = get_setting("agent_passphrase") or ""
        
        # 2. Fetch Data
        prices = fetch_crypto_prices(tickers)
        news = fetch_rss_news(rss)
        
        # 3. Generate Summary
        summary = generate_summary(llm_provider, api_key, news)
        
        # 4. Construct Payload
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        payload = f"FLOPII PULSE | {now}\\n"
        for p in prices:
            sign = "+" if p['change_24h'] >= 0 else ""
            payload += f"{p['ticker']} ${p['price']:,.2f} ({sign}{p['change_24h']:.2f}%)\\n"
        payload += f"\\nNEWS:\\n{summary}"
        
        # Save the latest payload
        set_setting("latest_payload", payload)
        
        # 5. Sign and Post
        try:
            with open("identity.pem", "rb") as f:
                pem_bytes = f.read()
        except FileNotFoundError:
            err = "identity.pem file missing from disk."
            log_post(target_room, payload, "Failed", f'{{"error": "{err}"}}')
            return {"status": "error", "message": err}
            
        success, response_data = post_to_technocore(did, target_room, payload, pem_bytes, passphrase)
        
        import json
        status = "Success" if success else "Failed"
        log_post(target_room, payload, status, json.dumps(response_data))
        
        if success:
            return {"status": "success", "message": "Successfully posted to Technocore!", "payload": payload, "network_response": response_data}
        else:
            return {"status": "error", "message": f"Failed to post to Technocore API. Response: {response_data}"}
            
    except Exception as e:
        logging.error(f"Error during agent cycle: {e}")
        log_post(target_room, "Execution aborted due to internal error.", "Failed", f'{{"error": "{str(e)}"}}')
        return {"status": "error", "message": f"Internal error: {e}"}
"""

agent_code = re.sub(
    r"def run_agent_cycle\(\) -> dict:.*", new_agent_cycle, agent_code, flags=re.DOTALL
)

with open("core/agent.py", "w") as f:
    f.write(agent_code)
