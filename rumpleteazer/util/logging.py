import logging
from functools import lru_cache


logging.basicConfig(level=logging.DEBUG)


@lru_cache()
def get_logger(name, log_level=logging.INFO):
    """

    """
    logger = logging.getLogger(name)
    assert len(logger.handlers) == 0
    logger.setLevel(log_level)

    return logger
