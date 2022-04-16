import random
import uuid

import requests


class FacadeService:
    def __init__(self):
        self.logging_service_ips = [
            "http://localhost:8082",
            "http://localhost:8083",
            "http://localhost:8084",
        ]

    def get_data(self):
        from_messages = requests.get(url="http://localhost:8081/messages_service").json()
        try:
            from_logging = requests.get(url=f"{random.choice(self.logging_service_ips)}/logging_service").json()
        except:
            from_logging = "Error"
        return f"{from_messages} : {from_logging}"

    def post_data(self, body):
        request_uuid = str(uuid.uuid4())
        data = {
            "uuid": request_uuid,
            "msg": body
        }
        requests.post(url=f"{random.choice(self.logging_service_ips)}/logging_service", json=data)

