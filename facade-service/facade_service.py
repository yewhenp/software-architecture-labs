import argparse
import uuid

import requests
from flask import Flask, make_response, jsonify, request
from flask.views import MethodView

facade_service_app = Flask(__name__)


class FacadeServiceAPI(MethodView):
    def get(self):
        from_messages = requests.get(url="http://localhost:8082/messages_service").json()
        from_logging = requests.get(url="http://localhost:8081/logging_service").json()
        return make_response(jsonify(f"{from_messages} : {from_logging}"), 200)

    def post(self):
        body = request.get_data(as_text=True)
        request_uuid = str(uuid.uuid4())

        if body is None:
            make_response(jsonify({}), 400)

        data = {
            "uuid": request_uuid,
            "msg": body
        }
        requests.post(url="http://localhost:8081/logging_service", json=data)

        return make_response(jsonify(None), 200)


facade_service_app.add_url_rule("/facade_service", view_func=FacadeServiceAPI.as_view("facade_service"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Facade service")
    parser.add_argument("--port", dest="port", default=8080, type=int)
    args = parser.parse_args()

    facade_service_app.run(port=args.port)
