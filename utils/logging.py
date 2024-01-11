""" Модуль логгера. Записывает лог с ошибками в ./logs/err.log."""
import logging.config
import os
import sys

DIR_LOGS = "logs"

if not os.path.exists(DIR_LOGS):
    os.makedirs(DIR_LOGS)

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "{level: %(levelname)s | "
            "logger: %(name)s | "
            "time: %(asctime)s | "
            "line №: %(lineno)s | "
            "message: %(message)s}"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": sys.stdout,
        },
        "file_info_utils": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"./{DIR_LOGS}/info.log",
            "when": "H",
            "interval": 10,
            "backupCount": 1,
            "level": "DEBUG",
            "encoding": "utf8",
            "formatter": "base",
        },
        "file_errors_utils": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"./{DIR_LOGS}/err.log",
            "when": "H",
            "interval": 10,
            "backupCount": 1,
            "level": "ERROR",
            "encoding": "utf8",
            "formatter": "base",
        },
    },
    "loggers": {
        "logger_main": {"level": "DEBUG", "handlers": ["console", "file_info_utils"]},
        "logger_loader": {"level": "DEBUG", "handlers": ["console", "file_info_utils"]},
        "logger_middleware": {
            "level": "DEBUG",
            "handlers": ["console", "file_info_utils"],
        },
    },
}

logging.config.dictConfig(dict_config)

logger_root = logging.getLogger("")
logger_root.setLevel(logging.DEBUG)
