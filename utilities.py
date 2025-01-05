import os
import logging
from datetime import datetime


def validate_time(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def validate_script_path(script_path: str) -> bool:
    return os.path.isfile(script_path)


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler("scheduler.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

