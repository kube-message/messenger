from wsgiref import simple_server

import falcon

import api


app = falcon.API()

"""
Messages URL"s
"""
app.add_route("/message", api.MessageListResource())
app.add_route("/message/{message_id}", api.MessageDetailResource())

"""
Thread URL"s
"""
app.add_route("/thread", api.ThreadListResource())
app.add_route("/thread/{thread_id}/message", api.ThreadMessageListResource())

"""
Health Check
"""
app.add_route("/shc", api.HealthCheckResource())


if __name__ == "__main__":
    httpd = simple_server.make_server("0.0.0.0", 8080, app)
    httpd.serve_forever()
