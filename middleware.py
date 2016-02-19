from base64 import b64decode
from hashlib import sha256

import falcon

import config
from models import User, session


class AuthenticationMiddleware(object):
    """
    Middleware to parse the ``AUTHORIZATION`` header of an incoming request.
    """
    def process_request(self, request, response):
        try:
            self.validate_public_endpoint(request)
            auth_header = request.headers.get('AUTHORIZATION')
            username, password = self.decode_auth_header(auth_header)
            self.validate_user(username, password)
        except AttributeError:
            response.status = falcon.HTTP_400
            raise falcon.HTTPBadRequest(
                'Bad Request',
                'There was something wrong with your request'
            )

    @staticmethod
    def decode_auth_header(auth_header):
        try:
            encoded_string = auth_header.split()[1]
            username, password = b64decode(encoded_string).split(':')
            password = sha256(password).hexdigest()
            return username, password
        except (AttributeError, ValueError):
            raise falcon.HTTPBadRequest(
                'Bad Request',
                'There was an issue parsing the AUTHORIZATION header of your request.'
            )

    @staticmethod
    def is_public_endpoint(request):
        return all([request.path in config.PUBLIC_ENDPOINTS,
                    request.method in config.PUBLIC_ENDPOINTS.get(request.path)])

    def validate_public_endpoint(self, request):
        if self.is_public_endpoint(request) or request.headers.get('AUTHORIZATION'):
            return
        else:
            raise falcon.HTTPUnauthorized(
                'Unauthorized',
                'You are not allowed to access this endpoint'
            )

    @staticmethod
    def validate_user(username, password):
        user = session.query(User).filter_by(username=username).first()
        if password != user.password:
            raise falcon.HTTPUnauthorized(
                'Permission Denied',
                'Invalid authentication credentials'
            )
