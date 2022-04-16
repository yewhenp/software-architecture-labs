import logging
import subprocess

import hazelcast

hz_logger = logging.getLogger("hazelcast")
hz_logger.setLevel(logging.WARNING)


class LoggingService:
    hz = None

    def __init__(self, logger):
        self.logger = logger
        self.client = hazelcast.HazelcastClient()
        self.hazelcast_map = self.client.get_map("logging-service-map").blocking()

    def get_records(self):
        return [value[1] for value in self.hazelcast_map.entry_set()]

    def put_record(self, uuid, msg):
        self.hazelcast_map.put(uuid, msg)
        self.logger.logger.info(f"Got message: {uuid} - {msg}")

    @staticmethod
    def run_hz():
        if LoggingService.hz is None:
            LoggingService.hz = subprocess.Popen(["hz", "start"],
                                                 stdout=subprocess.DEVNULL,
                                                 stderr=subprocess.DEVNULL)

