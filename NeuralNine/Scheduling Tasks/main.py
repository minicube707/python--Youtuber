import schedule
import time as tm
from datetime import time, timedelta

# Python Schedule Library - Examples

# The `schedule` package provides a simple way to run Python functions
# at specific intervals or at specific times.

# Install:
#     pip install schedule
#     uv add schedule

# Documentation:
#     https://schedule.readthedocs.io/


# ============================================================
# 1. BASIC JOB
# ============================================================

def job():
    """Simple function that will be executed by the scheduler."""
    print("Subscribe to NeuralNine!")


# Run `job()` every 5 seconds
# schedule.every(5).seconds.do(job)

# Run `job()` every second
# schedule.every().second.do(job)

# Run `job()` every 10 minutes
# schedule.every(10).minutes.do(job)

# Run `job()` every hour
# schedule.every().hour.do(job)

# Run `job()` every day at 10:30
# schedule.every().day.at("10:30").do(job)

# Run `job()` every Monday
# schedule.every().monday.do(job)

# Run `job()` every Wednesday at 13:15
# schedule.every().wednesday.at("13:15").do(job)

# Run `job()` every day at 12:42 in the Amsterdam timezone
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)

# Run every minute at the 17th second
# Example: 10:00:17, 10:01:17, 10:02:17...
# schedule.every().minute.at(":17").do(job)


# ============================================================
# 2. PASSING ARGUMENTS TO A JOB
# ============================================================

def job_with_message(message):
    """Print a custom message."""
    print(message)


# Pass an argument to the scheduled function
# schedule.every(5).seconds.do(job_with_message, "Hello World!")


# ============================================================
# 3. RANDOM INTERVAL
# ============================================================

# Run the job at a random interval between 1 and 5 seconds.
#
# For example:
#   after 2 seconds
#   then after 5 seconds
#   then after 1 second
#   etc.
#
# schedule.every(1).to(5).seconds.do(job)


# ============================================================
# 4. RUN A JOB UNTIL A SPECIFIC TIME
# ============================================================

# Run the job every hour until 11:33:42
#
# schedule.every().hour.until(time(11, 33, 42)).do(job)

# Run the job every hour for the next 8 hours
#
# schedule.every().hour.until(timedelta(hours=8)).do(job)


# ============================================================
# 5. MULTIPLE SCHEDULES
# ============================================================

def remind_to_sleep(message):
    """Display a reminder message."""
    print(f"Remind me to go to sleep at {message}")


# The same function can have multiple schedules.
#
# schedule.every(5).seconds.do(remind_to_sleep, "8:00 pm")
# schedule.every(2).seconds.do(remind_to_sleep, "9:30 pm")
#
# This is generally clearer than using decorators when learning
# how the schedule package works.


# ============================================================
# 6. DECORATORS
# ============================================================

# The `schedule` package also provides decorators.
#
# Example:
#
# @schedule.repeat(schedule.every(5).seconds)
# def decorated_job():
#     print("This job runs every 5 seconds.")
#
# The decorator is useful when you want to associate the schedule
# directly with the function.


# ============================================================
# 7. KEEP THE PROGRAM RUNNING
# ============================================================

def run_scheduler():
    """
    Continuously check for scheduled jobs.

    `schedule.run_pending()` executes all jobs whose scheduled
    execution time has arrived.

    We sleep for one second between checks to avoid continuously
    using CPU resources.
    """
    while True:
        schedule.run_pending()
        tm.sleep(1)


# ============================================================
# 8. CANCEL A SPECIFIC JOB
# ============================================================

def cancel_example():
    """
    Schedule a job and cancel it after 10 seconds.
    """

    # Schedule the job every 5 seconds.
    job_reference = schedule.every(5).seconds.do(job)

    start_time = tm.time()

    while True:
        schedule.run_pending()
        tm.sleep(1)

        # Cancel the job after 10 seconds.
        if tm.time() - start_time >= 10:
            schedule.cancel_job(job_reference)
            print("Job cancelled.")
            break


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Choose ONE example to run.
    # --------------------------------------------------------

    # Example 1: Run a job every 5 seconds forever
    schedule.every(5).seconds.do(job)
    run_scheduler()

    # Example 2: Cancel a job after 10 seconds
    # cancel_example()