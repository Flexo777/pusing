import sys
import tkinter as tk
from tkinter import simpledialog
from app.gui import ChatGUI
from app.database import DatabaseManager
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def main():
    # Ask for username
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Username", "Enter your username:", parent=root)
    
    if not username:
        sys.exit()
    
    # Check if user exists or create new
    db = DatabaseManager()
    user = db.get_user(username)
    
    if not user:
        # New user - we'd need to collect more info in a real app
        from app.crypto import CryptoManager
        crypto = CryptoManager()
        
        # Get public key as PEM
        public_key_pem = crypto.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        # For demo, we'll just use localhost
        # In a real app, you'd get the actual IP
        ip_address = "127.0.0.1"
        
        if not db.add_user(username, public_key_pem, ip_address):
            tk.messagebox.showerror("Error", "Failed to create user")
            sys.exit()
    
    # Start the chat GUI
    gui = ChatGUI(username)
    gui.run()

if __name__ == "__main__":
    main()