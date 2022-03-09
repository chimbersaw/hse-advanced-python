import codecs
import multiprocessing as mp
import os
import sys
import time
from datetime import datetime
from threading import Thread

run = True


def process_a(queue, out_conn):
    while True:
        s = queue.get()
        out_conn.send(s.lower())
        time.sleep(5)


def process_b(in_conn, out_conn):
    while True:
        out_conn.send(codecs.encode(in_conn.recv(), "rot13"))


def receiver_thread(in_conn):
    global run
    while run:
        if in_conn.poll(1):
            msg = in_conn.recv()
            print(f"Received: {msg} at {datetime.now().strftime('%H:%M:%S')}")


def sender_thread(queue):
    global run
    while True:
        msg = input().strip()
        if not msg:
            continue
        if msg == "q" or msg == "quit" or msg == "exit":
            break
        print(f"Sent: {msg} at {datetime.now().strftime('%H:%M:%S')}")
        queue.put(msg)
    run = False


def main():
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    sys.stdout = open("artifacts/hard.txt", 'w')
    queue = mp.Queue()
    a_to_b, b_from_a = mp.Pipe()
    b_to_main, main_from_b = mp.Pipe()
    a = mp.Process(target=process_a, args=(queue, a_to_b), daemon=True)
    b = mp.Process(target=process_b, args=(b_from_a, b_to_main), daemon=True)
    receiver = Thread(target=receiver_thread, args=(main_from_b,))
    sender = Thread(target=sender_thread, args=(queue,))

    a.start()
    b.start()
    receiver.start()
    sender.start()

    sender.join()
    receiver.join()
    queue.close()
    a_to_b.close()
    b_to_main.close()
    sys.stdout.close()


if __name__ == "__main__":
    main()
