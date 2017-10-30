import falcon
import json

from models import Thread, Message, session
from serializers import ModelSerializer


class HealthCheckResource(object):
    @staticmethod
    def on_get(request, response):
        response.status = falcon.HTTP_200
        response.data = json.dumps({"status": "OK"})


class ThreadListResource(object):
    @staticmethod
    def on_get(request, response):
        thread_objects = session.query(Thread).filter(
            Thread.participants.any(int(request.params.get("sender_id")))
        ).all()
        thread_dict = {t.pk: t.participants for t in thread_objects}
        response.data = json.dumps(thread_dict)
        response.status = falcon.HTTP_200

    @staticmethod
    def on_post(request, response):
        data = json.loads(request.stream.read())
        thread = Thread(participants=data.get("participants"))
        session.add(thread)
        session.commit()
        response.data = json.dumps({
            "threadId": thread.pk,
            "participants": thread.participants
        })
        response.status = falcon.HTTP_202


class ThreadMessageListResource(object):
    @staticmethod
    def on_get(request, response, thread_id):
        messages = session.query(Message).filter(Message.thread_id == thread_id)
        response.data = json.dumps({m.pk: m.text for m in messages})
        response.status = falcon.HTTP_200


class MessageListResource(object):
    @staticmethod
    def on_get(request, response):
        """
        Handle GET requests for message objects.
        Args:
            request: Falcon request object
            response: Falcon response object

        Returns:
            (response)
        """
        response.status = falcon.HTTP_200
        messages = session.query(Message).all()
        response.data = json.dumps({
            "links": {
                "self": "http://example.com/messages",
            },
            "data": [
                ModelSerializer(
                    message, ['text', 'sender_id', 'recipient_id']
                ).build_response()
                for message in messages
            ],
        })

    @staticmethod
    def on_post(request, response):
        data = json.loads(request.stream.read())
        message = Message(**data)
        session.add(message)
        session.commit()
        response.status = falcon.HTTP_201
        serializer = ModelSerializer(message, ['text', 'sender_id', 'recipient_id'])
        response.data = json.dumps(serializer.build_response())


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
        message = session.query(Message).get(message_id)
        if message is None:
            response.status = falcon.HTTP_404
        else:
            serializer = ModelSerializer(message, ['text', 'sender_id', 'recipient_id'])
            response.data = json.dumps(serializer.build_response())
