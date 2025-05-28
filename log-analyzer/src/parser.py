def read_log_file(filepath):
    """
    Read log file and return list of lines.
    Handles file not found and other errors gracefully.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Log file not found: {filepath}")
        raise
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.readlines()
        except Exception as e:
            print(f"Error reading file with latin-1 encoding: {e}")
            raise
    except Exception as e:
        print(f"Unexpected error reading {filepath}: {e}")
        raise