import multiprocessing
import time

import hazelcast


class Value:
    def __init__(self, amount=0):
        self.amount = amount


def run_map_test_no_lock():
    client = hazelcast.HazelcastClient()
    hazelcast_map = client.get_map("map").blocking()
    key = "1"

    for k in range(1000):
        value = hazelcast_map.get(key)
        value.amount += 1
        hazelcast_map.put(key, value)

    client.shutdown()


def run_map_test_pessimistic_lock():
    client = hazelcast.HazelcastClient()
    hazelcast_map = client.get_map("map").blocking()
    key = "1"

    for k in range(1000):
        while True:
            hazelcast_map.lock(key)
            try:
                value = hazelcast_map.get(key)
                value.amount += 1
                hazelcast_map.put(key, value)
            except Exception:
                continue
            else:
                break
            finally:
                hazelcast_map.unlock(key)

    client.shutdown()


def run_map_test_optimistic_lock():
    client = hazelcast.HazelcastClient()
    hazelcast_map = client.get_map("map").blocking()
    key = "1"

    for k in range(1000):
        while True:
            value = hazelcast_map.get(key)
            new_value = Value(value.amount)
            new_value.amount += 1
            if hazelcast_map.replace_if_same(key, value, new_value):
                break

    client.shutdown()


def make_test(target, name, hazelcast_map):
    print(f"Test {name}:")
    hazelcast_map.put("1", Value())

    time_start = time.time()
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=target)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"Finished, result is {hazelcast_map.get('1').amount}; time spent = {time.time() - time_start} s\n")


if __name__ == '__main__':
    client = hazelcast.HazelcastClient()
    hazelcast_map = client.get_map("map").blocking()
    make_test(run_map_test_no_lock, "no lock", hazelcast_map)
    make_test(run_map_test_pessimistic_lock, "pessimistic lock", hazelcast_map)
    make_test(run_map_test_optimistic_lock, "optimistic lock", hazelcast_map)
    client.shutdown()
