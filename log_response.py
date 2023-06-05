import logging
import time
from logging.handlers import TimedRotatingFileHandler


class LogResponse:

    def __init__(self, path):
        logger = logging.getLogger("Rotating Log")
        _path = path

    def create_rotating_chat_logger(self):
        logger = logging.getLogger("askai log")
        logger.setLevel(logging.INFO)

        handler = TimedRotatingFileHandler(self._path, when="d")
        logger.addHandler(handler)
        return logger

    def print_and_log(self, input_str):
        print(input_str)
        self.logger.info(input_str)
