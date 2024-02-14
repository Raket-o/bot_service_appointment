""" Модуль логгера. Записывает лог с ошибками в ./logs/err.log."""
import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler


DIR_LOGS = "logs"

if not os.path.exists(DIR_LOGS):
    os.makedirs(DIR_LOGS)

log_file_handler = TimedRotatingFileHandler(
    filename=f'./{DIR_LOGS}/loging.log',
    when='H',
    interval=10,
    backupCount=3
)
stream_handler = logging.StreamHandler(stream=sys.stdout)

logging.basicConfig(
    format=(
        'level: %(levelname)s | '
        'logger: %(name)s | '
        'time: %(asctime)s | '
        'line №: %(lineno)s | '
        'message: %(message)s'
    ),
    level=logging.INFO,
    handlers=[
        stream_handler,
        log_file_handler
    ]
)
