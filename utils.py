# import datetime

# """Utility functions for the cooking assistant application."""
# def log_event(event: str, log_file="cooking_log.txt"):
#     """Log cooking events with timestamps to a log file."""
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(log_file, 'a') as f:
#         f.write(f"[{timestamp}] {event}\n")
#     print(f"Logged event: {event}")

# def load_config(path="config.json"):
#     """Load configuration settings from a JSON file."""
#     import json
#     try:
#         with open(path, 'r') as f:
#             config = json.load(f)
#         return config
#     except Exception as e:
#         print(f"Failed to load config: {e}")
#         return {
#             "wake_word": "hey chef",
#             "voice": "alloy",
#             "command_timeout": 10,
#             "mode": "hybrid",
#         }

# Version 2:
# import json
# import datetime
# import os


# def log_event(event: str, log_file="cooking_log.txt"):
#     """Log events to console + file with timestamps."""
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(log_file, "a") as f:
#         f.write(f"[{timestamp}] {event}\n")
#     print("LOG:", event)


# def load_config(path="config.json"):
#     """
#     Load configuration from JSON file.
#     Adds safety checks for OpenAI API key if GPT mode is selected.
#     """
#     default_config = {
#         "wake_word": "hey chef",
#         "voice": "alloy",
#         "command_timeout": 10,
#         "mode": "hybrid",
#         "openai_api_key": None,
#     }

#     try:
#         with open(path, "r") as f:
#             config = json.load(f)
#     except Exception as e:
#         print("⚠️ Error loading config.json, using defaults:", e)
#         return default_config

#     # Merge defaults with loaded config (in case keys are missing)
#     for key, value in default_config.items():
#         config.setdefault(key, value)

#     # API key handling
#     api_key = config.get("openai_api_key") or os.getenv("OPENAI_API_KEY")

#     if config["mode"].lower() in ["gpt", "hybrid"] and not api_key:
#         print(
#             "⚠️ WARNING: GPT mode selected but no OpenAI API key found in config.json or environment!"
#         )
#         print(
#             "   → You can add 'openai_api_key' to config.json or set OPENAI_API_KEY in your system environment."
#         )

#     # Ensure we store the resolved key
#     config["openai_api_key"] = api_key
#     return config

# Version 3:
import json
import datetime
import os


def log_event(event: str, log_file="cooking_log.txt"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{ts}] {event}\n")
    print("LOG:", event)


def load_config(path="config.json"):
    """Load configuration and resolve OPENAI_API_KEY from env if absent."""
    default = {
        "wake_word": "hey chef",
        "voice": "alloy",
        "command_timeout": 10,
        "mode": "gpt",
        "stt_model": "whisper-1",
        "mic_duration": 5,
        "openai_api_key": None,
    }
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except Exception as e:
        print("⚠️ Could not read config.json, using defaults:", e)
        cfg = {}

    # merge defaults
    for k, v in default.items():
        cfg.setdefault(k, v)

    # resolve key from env if not present
    cfg["openai_api_key"] = cfg.get("openai_api_key") or os.getenv("OPENAI_API_KEY")

    if cfg["mode"].lower() in ["gpt", "hybrid"] and not cfg["openai_api_key"]:
        print(
            "⚠️ GPT mode but no API key found. Set OPENAI_API_KEY or add openai_api_key in config.json."
        )
    return cfg
