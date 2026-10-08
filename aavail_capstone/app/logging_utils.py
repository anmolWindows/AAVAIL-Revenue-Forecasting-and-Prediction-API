import json
import logging
from pathlib import Path

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        return json.dumps(payload)

def get_logger(name="aavail", log_path="logs/api.log"):
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_path)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger
