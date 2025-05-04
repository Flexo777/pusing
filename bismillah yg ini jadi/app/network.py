import socket
import threading
from queue import Queue

class NetworkManager:
    def __init__(self, message_callback=None):
        self.message_callback = message_callback
        self.receive_queue = Queue()
        self.running = False
        
    def start_server(self, host='127.0.0.1', port=5000):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.running = True
        
        # Start thread untuk menerima koneksi
        threading.Thread(target=self._accept_connections, daemon=True).start()
        threading.Thread(target=self._process_messages, daemon=True).start()
    
    def _accept_connections(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                ).start()
            except:
                break
    
    def _handle_client(self, conn, addr):
        try:
            while self.running:
                data = conn.recv(4096)
                if not data:
                    break
                if self.message_callback:
                    self.receive_queue.put((addr[0], data.decode()))
        finally:
            conn.close()
    
    def _process_messages(self):
        while self.running:
            sender_ip, message = self.receive_queue.get()
            if self.message_callback:
                self.message_callback(sender_ip, message)
    
    def send_message(self, receiver_ip: str, message: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((receiver_ip, 5000))
                s.sendall(message.encode())
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False
    
    def stop_server(self):
        self.running = False
        if hasattr(self, 'server_socket'):
            self.server_socket.close()