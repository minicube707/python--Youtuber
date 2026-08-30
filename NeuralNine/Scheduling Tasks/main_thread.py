import threading
import time
import schedule


def job():
    """The task that will run in a separate thread."""
    print(f"I'm running on thread {threading.current_thread().name}")


def run_threaded(job_func):
    """
    Run a job in a separate thread.

    daemon=True means the thread will not prevent the program
    from shutting down when the main thread exits.
    """
    job_thread = threading.Thread(
        target=job_func,
        daemon=True
    )
    job_thread.start()


# Schedule the same job multiple times.
for _ in range(5):
    schedule.every(10).seconds.do(run_threaded, job)


try:
    print("Scheduler is running...")
    print("Press Ctrl+C to stop the program.\n")

    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    # Ctrl+C triggers KeyboardInterrupt.
    print("\nStopping scheduler...")

    # Cancel all scheduled jobs.
    schedule.clear()

    print("All scheduled jobs have been cancelled.")
    print("Program stopped.")
