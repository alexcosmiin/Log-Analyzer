def classify_log_line(line: str) -> str:
    line_lower = line.lower()

    if "failed" in line_lower:
        return "FAILED"
    elif "[error]" in line_lower:
        return "ERROR"
    elif "[warning]" in line_lower:
        return "WARNING"
    elif "[info]" in line_lower:
        return "INFO"
    else:
        return "UNKNOWN"
