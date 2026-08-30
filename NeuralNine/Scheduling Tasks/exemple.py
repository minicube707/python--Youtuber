import schedule
import time as tm


def break_reminder():
    """Remind the user to take a break."""
    print("Take a break! You have been working for 30 minutes!")


# Run the reminder every 30 minutes.
schedule.every(30).minutes.do(break_reminder)

# Also run the reminder every day at 10:00 AM.
schedule.every().day.at("10:00").do(break_reminder)


# Keep the scheduler running.
while True:
    schedule.run_pending()
    tm.sleep(1)