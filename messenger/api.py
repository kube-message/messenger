import falcon
import json

from services import messages, threads
from serializers import ModelSerializer


class HealthCheckResource(object):
    @staticmethod
    def on_get(request, response):
        response.status = falcon.HTTP_200
        response.data = json.dumps({"status": "OK"})


class ThreadListResource(object):
    @staticmethod
    def on_post(request, response):
        data = json.loads(request.stream.read())
        participants = data.get("participants")
        if not participants:
            response.status = falcon.HTTP_BAD_REQUEST
            response.data = json.dumps({"error": "particiapnts is a required field."})
            return
        thread = threads.create_thread(participants)
        response.data = json.dumps(ModelSerializer(thread, ["pk", "participants"]).build_response())
        response.status = falcon.HTTP_202


class ThreadMessageListResource(object):
    @staticmethod
    def on_get(request, response, thread_id):
        message_objects = messages.get_messages_for_thread(thread_id)
        response.data = json.dumps({m.pk: m.text for m in message_objects})
        response.status = falcon.HTTP_200


class ThreadUserListResource(object):
    @staticmethod
    def on_get(request, response, user_id):
        user_threads = threads.get_threads_for_user(user_id)
        response.data = json.dumps([ModelSerializer(t, ["pk", "particiapnts"]).build_response() for t in user_threads])
        response.status = falcon.HTTP_200


class MessageListResource(object):
    @staticmethod
    def on_post(request, response):
        data = json.loads(request.stream.read())
        try:
            thread_id, sender_id, text = data["thread_id"], data["sender_id"], data["text"]
        except KeyError as err:
            response.status = falcon.HTTP_400
            response.data = json.dumps({"error": "error sending message: %s" % err})
            return

        if threads.is_user_in_thread(sender_id, thread_id):
            message = messages.send_message(thread_id, sender_id, text)
            response.status = falcon.HTTP_201
            serializer = ModelSerializer(message, ['text', 'thread_id'])
            response.data = json.dumps(serializer.build_response())
        else:
            response.status = falcon.HTTP_400
            response.data = json.dumps({"error": "error sending message: sender not in thread"})
            return


class MessageDetailResource(object):
    @staticmethod
    def on_get(request, response, message_id):
        """
        Handle GET requests for message objects.
        Args:
            request: Falcon request object
            response: Falcon response object
            message_id (int): a message ID

        Returns:
            (response)
        """
        message = messages.get_message_by_id(message_id)
        if message is None:
            response.status = falcon.HTTP_404
        else:
            serializer = ModelSerializer(message, ['text', 'sender_id', 'thread_id'])
            response.data = json.dumps(serializer.build_response())
