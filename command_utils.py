# command_utils.py
COMMAND_SET = {
    "start",
    "next",
    "repeat",
    "clarify",
    "grocery",
    "switch_step",
    "switch_all",
}

def normalize_command(text: str) -> str:
    """Normalize free-form speech into a fixed system command."""
    if not text:
        return "unknown"

    text = text.lower().strip()

    if "start" in text or "begin" in text:
        return "start"
    elif "next" in text or "forward" in text:
        return "next"
    elif "repeat" in text or "again" in text:
        return "repeat"
    elif "clarify" in text or "tip" in text or "explain" in text:
        return "clarify"
    elif "step" in text:
        return "switch_step"
    elif "all" in text or "everything" in text:
        return "switch_all"

    return "unknown"
