import threading

import hazelcast

from common import get_queue, get_consul_and_register_service, suppress_hz_logs

suppress_hz_logs()


class MessagesService:
    client = None
    hazelcast_queue = None
    thread = None
    entries = []
    consul_inst = None

    @staticmethod
    def register_in_consul(port):
        MessagesService.consul_inst = get_consul_and_register_service(port, "messages_service")

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def get_records():
        return MessagesService.entries

    @staticmethod
    def loop_records():
        while 1:
            msg = MessagesService.hazelcast_queue.take()
            if msg:
                MessagesService.entries.append(msg)
                print(f"Got message: {msg}")

    @staticmethod
    def init_hz():
        MessagesService.client = hazelcast.HazelcastClient()
        MessagesService.hazelcast_queue = get_queue(MessagesService.client, MessagesService.consul_inst)
        MessagesService.thread = threading.Thread(target=MessagesService.loop_records)
        MessagesService.thread.start()
