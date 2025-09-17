import datetime

"""Utility functions for the cooking assistant application."""
def log_event(event: str, log_file="cooking_log.txt"):
    """Log cooking events with timestamps to a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {event}\n")
    print(f"Logged event: {event}")