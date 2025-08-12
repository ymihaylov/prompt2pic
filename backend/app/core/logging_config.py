import logging
import sys
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", None)
        if request_id:
            payload["request_id"] = request_id

        path = getattr(record, "path", None)
        if path:
            payload["path"] = path

        method = getattr(record, "method", None)
        if method:
            payload["method"] = method

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        import json

        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "celery"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(log_level)
        logger.propagate = True
