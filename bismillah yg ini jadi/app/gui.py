import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk

class ChatGUI:
    def __init__(self, username):
        self.username = username
        self.setup_dashboard()
        
    def setup_dashboard(self):
        self.root = tk.Tk()
        self.root.title(f"RAPTOR CHAT - Welcome, {self.username}")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')
        
        # Header
        header_frame = tk.Frame(self.root, bg='#3a3a5c')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome, {self.username}",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#3a3a5c'
        )
        welcome_label.pack(side=tk.LEFT, padx=10)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg='#f5f5f5')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Online Users Section
        online_frame = tk.LabelFrame(
            content_frame,
            text=" Online Users ",
            font=('Arial', 12),
            bg='#f5f5f5',
            fg='#333333'
        )
        online_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Sample Online Users
        users = [
            {"name": "Gregory Floyd", "status": "Online"},
            {"name": "Sandy Smith", "status": "Online"}
        ]
        
        for user in users:
            user_frame = tk.Frame(online_frame, bg='#f5f5f5')
            user_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                user_frame,
                text=f"• {user['name']}",
                font=('Arial', 11),
                bg='#f5f5f5',
                fg='#333333'
            ).pack(side=tk.LEFT)
            
            tk.Button(
                user_frame,
                text="Chat",
                bg='#4a90e2',
                fg='white',
                relief=tk.FLAT,
                command=lambda u=user: self.start_chat(u['name'])
            ).pack(side=tk.RIGHT, padx=10)
        
        # Recent Activity Section
        activity_frame = tk.LabelFrame(
            content_frame,
            text=" Recent Activity ",
            font=('Arial', 12),
            bg='#f5f5f5',
            fg='#333333'
        )
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        activities = [
            {"action": "Connected to chat server", "time": "Just now"},
            {"action": "Logged in successfully", "time": "2 minutes ago"}
        ]
        
        for activity in activities:
            activity_item = tk.Frame(activity_frame, bg='#f5f5f5')
            activity_item.pack(fill=tk.X, pady=5)
            
            tk.Label(
                activity_item,
                text=f"• {activity['action']}",
                font=('Arial', 11),
                bg='#f5f5f5',
                fg='#333333'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                activity_item,
                text=activity['time'],
                font=('Arial', 10),
                bg='#f5f5f5',
                fg='#777777'
            ).pack(side=tk.RIGHT)
    
    def start_chat(self, contact_name):
        # Implementasi buka window chat
        chat_window = tk.Toplevel()
        chat_window.title(f"Chat with {contact_name}")
        # ... tambahkan implementasi chat disini
    
    def run(self):
        self.root.mainloop()