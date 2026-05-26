import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{name}</cyan> | {message}", level="DEBUG")
logger.add("logs/backend.log", rotation="10 MB", retention=7, level="DEBUG", encoding="utf-8")

__all__ = ["logger"]
