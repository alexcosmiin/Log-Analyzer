import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any


class TestLogger:
    """Advanced test logger with multiple handlers and structured logging"""

    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self._configure_logging()

    def _configure_logging(self):
        """Set up logging handlers and formatters"""
        self.log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"test_run_{timestamp}.log"

        self.logger = logging.getLogger("TestFramework")
        self.logger.setLevel(self.log_level)

        # Clear existing handlers
        self.logger.handlers = []

        # File handler (rotating logs)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(self._get_file_formatter())

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._get_console_formatter())

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _get_file_formatter(self):
        """Formatter for file output (more detailed)"""
        return logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def _get_console_formatter(self):
        """Colorized formatter for console output"""
        try:
            from colorlog import ColoredFormatter
            return ColoredFormatter(
                "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
                datefmt=None,
                reset=True,
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
        except ImportError:
            return logging.Formatter('%(levelname)-8s %(message)s')

    def log_test_start(self, test_name: str, test_metadata: Dict[str, Any] = None):
        """Log test start event"""
        self.logger.info(f"TEST START: {test_name}")
        if test_metadata and self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Test metadata: {json.dumps(test_metadata, indent=2)}")

    def log_test_end(self, test_name: str, status: str, duration: float):
        """Log test end event"""
        self.logger.info(f"TEST {status.upper()}: {test_name} (Duration: {duration:.3f}s)")

    def log_step(self, step_name: str, status: str, duration: float = None):
        """Log test step execution"""
        message = f"STEP {status.upper()}: {step_name}"
        if duration is not None:
            message += f" ({duration:.3f}s)"

        if status.lower() == 'failed':
            self.logger.error(message)
        elif status.lower() == 'warning':
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def log_metric(self, name: str, value: Any, unit: str = None):
        """Log performance metric"""
        unit_str = f" {unit}" if unit else ""
        self.logger.info(f"METRIC: {name} = {value}{unit_str}")

    def log_debug_data(self, context: str, data: Any):
        """Log debug information with context"""
        self.logger.debug(f"DEBUG [{context}]: {str(data)}")

    def log_error(self, message: str, exc_info=None):
        """Log error with optional exception info"""
        self.logger.error(message, exc_info=exc_info)

    def capture_system_info(self):
        """Log system information"""
        import platform
        import psutil

        system_info = {
            "system": platform.system(),
            "release": platform.release(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "cpu_cores": psutil.cpu_count(),
            "memory_gb": psutil.virtual_memory().total / (1024 ** 3)
        }

        self.logger.info("SYSTEM INFO:\n" + json.dumps(system_info, indent=2))

    def get_log_file_path(self) -> Path:
        """Get path to current log file"""
        for handler in self.logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                return Path(handler.baseFilename)
        return None