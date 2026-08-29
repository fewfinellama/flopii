import re

with open("main.py", "r") as f:
    main_code = f.read()

# Add asyncio import
main_code = main_code.replace("import os", "import os\nimport asyncio\nimport logging")

# Add the background task loop
background_task_code = """
async def autonomous_agent_loop():
    logging.info("Starting autonomous agent loop...")
    while True:
        try:
            status = get_setting("agent_status") or "active"
            if status == "active":
                logging.info("Agent is ACTIVE. Running cycle...")
                # Run the blocking function in a thread to avoid blocking FastAPI
                result = await asyncio.to_thread(run_agent_cycle)
                logging.info(f"Cycle complete. Result: {result.get('status')}")
            else:
                logging.info("Agent is PAUSED. Skipping cycle.")
        except Exception as e:
            logging.error(f"Error in autonomous loop: {e}")
        
        # Sleep for 60 seconds before next check/run
        await asyncio.sleep(60)

@app.on_event("startup")
def startup_event():
    init_db()
    asyncio.create_task(autonomous_agent_loop())
"""

main_code = re.sub(
    r'@app\.on_event\("startup"\)\ndef startup_event\(\):\n    init_db\(\)',
    background_task_code,
    main_code,
)

with open("main.py", "w") as f:
    f.write(main_code)
