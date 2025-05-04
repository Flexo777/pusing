import tkinter as tk

class Dashboard:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title(f"RAPTOR CHAT - Welcome, {self.username}")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')
        
        # Header
        header = tk.Frame(self.root, bg='#3a3a5c')
        header.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(header, text=f"Welcome, {self.username}", 
                font=('Arial', 16), fg='white', bg='#3a3a5c').pack(side=tk.LEFT)
        
        # Main Content
        content = tk.Frame(self.root, bg='#f5f5f5')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Online Users
        online_frame = tk.LabelFrame(content, text=" Online Users ", 
                                   font=('Arial', 12), bg='#f5f5f5')
        online_frame.pack(fill=tk.X, pady=(0, 20))
        
        users = ["Gregory Floyd", "Sandy Smith"]
        for user in users:
            frame = tk.Frame(online_frame, bg='#f5f5f5')
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=f"• {user}", font=('Arial', 11), 
                    bg='#f5f5f5').pack(side=tk.LEFT)
            
            tk.Button(frame, text="Chat", bg='#4a90e2', fg='white',
                     command=lambda u=user: self.open_chat(u)).pack(side=tk.RIGHT)
        
        # Recent Activity
        activity_frame = tk.LabelFrame(content, text=" Recent Activity ",
                                     font=('Arial', 12), bg='#f5f5f5')
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        activities = [
            "Connected to chat server - Just now",
            "Logged in successfully - 2 minutes ago"
        ]
        
        for activity in activities:
            tk.Label(activity_frame, text=f"• {activity}", 
                    font=('Arial', 11), bg='#f5f5f5', anchor='w').pack(fill=tk.X)
    
    def open_chat(self, contact):
        from .chat import ChatWindow
        ChatWindow(self.username, contact).show()
    
    def show(self):
        self.root.mainloop()