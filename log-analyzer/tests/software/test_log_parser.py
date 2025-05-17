# tests/test_log_parser.py
from app.log_parser import parse_log

def test_parse_log():
    log = "INFO: This is a log entry"
    result = parse_log(log)
    assert result == {"level": "INFO", "message": "This is a log entry"}