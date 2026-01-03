import json
import logging
from datetime import datetime, timezone

def get_logger(name: str, log_file: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_event(logger, event: dict):
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    logger.info(json.dumps(event, ensure_ascii=False))
