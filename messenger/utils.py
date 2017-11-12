import logging
import sys

_logger = None


def get_logger():
    global _logger
    if _logger is None:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        log_format = "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d:p%(process)s] %(message)s"
        logging.basicConfig(format=log_format, level=logging.INFO, handlers=[ch])
        _logger = logging.getLogger(__name__)
    return _logger
