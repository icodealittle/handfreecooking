import datetime

"""Utility functions for the cooking assistant application."""
def log_event(event: str, log_file="cooking_log.txt"):
    """Log cooking events with timestamps to a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {event}\n")
    print(f"Logged event: {event}")

def load_config(path="config.json"):
    """Load configuration settings from a JSON file."""
    import json
    try:
        with open(path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Failed to load config: {e}")
        return {
            "wake_word": "hey chef",
            "voice": "alloy",
            "command_timeout": 10,
            "mode": "hybrid",
        }
