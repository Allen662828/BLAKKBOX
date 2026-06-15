"""
core/logger.py

Central logging configuration for the BLAKKBOX project.
"""

from __future__ import annotations

import logging
import sys

from configs.config import LOG_LEVEL


class Logger:

    _configured = False

    @classmethod
    def configure(cls) -> None:

        if cls._configured:
            return

        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
            format="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
            stream=sys.stdout,
        )

        cls._configured = True

    @classmethod
    def get(cls, name: str = "BLAKKBOX") -> logging.Logger:

        cls.configure()

        return logging.getLogger(name)


# ----------------------------------------------------------
# Default project logger
# ----------------------------------------------------------

logger = Logger.get()


# ----------------------------------------------------------
# Convenience wrappers
# ----------------------------------------------------------


def info(message: str) -> None:
    logger.info(message)


def debug(message: str) -> None:
    logger.debug(message)


def warning(message: str) -> None:
    logger.warning(message)


def error(message: str) -> None:
    logger.error(message)


def critical(message: str) -> None:
    logger.critical(message)


# ----------------------------------------------------------
# Section Header
# ----------------------------------------------------------


def section(title: str) -> None:

    logger.info("=" * 60)
    logger.info(title)
    logger.info("=" * 60)


# ----------------------------------------------------------
# Key / Value output
# ----------------------------------------------------------


def kv(key: str, value) -> None:

    logger.info(f"{key:<24}: {value}")
