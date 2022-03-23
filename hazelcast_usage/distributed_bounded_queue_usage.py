import multiprocessing
import hazelcast


def queue_producer(process_id, N):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("my-bounded-queue").blocking()

    for i in range(N):
        rez = queue.offer(f"hello_{i}")
        rez and print(f"Process {process_id} - producer - offer {i} done")
        not rez and print(f"Process {process_id} - producer - offer {i} failed - queue full")

    client.shutdown()


def queue_consumer(process_id, N):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("my-bounded-queue").blocking()

    for i in range(N):
        rez = queue.poll(timeout=2)
        rez and print(f"Process {process_id} - consumer - take {rez} done")
        not rez and print(f"Process {process_id} - consumer - take failed after timeout - queue empty")

    client.shutdown()


def make_test(targets, Ns, test_name):
    print(test_name)

    processes = []
    for i in range(len(targets)):
        p = multiprocessing.Process(target=targets[i], args=(i, Ns[i],))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print()
    print()


if __name__ == '__main__':
    make_test(Ns=[6, 3, 3],
              targets=[queue_producer, queue_consumer, queue_consumer],
              test_name="Test 1 producer 2 consumers")

    make_test(Ns=[6],
              targets=[queue_producer],
              test_name="Test 1 producer no consumer (will exceed max size)")