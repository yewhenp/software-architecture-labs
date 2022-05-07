import argparse
import logging

from flask import Flask, make_response, jsonify
from flask.views import MethodView

from messages_service import MessagesService

messages_service_app = Flask(__name__)


class MessagesServiceAPI(MethodView):
    def __init__(self):
        super().__init__()
        self.service = MessagesService(messages_service_app)

    def get(self):
        return make_response(jsonify(list(self.service.get_records())), 200)


messages_service_app.add_url_rule("/messages_service", view_func=MessagesServiceAPI.as_view("messages_service"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Messages service")
    parser.add_argument("--port", dest="port", default=8081, type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    MessagesService.init_hz()
    messages_service_app.run(port=args.port)
