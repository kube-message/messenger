from wsgiref import simple_server

import falcon

import api
from .middleware import ResponseLoggerMiddleware


app = falcon.API(middleware=[ResponseLoggerMiddleware()])

"""
Messages URL"s
"""
app.add_route("/messages", api.MessageListResource())
app.add_route("/messages/{message_id}", api.MessageDetailResource())

"""
Thread URL"s
"""
app.add_route("/threads", api.ThreadListResource())
app.add_route("/threads/{thread_id:int}", api.ThreadDetailResource())
app.add_route("/threads/users/{user_id:int}", api.ThreadUserListResource())
app.add_route("/threads/{thread_id:int}/messages", api.ThreadMessageListResource())

"""
Health Check
"""
app.add_route("/shc", api.HealthCheckResource())


if __name__ == "__main__":
    httpd = simple_server.make_server("0.0.0.0", 8080, app)
    httpd.serve_forever()
