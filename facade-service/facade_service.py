import random
import uuid
import requests

import hazelcast

from common import get_consul_and_register_service, get_queue


class FacadeService:
    consul_inst = None

    @staticmethod
    def register_in_consul(port):
        FacadeService.consul_inst = get_consul_and_register_service(port, "facade_service")

    def __init__(self):
        self.client = hazelcast.HazelcastClient()
        self.hazelcast_queue = get_queue(self.client, FacadeService.consul_inst)

    def get_data(self):
        available_services = FacadeService.consul_inst.agent.services()
        messages_service_ips = [val["Address"] + ":" + str(val["Port"]) for key, val in available_services.items() if val["Service"] == "messages_service"]
        logging_service_ips = [val["Address"] + ":" + str(val["Port"]) for key, val in available_services.items() if val["Service"] == "logging_service"]
        try:
            from_messages = requests.get(url=f"{random.choice(messages_service_ips)}/messages_service").json()
        except:
            from_messages = "Error"
        try:
            from_logging = requests.get(url=f"{random.choice(logging_service_ips)}/logging_service").json()
        except:
            from_logging = "Error"
        return f"MessagesService: {from_messages} : LoggingService: {from_logging}"

    def post_data(self, body):
        available_services = FacadeService.consul_inst.agent.services()
        logging_service_ips = [val["Address"] + ":" + str(val["Port"]) for key, val in available_services.items() if val["Service"] == "logging_service"]
        request_uuid = str(uuid.uuid4())
        data = {
            "uuid": request_uuid,
            "msg": body
        }
        requests.post(url=f"{random.choice(logging_service_ips)}/logging_service", json=data)
        self.hazelcast_queue.put(body)

