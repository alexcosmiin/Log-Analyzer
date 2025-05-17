import os
import subprocess
import json

test_logs = {}

def test_log(message):
    from inspect import currentframe, getframeinfo
    import threading

    frame = currentframe().f_back
    test_name = f"{getframeinfo(frame).filename}:{frame.f_lineno}"

    thread_id = threading.get_ident()
    if thread_id not in test_logs:
        test_logs[thread_id] = []
    test_logs[thread_id].append(message)

    print(f"    → {message}")


def create_test_log(lines=None):
    """Creează fișierul logs/log.txt cu conținut personalizat."""
    os.makedirs("logs", exist_ok=True)
    with open("logs/log.txt", "w") as f:
        f.writelines((line + "\n") for line in (lines or [
            "Login failed for user John",
            "Payment succeeded",
            "Something else failed"
        ]))

def run_analysis_script():
    """Rulează scriptul de analiză."""
    return subprocess.run(["bash", "start_script.sh"], capture_output=True, text=True)

def load_output_json():
    """Încarcă fișierul de output în format JSON."""
    with open("output/output.json", "r") as f:
        return json.load(f)

def file_exists(path):
    """Verifică dacă un fișier există."""
    return os.path.exists(path)
