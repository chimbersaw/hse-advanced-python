import multiprocessing as mp
import os
import time
from threading import Thread

N = 100000
NUM_RUNS = 10


def fib(n):
    result = [0] * n
    result[1] = 1
    for i in range(2, n):
        result[i] = result[i - 1] + result[i - 2]
    return result


def synchronized():
    for i in range(NUM_RUNS):
        fib(N)


def use_threads():
    threads = [Thread(target=fib, args=(N,)) for _ in range(NUM_RUNS)]
    [t.start() for t in threads]
    [t.join() for t in threads]


def use_processes():
    processes = [mp.Process(target=fib, args=(N,)) for _ in range(NUM_RUNS)]
    [p.start() for p in processes]
    [p.join() for p in processes]


def timed(f):
    start = time.time()
    f()
    return time.time() - start


def main():
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    with open("artifacts/easy.txt", "w") as file:
        file.write(f"Synchronized: {timed(synchronized)} sec\n")
        file.write(f"Threads: {timed(use_threads)} sec\n")
        file.write(f"Processes: {timed(use_processes)} sec\n")


if __name__ == "__main__":
    main()
