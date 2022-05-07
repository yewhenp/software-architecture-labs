import logging
import threading
import time

import hazelcast

hz_logger = logging.getLogger("hazelcast")
hz_logger.setLevel(logging.WARNING)


class MessagesService:
    client = None
    hazelcast_queue = None
    thread = None
    entries = []

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
        MessagesService.hazelcast_queue = MessagesService.client.get_queue("messages-service-queue").blocking()
        MessagesService.thread = threading.Thread(target=MessagesService.loop_records)
        MessagesService.thread.start()
