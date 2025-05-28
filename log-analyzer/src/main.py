import json
import os
import argparse
from datetime import datetime
from .classifier import classify_log_line
from .parser import read_log_file


def main():
    parser = argparse.ArgumentParser(description="Analyze log files.")
    parser.add_argument(
        "--log-file",
        default="/app/logs/log.txt",
        help="Path to the log file."
    )
    parser.add_argument(
        "--output-file",
        default="/app/output/output.json",
        help="Path to the output JSON file."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose mode for detailed output."
    )
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled.")
        print(f"Using log file: {args.log_file}")
        print(f"Using output file: {args.output_file}")

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Read log file
    log_lines = []
    try:
        if not os.path.exists(args.log_file):
            print(f"ERROR: Log file not found at {args.log_file}")
            return 1

        log_lines = read_log_file(args.log_file)
        if args.verbose:
            print(f"Successfully read {len(log_lines)} lines from {args.log_file}")

    except Exception as e:
        print(f"ERROR: Failed to read log file: {e}")
        return 1

    # Process log lines
    logs_by_type = {}
    for line in log_lines:
        log_type = classify_log_line(line).upper()
        logs_by_type.setdefault(log_type, []).append(line.strip())

    # Create results dictionary
    results = {}
    for log_type, messages in logs_by_type.items():
        results[log_type] = {
            "count": len(messages),
            "messages": messages
        }

    # Add metadata
    results["metadata"] = {
        "total_lines_processed": len(log_lines),
        "log_file_path": args.log_file,
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Write results to output file
    try:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
        if args.verbose:
            print(f"Log classification complete. Output saved in {args.output_file}")

    except Exception as e:
        print(f"Error writing output file: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())