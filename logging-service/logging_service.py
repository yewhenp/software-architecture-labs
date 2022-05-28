import subprocess

import hazelcast

from common import get_consul_and_register_service, suppress_hz_logs, get_map

suppress_hz_logs()


class LoggingService:
    hz = None
    consul_inst = None

    @staticmethod
    def register_in_consul(port):
        LoggingService.consul_inst = get_consul_and_register_service(port, "logging_service")

    def __init__(self, logger):
        self.logger = logger
        self.client = hazelcast.HazelcastClient()
        self.hazelcast_map = get_map(self.client, LoggingService.consul_inst)

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

