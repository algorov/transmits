import socket
import queue
import threading

from bot.Bot import Bot
from config import *

rec_msg_queue = queue.Queue()
depart_msg_queue = queue.Queue()


def listen_server(rec_queue: queue.Queue, depart_queue: queue.Queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bot_socket:
        bot_socket.settimeout(timeout)
        bot_socket.connect((SERVER_HOST, SERVER_PORT))

        while True:
            try:
                rec_data = bot_socket.recv(1024)
                data = rec_data.decode('utf-8')
                # print("Received data:", data)
                rec_queue.put(data)
            except TimeoutError:
                print("[ERROR] Timeout")

            try:
                dep_data = depart_queue.get_nowait()
                bot_socket.send(dep_data.encode('utf-8'))
            except queue.Empty:
                print("[ERROR] Queue")


def start_bot(rec_queue: queue.Queue, depart_queue: queue.Queue):
    bot = Bot(rec_queue, depart_queue)
    bot.start()


if __name__ == '__main__':
    handler = threading.Thread(target=listen_server, args=(rec_msg_queue, depart_msg_queue))
    handler.start()
    start_bot(rec_msg_queue, depart_msg_queue)
    handler.join()
