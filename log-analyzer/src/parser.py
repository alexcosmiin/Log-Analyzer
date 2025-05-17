def read_log_file(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()