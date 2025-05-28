def classify_log_line(line: str) -> str:
    line_lower = line.lower()

    if "critical" in line_lower:
        return "CRITICAL"
    elif "error" in line_lower:
        return "ERROR"
    elif "failed" in line_lower:
        return "FAILED"
    elif "warning" in line_lower:
        return "WARNING"
    elif "info" in line_lower:
        return "INFO"
    elif "debug" in line_lower:
        return "DEBUG"
    else:
        return "UNKNOWN"
