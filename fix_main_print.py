with open("main.py", "r") as f:
    main_code = f.read()

main_code = main_code.replace(
    'logging.info("Starting autonomous agent loop...")',
    'print("\\n[AUTONOMOUS LOOP] Started. Agent will poll every 60 seconds...\\n")',
)
main_code = main_code.replace(
    'logging.info("Agent is ACTIVE. Running cycle...")',
    'print(f"\\n[AUTONOMOUS LOOP] Agent ACTIVE. Executing workflow cycle at target room...")',
)
main_code = main_code.replace(
    "logging.info(f\"Cycle complete. Result: {result.get('status')}\")",
    "print(f\"[AUTONOMOUS LOOP] Cycle complete. Result: {result.get('status')}\\n\")",
)
main_code = main_code.replace(
    'logging.info("Agent is PAUSED. Skipping cycle.")',
    'print("[AUTONOMOUS LOOP] Agent PAUSED. Skipping execution.", end="\\r")',
)

with open("main.py", "w") as f:
    f.write(main_code)
