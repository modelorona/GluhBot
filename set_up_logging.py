import logging
from os import getenv

if getenv('LOGGING'):
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


def get_logger():
    if getenv('LOGGING'):
        return logging.getLogger('discord')