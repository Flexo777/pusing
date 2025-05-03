import socket
import threading
import json
from queue import Queue
from .crypto import CryptoManager

class NetworkManager:
    def __init__(self, message_callback=None):
        self.crypto = CryptoManager()
        self.message_callback = message_callback
        self.socket = None
        self.receive_queue = Queue()
        self.running = False
        
        with open('../config/config.json') as config_file:
            config = json.load(config_file)
        self.server_ip = config['server_ip']
        self.server_port = config['server_port']

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.server_ip, self.server_port))
        self.socket.listen(5)
        self.running = True
        threading.Thread(target=self._accept_connections, daemon=True).start()
        threading.Thread(target=self._process_messages, daemon=True).start()

    def _accept_connections(self):
        while self.running:
            try:
                conn, addr = self.socket.accept()
                threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
            except OSError:
                break

    def _handle_client(self, conn, addr):
        try:
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break
                decrypted = self.crypto.decrypt_message(data)
                self.receive_queue.put((addr[0], decrypted.decode('utf-8')))
        finally:
            conn.close()

    def _process_messages(self):
        while self.running:
            sender_ip, message = self.receive_queue.get()
            if self.message_callback:
                self.message_callback(sender_ip, message)

    def send_message(self, receiver_ip: str, message: str, receiver_public_key: bytes):
        try:
            encrypted = self.crypto.encrypt_message(message.encode('utf-8'), receiver_public_key)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((receiver_ip, self.server_port))
                s.sendall(encrypted)
            return True
        except Exception as e:
            print(f"Failed to send message: {str(e)}")
            return False

    def stop_server(self):
        self.running = False
        if self.socket:
            self.socket.close()