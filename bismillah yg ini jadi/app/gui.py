import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import json
import base64
from .database import DatabaseManager
from .network import NetworkManager
from .crypto import CryptoManager
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class ChatGUI:
    def __init__(self, username):
        self.username = username
        self.db = DatabaseManager()
        self.crypto = CryptoManager()
        self.network = NetworkManager(self.receive_message)
        
        self.current_chat = None
        self.user_cache = {}
        
        self.setup_gui()
        self.load_contacts()
        self.network.start_server()
        
    def setup_gui(self):
        # Main window
        self.root = tk.Tk()
        self.root.title(f"Raptor Chat - {self.username}")
        self.root.geometry("900x600")
        self.root.configure(bg='#1e1e2d')
        
        # Left panel - Contacts
        self.left_panel = tk.Frame(self.root, width=250, bg='#25253b')
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        
        # Contact search
        self.search_frame = tk.Frame(self.left_panel, bg='#25253b')
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_entry = tk.Entry(self.search_frame, bg='#3a3a5c', fg='white', 
                                   insertbackground='white', relief=tk.FLAT)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.filter_contacts)
        
        # Contact list
        self.contact_list = tk.Listbox(self.left_panel, bg='#25253b', fg='white',
                                     selectbackground='#3a3a5c', selectforeground='white',
                                     borderwidth=0, highlightthickness=0)
        self.contact_list.pack(fill=tk.BOTH, expand=True)
        self.contact_list.bind('<<ListboxSelect>>', self.select_contact)
        
        # Right panel - Chat
        self.right_panel = tk.Frame(self.root, bg='#1e1e2d')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat header
        self.chat_header = tk.Frame(self.right_panel, height=50, bg='#25253b')
        self.chat_header.pack(fill=tk.X)
        self.chat_header.pack_propagate(False)
        
        self.chat_title = tk.Label(self.chat_header, text="Select a contact", 
                                  bg='#25253b', fg='white', font=('Arial', 12))
        self.chat_title.pack(side=tk.LEFT, padx=10)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.right_panel, bg='#1e1e2d', fg='white',
                                                    insertbackground='white', wrap=tk.WORD,
                                                    state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Message input
        self.input_frame = tk.Frame(self.right_panel, bg='#1e1e2d')
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.message_entry = tk.Text(self.input_frame, height=3, bg='#25253b', fg='white',
                                   insertbackground='white', wrap=tk.WORD)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind('<Return>', self.send_message_event)
        
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message,
                                   bg='#3a3a5c', fg='white', relief=tk.FLAT)
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Add contact button
        self.add_contact_button = tk.Button(self.left_panel, text="+ Add Contact", 
                                          command=self.add_contact_dialog,
                                          bg='#3a3a5c', fg='white', relief=tk.FLAT)
        self.add_contact_button.pack(fill=tk.X, padx=5, pady=5)
        
    def load_contacts(self):
        self.contact_list.delete(0, tk.END)
        users = self.db.get_all_users()
        for user in users:
            if user['username'] != self.username:
                self.contact_list.insert(tk.END, user['username'])
                self.user_cache[user['username']] = user
    
    def filter_contacts(self, event):
        search_term = self.search_entry.get().lower()
        self.contact_list.delete(0, tk.END)
        users = self.db.get_all_users()
        for user in users:
            if user['username'] != self.username and search_term in user['username'].lower():
                self.contact_list.insert(tk.END, user['username'])
    
    def select_contact(self, event):
        selection = self.contact_list.curselection()
        if selection:
            contact_name = self.contact_list.get(selection[0])
            self.current_chat = self.user_cache.get(contact_name)
            self.update_chat_display()
            self.chat_title.config(text=f"Chat with {contact_name}")
    
    def update_chat_display(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        
        if not self.current_chat:
            return
            
        current_user = self.db.get_user(self.username)
        messages = self.db.get_messages(current_user['id'], self.current_chat['id'])
        
        for msg in messages:
            sender = current_user['username'] if msg['sender_id'] == current_user['id'] else self.current_chat['username']
            is_me = sender == self.username
            
            # Decrypt message
            try:
                decrypted = self.crypto.decrypt_message(base64.b64decode(msg['encrypted_message']))
                message_text = decrypted.decode('utf-8')
            except Exception as e:
                message_text = "[Unable to decrypt message]"
            
            # Format message
            tag = "me" if is_me else "other"
            self.chat_display.tag_config(tag, 
                                       foreground='white',
                                       background='#3a3a5c' if is_me else '#25253b',
                                       lmargin1=20 if is_me else 50,
                                       rmargin=50 if is_me else 20,
                                       relief=tk.RAISED,
                                       borderwidth=2)
            
            self.chat_display.insert(tk.END, f"{sender}: {message_text}\n", tag)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message_event(self, event):
        if event.state == 0 and event.keysym == 'Return':
            self.send_message()
            return "break"
    
    def send_message(self):
        if not self.current_chat or not self.message_entry.get(1.0, tk.END).strip():
            return
            
        message = self.message_entry.get(1.0, tk.END).strip()
        self.message_entry.delete(1.0, tk.END)
        
        # Encrypt message
        try:
            receiver_public_key = serialization.load_pem_public_key(
                self.current_chat['public_key'].encode('utf-8'),
                backend=default_backend()
            )
            encrypted = self.crypto.encrypt_message(message.encode('utf-8'), receiver_public_key)
            encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
            
            # Save to database
            current_user = self.db.get_user(self.username)
            self.db.save_message(current_user['id'], self.current_chat['id'], encrypted_b64)
            
            # Send over network
            self.network.send_message(self.current_chat['ip_address'], message, receiver_public_key)
            
            # Update display
            self.update_chat_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
    
    def receive_message(self, sender_ip, message):
        # Find which contact this message is from
        for username, user in self.user_cache.items():
            if user['ip_address'] == sender_ip:
                # Save to database
                current_user = self.db.get_user(self.username)
                encrypted = self.crypto.encrypt_message(message.encode('utf-8'), 
                                                      self.crypto.public_key)
                encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
                self.db.save_message(user['id'], current_user['id'], encrypted_b64)
                
                # Update display if this is the current chat
                if self.current_chat and self.current_chat['username'] == username:
                    self.update_chat_display()
                break
    
    def add_contact_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Contact")
        dialog.geometry("400x200")
        dialog.configure(bg='#1e1e2d')
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Username:", bg='#1e1e2d', fg='white').pack(pady=(10, 0))
        username_entry = tk.Entry(dialog, bg='#25253b', fg='white', insertbackground='white')
        username_entry.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(dialog, text="IP Address:", bg='#1e1e2d', fg='white').pack()
        ip_entry = tk.Entry(dialog, bg='#25253b', fg='white', insertbackground='white')
        ip_entry.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(dialog, text="Public Key (PEM):", bg='#1e1e2d', fg='white').pack()
        key_entry = tk.Text(dialog, height=4, bg='#25253b', fg='white', insertbackground='white')
        key_entry.pack(fill=tk.X, padx=20, pady=5)
        
        def add_contact():
            username = username_entry.get().strip()
            ip_address = ip_entry.get().strip()
            public_key = key_entry.get(1.0, tk.END).strip()
            
            if not all([username, ip_address, public_key]):
                messagebox.showerror("Error", "All fields are required", parent=dialog)
                return
                
            try:
                # Validate public key
                serialization.load_pem_public_key(
                    public_key.encode('utf-8'),
                    backend=default_backend()
                )
                
                if self.db.add_user(username, public_key, ip_address):
                    messagebox.showinfo("Success", "Contact added successfully", parent=dialog)
                    self.load_contacts()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Username already exists", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid public key: {str(e)}", parent=dialog)
        
        tk.Button(dialog, text="Add", command=add_contact, 
                bg='#3a3a5c', fg='white').pack(pady=10)
    
    def run(self):
        self.root.mainloop()