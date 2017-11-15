from proto import messenger
from services import messages, threads
from utils import get_logger


logger = get_logger()


class MessengerService(messenger.MessengerServicer):
    def create_thread(self, request, context):
        thread = threads.create_thread(request.participants)
        response = messenger.CreateThreadResponse(thread=threads.to_proto(thread))
        return response

    def get_thread_detail(self, request, context):
        thread = threads.get_thread_by_id(request.thread_id)
        response = messenger.GetThreadDetailResponse(thread=threads.to_proto(thread))
        return response

    def get_thread_messages(self, request, context):
        message_objs = threads.get_thread_messages(request.thread_id)
        message_protos = [messages.to_proto(m) for m in message_objs]
        response = messenger.GetThreadMessagesResponse(messages=message_protos)
        return response

    def get_threads_for_user(self, request, context):
        thread_objs = threads.get_threads_for_user(request.user_id)
        thread_protos = [threads.to_proto(t) for t in thread_objs]
        response = messenger.GetThreadsForUserResponse(threads=thread_protos)
        return response

    def send_message(self, request, context):
        message = messages.send_message(request.thread_id, request.sender_id, request.text)
        resposne = messenger.SendMessageResponse(message=messages.to_proto(message))
        return resposne
