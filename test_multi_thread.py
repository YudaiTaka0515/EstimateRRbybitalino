import threading
import time

# Hello, Multi thread


def worker_1():
    while True:
        elapsed_time = time.clock()
        time.sleep(10)
        print("worker1:", elapsed_time)

        if elapsed_time > 100:
            break


def worker_2():
    while True:
        elapsed_time = time.clock()
        time.sleep(10)
        print("worker2:", elapsed_time)

        if elapsed_time > 100:
            break


if __name__ == '__main__':
    t1 = threading.Thread(target=worker_1)
    t2 = threading.Thread(target=worker_2)
    t1.start()
    t2.start()
