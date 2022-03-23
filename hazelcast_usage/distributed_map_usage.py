import hazelcast


def create_many_entries_inside_map():
    client = hazelcast.HazelcastClient()
    hazelcast_map = client.get_map("my-distributed-map").blocking()

    for i in range(1000):
        hazelcast_map.put(i, i)
        print(f"{i} done")

    client.shutdown()


if __name__ == '__main__':
    create_many_entries_inside_map()
