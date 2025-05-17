def parse_log(log_line):
    """
    Parse a log line into a dictionary with level and message.

    Example:
    "INFO: This is a log entry" -> {"level": "INFO", "message": "This is a log entry"}
    """
    if ":" in log_line:
        parts = log_line.split(":", 1)
        level = parts[0].strip()
        message = parts[1].strip() if len(parts) > 1 else ""
        return {"level": level, "message": message}
    else:
        return {"level": "UNKNOWN", "message": log_line.strip()}