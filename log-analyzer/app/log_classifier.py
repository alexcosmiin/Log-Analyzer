def classify_log(log_entry):
    """
    Classify a log entry based on its level.

    Args:
        log_entry (dict): Dictionary containing log level and message

    Returns:
        str: Classification of the log
    """
    level = log_entry.get("level", "").upper()

    if level == "INFO":
        return "Informational"
    elif level == "WARNING":
        return "Warning"
    elif level == "ERROR":
        return "Error"
    else:
        return "Unknown"

