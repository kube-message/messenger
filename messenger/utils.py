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


def get_log_message_from_grpc_metadata(md):
    data = {k: v for k, v in md}
    endpoint = data["endpoint"]
    user_agent = data["user-agent"]
    caller = data["caller"]
    template = "endpoint: %s user-agent: %s response_code: [200] caller: %s"
    return template % (endpoint, user_agent, caller)
