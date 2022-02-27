import argparse

from flask import Flask, make_response, jsonify
from flask.views import MethodView

messages_service_app = Flask(__name__)


class MessagesServiceAPI(MethodView):
    def get(self):
        return make_response(jsonify("messages service not implemented yet"), 200)


messages_service_app.add_url_rule("/messages_service", view_func=MessagesServiceAPI.as_view("messages_service"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Messages service")
    parser.add_argument("--port", dest="port", default=8082, type=int)
    args = parser.parse_args()

    messages_service_app.run(port=args.port)
