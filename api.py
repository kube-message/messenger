import falcon
import json

from models import User, Message, session
from serializers import ModelSerializer


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
            import ipdb; ipdb.set_trace()
            response.data = json.dumps(serializer.build_response())


class UserListResource(object):
    @staticmethod
    def on_get(request, response):
        """
        Handles GET requests for UserListResource's

        Args:
            request: Falcon request object
            response: Falcon response object

        Returns:
            A serialized collection of User resources
        """
        response.status = falcon.HTTP_200
        users = session.query(User).all()
        response.data = json.dumps({
            "links": {
                "self": "http://example.com/users",
            },
            "data": [
                {
                    'type': 'users',
                    'id': user.id,
                    'attributes': {'username': user.username},
                }
                for user in users
            ],
        })

    @staticmethod
    def on_post(request, response):
        """
        Handles POST requests for UserList resources. Creates a new User resource.

        Args:
            request: a Falcon request object
            response: a Falcon response object

        Returns:
            The newly created User resource in a serialized format
        """
        data = json.loads(request.stream.read())
        user = User(**data)
        session.add(user)
        session.commit()
        serializer = ModelSerializer(user, ['username'])
        response.status = falcon.HTTP_201
        response.data = json.dumps(serializer.build_response())


class UserDetailResource(object):
    @staticmethod
    def on_get(request, response, user_id):
        """
        Handles GET requests for UserDetailResource's

        Args:
            request: Falcon request object
            response: Falcon response object
            user_id (int): a user ID

        Returns:
            A serialized User
        """
        user = session.query(User).get(user_id)
        if user is None:
            response.status = falcon.HTTP_404
        else:
            serializer = ModelSerializer(user, ['username'])
            response.data = json.dumps(serializer.build_response())

    @staticmethod
    def on_put(request, response, **kwargs):
        data = json.loads(request.stream.read())
        user = session.query(User).get(kwargs.get('user_id'))
        serializer = ModelSerializer(user, ['username'])
        serializer.update_model(data)
        session.add(user)
        session.commit()
        response.status = falcon.HTTP_202
        response.data = json.dumps(serializer.build_response())
