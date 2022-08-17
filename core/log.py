import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

import coloredlogs

from core import settings

# ---------------------------------------------------------------------------
#   Global Variables
# ---------------------------------------------------------------------------

LEVEL: int = logging.INFO

if settings.DEBUG:
    LEVEL: int = logging.DEBUG

# ---------------------------------------------------------------------------
#   Prepare folders
# ---------------------------------------------------------------------------

if not os.path.exists("logs"):
    os.mkdir("logs")
    print("Folder logs created.")

if not os.path.exists("logs/bot"):
    os.mkdir("logs/bot")
    print("Folder logs/bot created.")

if not os.path.exists("logs/pyrogram"):
    os.mkdir("logs/pyrogram")
    print("Folder logs/pyrogram created.")


# ---------------------------------------------------------------------------
#   Initialize handlers
# ---------------------------------------------------------------------------


class Handlers:
    read_format: str = (
        "%(asctime)s %(name)s[%(process)d:%(thread)d] %(levelname)s %(message)s"
    )

    basic_formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    if not settings.DEBUG:
        # 設定預設 logging 等級
        main_handler_formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s[%(process)d:%(thread)d] - "
            "%(levelname)s - %(message)s"
        )

    else:
        main_handler_formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(processName)s(%(process)d):%(threadName)s(%(thread)d) - "
            "[%(levelname)8s] %(name)s:%(lineno)d - %(message)s"
        )

    pyrogram_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
        "logs/pyrogram/pyrogram.log", when="midnight", encoding="utf-8"
    )
    pyrogram_handler.setFormatter(basic_formatter)

    event_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
        "logs/bot/events.log", when="midnight", encoding="utf-8"
    )
    event_handler.setFormatter(basic_formatter)

    main_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
        "logs/bot/bot.log", when="midnight", encoding="utf-8"
    )
    main_handler.setFormatter(main_handler_formatter)


# ---------------------------------------------------------------------------
#   Usable Loggers
# ---------------------------------------------------------------------------


# Pyrogram logger singleton
class PyrogramLogger:
    _instance: Optional["PyrogramLogger"] = None
    _initialized: bool = False

    logger: logging.Logger = logging.getLogger("pyrogram")

    def __init__(self, detail: bool = False):
        if self._initialized:
            return

        if detail:
            self.level: int = logging.INFO

        else:
            self.level: int = logging.WARNING

        self.logger.addHandler(Handlers.pyrogram_handler)
        self.logger.setLevel(self.level)
        coloredlogs.install(
            logger=self.logger, level=self.level, fmt=Handlers.read_format
        )

        self._initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


def event_logger(name: str) -> logging.Logger:
    """
    For those you don't want to see them in console.

    Args:
        name:

    Returns:

    """
    logger: logging.Logger = logging.Logger(f"event.{name}")
    logger.addHandler(Handlers.event_handler)
    logger.setLevel(LEVEL)
    logger.propagate = False

    return logger


def main_logger(name: str) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.addHandler(Handlers.main_handler)
    logger.setLevel(LEVEL)
    logger.propagate = False

    coloredlogs.install(logger=logger, level=LEVEL, fmt=Handlers.read_format)
    return logger
