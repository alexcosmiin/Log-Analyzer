# tests/test_log_classifier.py
from app.log_classifier import classify_log

def test_classify_log():
    log = {"level": "INFO", "message": "This is a log entry"}
    result = classify_log(log)
    assert result == "Informational"