import json
import os

import requests

from proto import messenger
from services import messages, threads
from utils import get_logger, get_log_message_from_grpc_metadata


logger = get_logger()
PUSH_URL = "http://{}:{}/pub/?id=ch1".format(os.environ.get("PUSH_SERVICE_HOST"), os.environ.get("PUSH_SERVICE_PORT"))


def log_request(ctx):
    logger.info(get_log_message_from_grpc_metadata(ctx.invocation_metadata()))


class MessengerService(messenger.MessengerServicer):
    def create_thread(self, request, context):
        thread = threads.create_thread(list(request.participants))
        response = messenger.CreateThreadResponse(thread=threads.to_proto(thread))
        log_request(context)
        return response

    def get_thread_detail(self, request, context):
        thread = threads.get_thread_by_id(request.thread_id)
        response = messenger.GetThreadDetailResponse(thread=threads.to_proto(thread))
        log_request(context)
        return response

    def get_thread_messages(self, request, context):
        message_objs = messages.get_messages_for_thread(request.thread_id)
        message_protos = [messages.to_proto(m) for m in message_objs]
        response = messenger.GetThreadMessagesResponse(messages=message_protos)
        log_request(context)
        return response

    def get_threads_for_user(self, request, context):
        thread_objs = threads.get_threads_for_user(request.user_id)
        thread_protos = [threads.to_proto(t) for t in thread_objs]
        response = messenger.GetThreadsForUserResponse(threads=thread_protos)
        log_request(context)
        return response

    def send_message(self, request, context):
        message_pb = request.message
        message = messages.send_message(message_pb.thread_id, message_pb.sender_id, message_pb.text)
        response = messenger.SendMessageResponse(message=messages.to_proto(message))
        try:
            requests.post(PUSH_URL, data=json.dumps({"userId": message.sender_id, "message": message.text}))
        except Exception:
            pass
        log_request(context)
        return response
