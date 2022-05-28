import logging

import consul


def get_consul_value_or_set_default(consul_inst, key, default_value):
    name_idx, name = consul_inst.kv.get(key)
    if name is None:
        name = default_value
        consul_inst.kv.put(key, name)
    else:
        name = name["Value"].decode()
    return name


def get_queue(hz_client, consul_inst):
    hz_queue_name = get_consul_value_or_set_default(consul_inst, "hz_queue_name", "messages-service-queue")
    hazelcast_queue = hz_client.get_queue(hz_queue_name).blocking()
    return hazelcast_queue


def get_map(hz_client, consul_inst):
    hz_map_name = get_consul_value_or_set_default(consul_inst, "hz_map_name", "logging-service-map")
    hazelcast_map = hz_client.get_map(hz_map_name).blocking()
    return hazelcast_map


def get_consul_and_register_service(port, service_name):
    consul_inst = consul.Consul()
    consul_inst.agent.service.register(service_name, address='http://localhost', port=port,
                                                       service_id=f"{service_name}_{port}")
    return consul_inst


def suppress_hz_logs():
    hz_logger = logging.getLogger("hazelcast")
    hz_logger.setLevel(logging.WARNING)
