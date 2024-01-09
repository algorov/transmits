import socket
import json
import threading

class TCPClient:
    def __init__(self):
        self.client_socket = None
        self.receive_thread = None

    def connect(self, server_ip, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")

    def send_data(self, data):
        if self.client_socket:
            json_data = json.dumps(data) + '\n'
            self.client_socket.send(json_data.encode('utf-8'))

    def receive_data_thread(self, callback):
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                received_data = json.loads(data.decode('utf-8'))
                callback(received_data)
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def start_receive_thread(self, callback):
        self.receive_thread = threading.Thread(target=self.receive_data_thread, args=(callback,))
        self.receive_thread.start()

    def close(self):
        if self.client_socket:
            self.client_socket.close()