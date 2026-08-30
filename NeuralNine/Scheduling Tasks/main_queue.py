import time
import threading
import schedule
import queue


# ============================================================
# JOBS
# ============================================================

def download_file():
    """Simulate downloading a file."""
    print("Downloading file...")
    time.sleep(2)
    print("File downloaded!")


def send_email():
    """Simulate sending an email."""
    print("Sending email...")
    time.sleep(1)
    print("Email sent!")


def process_data():
    """Simulate processing data."""
    print("Processing data...")
    time.sleep(3)
    print("Data processed!")


# ============================================================
# JOB QUEUE
# ============================================================

# The queue stores functions that need to be executed.
job_queue = queue.Queue()


# Add some jobs to the queue immediately.
job_queue.put(download_file)
job_queue.put(send_email)
job_queue.put(process_data)


# ============================================================
# STOP EVENT
# ============================================================

# This event tells the worker when it should stop.
stop_event = threading.Event()


# ============================================================
# WORKER
# ============================================================

def worker_main():
    """
    Continuously take jobs from the queue and execute them.

    The worker waits for new jobs instead of constantly checking
    whether the queue is empty.
    """

    while not stop_event.is_set():

        try:
            # Wait for a job for a maximum of one second.
            #
            # The timeout allows the worker to periodically
            # check whether stop_event has been triggered.
            job_func = job_queue.get(timeout=1)

        except queue.Empty:
            # No job is currently available.
            continue

        try:
            print(f"\nStarting: {job_func.__name__}")

            # Execute the job.
            job_func()

            print(f"Finished: {job_func.__name__}")

        except Exception as error:
            # Prevent one failed job from stopping the worker.
            print(f"Error while running {job_func.__name__}: {error}")

        finally:
            # Tell the queue that this job has been processed.
            job_queue.task_done()


# ============================================================
# SCHEDULE
# ============================================================

# Add jobs to the queue at specific intervals.

# Every 10 seconds, add download_file to the queue.
schedule.every(10).seconds.do(job_queue.put, download_file)

# Every 30 seconds, add send_email to the queue.
schedule.every(30).seconds.do(job_queue.put, send_email)

# Every hour, add process_data to the queue.
schedule.every(1).hours.do(job_queue.put, process_data)


# ============================================================
# START WORKER
# ============================================================

# Create one worker thread responsible for processing
# jobs from the queue.
worker_thread = threading.Thread(
    target=worker_main,
    daemon=True
)

worker_thread.start()


# ============================================================
# MAIN LOOP
# ============================================================

try:
    print("Scheduler is running...")
    print("Press Ctrl+C to stop the program.\n")

    while True:

        # Check whether a scheduled job needs to be added
        # to the queue.
        schedule.run_pending()

        # Wait one second before checking again.
        time.sleep(1)


except KeyboardInterrupt:
    # Ctrl+C triggers KeyboardInterrupt.
    print("\nStopping scheduler...")

    # --------------------------------------------------------
    # 1. Cancel all future scheduled jobs
    # --------------------------------------------------------

    schedule.clear()
    print("Scheduled jobs cancelled.")

    # --------------------------------------------------------
    # 2. Stop the worker
    # --------------------------------------------------------

    stop_event.set()

    # --------------------------------------------------------
    # 3. Wait for the current worker task to finish
    # --------------------------------------------------------

    worker_thread.join()

    print("Worker stopped.")
    print("Program stopped.")