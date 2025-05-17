import json
import os
from classifier import classify_log_line
from parser import read_log_file

# Folosim calea absolută în container
log_path = "/app/logs/log.txt"
output_path = "/app/output/output.json"

# Creăm directorul output dacă nu există
os.makedirs(os.path.dirname(output_path), exist_ok=True)

log_lines = read_log_file(log_path)

failed_messages = []

for line in log_lines:
    log_type = classify_log_line(line)
    if log_type.lower() == "failed":
        failed_messages.append(line.strip())

# Pregătim structura dict pentru output
results = {
    "failed_entries": failed_messages,
    "count": len(failed_messages)
}

with open(output_path, 'w') as f:
    json.dump(results, f, indent=4)

print(f"Log classification complete. Output saved in {output_path}")
