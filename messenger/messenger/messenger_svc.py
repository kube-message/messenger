import json
import os

import requests

from .proto import messenger
from .services import messages, threads
from .utils import get_logger, get_log_message_from_grpc_metadata


logger = get_logger()
PUSH_URL = "http://{}:{}/pub/?id=ch1".format(os.environ.get("PUSH_SERVICE_HOST"), os.environ.get("PUSH_SERVICE_PORT"))


def log_request(ctx):
    logger.info(get_log_message_from_grpc_metadata(ctx.invocation_metadata()))


class MessengerService(messenger.MessengerServicer):
    def create_thread(self, request, context):
        """
        Create a new thread.

        Args:
            request (messenger.CreateThreadRequest): A request to create a thread.
            context:

        Returns:
            messenger.CreateThreadResponse
        """
        thread = threads.create_thread(list(request.participants))
        response = messenger.CreateThreadResponse(thread=threads.to_proto(thread))
        log_request(context)
        return response

    def get_thread_detail(self, request, context):
        """
        Get the details of a single thread.

        Args:
            request (messages.GetThreadDetailRequest):
            context:

        Returns:
            messages.GetThreadDetailResponse
        """
        thread = threads.get_thread_by_id(request.thread_id)
        response = messenger.GetThreadDetailResponse(thread=threads.to_proto(thread))
        log_request(context)
        return response

    def get_thread_messages(self, request, context):
        """
        Get the messages for a given thread.

        Args:
            request (messages.GetThreadMessagesRequest):
            context:

        Returns:
            messages.GetThreadMessagesResponse
        """
        message_objs = messages.get_messages_for_thread(request.thread_id)
        message_protos = [messages.to_proto(m) for m in message_objs]
        response = messenger.GetThreadMessagesResponse(messages=message_protos)
        log_request(context)
        return response

    def get_threads_for_user(self, request, context):
        """
        Get all the threads for a given user.

        Args:
            request (messages.GetThreadsForUserRequest):
            context:

        Returns:
            messages.GetThreadsForUserResponse
        """
        thread_objs = threads.get_threads_for_user(request.user_id)
        thread_protos = [threads.to_proto(t) for t in thread_objs]
        response = messenger.GetThreadsForUserResponse(threads=thread_protos)
        log_request(context)
        return response

    def send_message(self, request, context):
        """
        Send a new message for the given thread ID

        Args:
            request (messages.SendMessageRequest):
            context:

        Returns:
            messages.SendMessageResponse
        """
        message_pb = request.message
        message = messages.send_message(message_pb.thread_id, message_pb.sender_id, message_pb.text)
        response = messenger.SendMessageResponse(message=messages.to_proto(message))
        try:
            requests.post(PUSH_URL, data=json.dumps({"userId": message.sender_id, "message": message.text}).encode())
        except Exception:
            pass
        log_request(context)
        return response

    def get_message_detail(self, request, context):
        """
        Get the details for a single message.

        Args:
            request (messages.GetMessageDetialRequest):
            context:

        Returns:
            messages.GetMessageDetailResponse
        """
        message = messages.get_message_by_id(request.message_id)
        response = messenger.GetThreadMessagesResponse(message=messages.to_proto(message))
        log_request(context)
        return response
