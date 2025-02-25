import logging
from logging.config import dictConfig
from typing import Dict, Any

def setup_logging() -> None:
    """Configure logging settings"""
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "formatter": "default",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": "DEBUG",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    }
    dictConfig(logging_config)

logger = logging.getLogger(__name__)