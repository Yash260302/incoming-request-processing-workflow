import logging
from pathlib import Path

from app.utils.config import Config


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

        log_file = Config.LOGS_DIR / "application.log"

        logger = logging.getLogger("IncomingRequestWorkflow")

        logger.setLevel(logging.INFO)

        logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        cls._logger = logger

        return logger