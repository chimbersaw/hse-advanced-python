import math
import multiprocessing as mp
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from matplotlib import pyplot as plt

UPPER_BOUND = mp.cpu_count() * 2
N_ITER = int(1e8)


def integrate(f, a, b, step):
    acc = 0
    cur = a
    start = time.time()
    while cur < b:
        acc += f(cur) * min(step, b - cur)
        cur += step
    end = time.time()
    return acc, a, b, start, end


def integrate_concurrent(f, a, b, get_executor, n_jobs=1, n_iter=N_ITER):
    all_start = time.time()
    step = (b - a) / n_iter
    job_step = (b - a) / n_jobs
    cur = 0
    res = 0
    log = ""
    with get_executor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            futures.append(executor.submit(integrate, f, cur, min(b, cur + job_step), step))
            cur += job_step
        for f in futures:
            acc, l, r, start, end = f.result()
            start -= all_start
            end -= all_start
            res += acc
            log += f"Integrated [{l:.2f}, {r:.2f}] from {start:.3f} to {end:.3f} seconds\n"
    return res, log


def main():
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    thread_results = []
    mp_results = []
    with open("artifacts/medium-logs.txt", "w") as file:
        for n_jobs in range(1, UPPER_BOUND + 1):
            start = time.time()
            res, log = integrate_concurrent(math.cos, 0, math.pi / 2, ThreadPoolExecutor, n_jobs=n_jobs)
            dur = time.time() - start
            file.write(f"Threadpool with n_jobs={n_jobs} executed in {dur:.5f} seconds, res={res}\n")
            file.write("\t" + log[:-1].replace("\n", "\n\t") + "\n")
            thread_results.append((res, dur))

            start = time.time()
            res, log = integrate_concurrent(math.cos, 0, math.pi / 2, ProcessPoolExecutor, n_jobs=n_jobs)
            dur = time.time() - start
            file.write(f"Processpool with n_jobs={n_jobs} executed in {dur:.5f} seconds, res={res}\n")
            file.write("\t" + log[:-1].replace("\n", "\n\t") + "\n")
            mp_results.append((res, dur))
            print(f"{n_jobs} done", flush=True)
    with open("artifacts/medium-results.txt", "w") as file:
        for i, (res, dur) in enumerate(thread_results):
            file.write(f"Threadpool with n_jobs={i + 1} executed in {dur:.5f} seconds, res={res}\n")
        file.write("\n")
        for i, (res, dur) in enumerate(mp_results):
            file.write(f"Processpool with n_jobs={i + 1} executed in {dur:.5f} seconds, res={res}\n")
    thread_times = [x[1] for x in thread_results]
    mp_times = [x[1] for x in mp_results]

    plt.xlabel("n_jobs")
    plt.ylabel("Time in seconds")
    plt.plot(list(range(1, UPPER_BOUND + 1)), thread_times, label="Threads")
    plt.plot(list(range(1, UPPER_BOUND + 1)), mp_times, label="Processes")
    plt.legend()
    plt.savefig("artifacts/medium-plot.png")


if __name__ == "__main__":
    main()
