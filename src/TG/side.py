import sys
import threading
import socket
import json
import queue

from datetime import datetime
from bot.Bot import Bot
from config import *

rec_msgs = {}
depart_msgs = queue.Queue()


def listen_server(rec_msgs: dict, depart_queue: queue.Queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bot_socket:
        bot_socket.settimeout(timeout)
        bot_socket.connect((sys.argv[1], int(sys.argv[2])))

        while True:
            try:
                rec_data = bot_socket.recv(1024)
                data = rec_data.decode('utf-8')

                print("[REC] Received data from server:", data)

                tg_id = json.loads(data).get("data").get("recipient")
                current_datetime = datetime.now()
                date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                if not (tg_id in rec_msgs):
                    rec_msgs[tg_id] = {}

                rec_msgs[tg_id][date] = data
            except TimeoutError:
                pass
                # print("[INFO] Rec timeout expired")

            try:
                dep_data = depart_queue.get_nowait()
                bot_socket.send(dep_data.encode('utf-8'))

                print(f'[SEND] JSON was send to server: {dep_data[:-1]}')
            except queue.Empty:
                pass
                # print("[INFO] Depart queue is empty")


def start_bot(recs: dict, departs: queue.Queue):
    bot = Bot(recs, departs)
    bot.start()


def validate_args(host, port):
    if not host or not port.isdigit() or not (0 <= int(port) <= 65535):
        return False
    return True


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if validate_args(sys.argv[1], sys.argv[2]):
            handler = threading.Thread(target=listen_server, args=(rec_msgs, depart_msgs))
            handler.start()
            start_bot(rec_msgs, depart_msgs)
            handler.join()
        else:
            print("[ERROR] Invalid arguments")
    else:
        print("[ERROR] args != 2")
