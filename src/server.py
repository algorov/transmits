import socket
import json
from time import sleep

HOST = '127.0.0.1'  # IP-адрес сервера
PORT = 65432  # Порт для прослушивания
data = {
    "data": {
        "sender": "Alice",
        "recipient": "Bob",
        "msg": "Привет, Bob! Как дела?"
    }
}

json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Привязка сервера к адресу и порту
    server_socket.listen()  # Начало прослушивания входящих соединений
    print('Server is listening...')

    conn, addr = server_socket.accept()  # Принятие входящего соединения
    with conn:
        print('Connected by', addr)
        while True:
            conn.send(json_str)
            sleep(5)
