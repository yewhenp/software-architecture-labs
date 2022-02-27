import argparse
import logging

from flask import Flask, make_response, jsonify, request
from flask.views import MethodView

logging_service_app = Flask(__name__)

database = {}


class LoggingServiceAPI(MethodView):
    def get(self):
        return make_response(jsonify(list(database.values())), 200)

    def post(self):
        body = request.get_json()
        request_uuid = body.get("uuid", None)
        request_msg = body.get("msg", None)
        if request_uuid is None or request_msg is None:
            make_response(jsonify({}), 400)
        database[request_uuid] = request_msg
        logging_service_app.logger.info(f"Got message: {request_uuid} - {request_msg}")
        return make_response(jsonify(None), 200)


logging_service_app.add_url_rule("/logging_service", view_func=LoggingServiceAPI.as_view("logging_service"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Logging service")
    parser.add_argument("--port", dest="port", default=8081, type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    logging_service_app.run(port=args.port)
