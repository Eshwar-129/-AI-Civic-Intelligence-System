"""
Notification Tool
-----------------
Handles sending or logging civic issue notifications.
Currently simulates email sending for academic deployment.
"""

import datetime
import os

LOG_FILE = "notification_log.txt"


def send_notification(email: str, subject: str, message: str) -> bool:
    """
    Simulates sending notification to department.

    Returns True if simulated send successful.
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
        f"\n--- NOTIFICATION ---\n"
        f"Time: {timestamp}\n"
        f"To: {email}\n"
        f"Subject: {subject}\n"
        f"Message:\n{message}\n"
        f"-------------------\n"
    )

    # Print to console (demo visibility)
    print(log_entry)

    # Append to log file
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        return True
    except Exception:
        return False