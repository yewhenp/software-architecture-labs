import random
import uuid

import hazelcast
import requests


class FacadeService:
    def __init__(self):
        self.logging_service_ips = [
            "http://localhost:8083",
            "http://localhost:8084",
            "http://localhost:8085",
        ]
        self.messages_service_ips = [
            "http://localhost:8081",
            "http://localhost:8082",
        ]
        self.client = hazelcast.HazelcastClient()
        self.hazelcast_queue = self.client.get_queue("messages-service-queue").blocking()

    def get_data(self):
        try:
            from_messages = requests.get(url=f"{random.choice(self.messages_service_ips)}/messages_service").json()
        except:
            from_messages = "Error"
        try:
            from_logging = requests.get(url=f"{random.choice(self.logging_service_ips)}/logging_service").json()
        except:
            from_logging = "Error"
        return f"MessagesService: {from_messages} : LoggingService: {from_logging}"

    def post_data(self, body):
        request_uuid = str(uuid.uuid4())
        data = {
            "uuid": request_uuid,
            "msg": body
        }
        requests.post(url=f"{random.choice(self.logging_service_ips)}/logging_service", json=data)
        self.hazelcast_queue.put(body)

