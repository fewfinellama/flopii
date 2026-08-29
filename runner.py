import time
import logging
import schedule
from core.db import get_setting
from core.agent import run_agent_cycle

# Setup basic logging to terminal
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def job():
    """Scheduled task that runs the agent cycle if it is active."""
    status = get_setting("agent_status")
    if status == "paused":
        logging.info("Agent is paused in the UI. Skipping cycle.")
        return

    logging.info("Triggering scheduled agent cycle...")

    # In a real environment, you might securely retrieve the passphrase from an environment variable
    # or secure key store if the PEM is encrypted.
    result = run_agent_cycle()

    if result["status"] == "success":
        logging.info(
            f"Cycle completed successfully! Payload snippet:\n{result['payload'][:100]}..."
        )
    else:
        logging.error(f"Cycle encountered an error: {result['message']}")


def main():
    logging.info("Starting Flopii Headless Runner...")

    # Run every 30 minutes as recommended in the design document
    schedule.every(30).minutes.do(job)

    # Trigger one run immediately upon starting the script
    job()

    logging.info("Runner is now listening for scheduled jobs (Ctrl+C to exit)...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
