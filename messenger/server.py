from wsgiref import simple_server

import falcon

import api
from middleware import AuthenticationMiddleware


app = falcon.API()

"""
Messages URL"s
"""
app.add_route("/messages", api.MessageListResource())
app.add_route("/messages/{message_id}", api.MessageDetailResource())

"""
User URL"s
"""
app.add_route("/users", api.UserListResource())
app.add_route("/users/{user_id}", api.UserDetailResource())

"""
Health Check
"""
app.add_route("/shc", api.HealthCheckResource())


if __name__ == "__main__":
    httpd = simple_server.make_server("0.0.0.0", 8080, app)
    httpd.serve_forever()
