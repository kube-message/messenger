from __future__ import absolute_import

from concurrent import futures
import time

import grpc

from messenger.proto import messenger
from messenger.messenger_svc import MessengerService
from messenger.utils import get_logger


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
logger = get_logger()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger.add_MessengerServicer_to_server(MessengerService(), server)
    server.add_insecure_port("[::]:8081")
    logger.info("Starting messenger service...")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
