import logging
from os import getenv


def info(text: str) -> None:
    if getenv('LOGGING'):
        get_logger().info(text)


def error(text: str) -> None:
    if getenv('LOGGING'):
        get_logger().error(text)


def get_logger() -> logging.Logger:
    return logging.getLogger('discord')


if getenv('LOGGING'):
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)