import argparse

from flask import Flask, make_response, jsonify, request
from flask.views import MethodView

from facade_service import FacadeService

facade_service_app = Flask(__name__)


class FacadeServiceAPI(MethodView):
    def __init__(self):
        super().__init__()
        self.service = FacadeService()

    def get(self):
        return make_response(jsonify(self.service.get_data()), 200)

    def post(self):
        body = request.get_data(as_text=True)
        if body is None:
            make_response(jsonify({}), 400)
        self.service.post_data(body)
        return make_response(jsonify(None), 200)


facade_service_app.add_url_rule("/facade_service", view_func=FacadeServiceAPI.as_view("facade_service"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Facade service")
    parser.add_argument("--port", dest="port", default=8080, type=int)
    args = parser.parse_args()

    facade_service_app.run(port=args.port)
