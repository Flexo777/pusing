import tkinter as tk

class ChatWindow:
    def __init__(self, username, contact):
        self.username = username
        self.contact = contact
        self.root = tk.Toplevel()
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title(f"Chat with {self.contact}")
        self.root.geometry("600x400")
        
        # Chat display
        self.chat_display = tk.Text(self.root, state='disabled')
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Message input
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X)
        
        self.message_entry = tk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(input_frame, text="Send", command=self.send_message).pack()
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.display_message(f"{self.username}: {message}")
            self.message_entry.delete(0, tk.END)
    
    def display_message(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state='disabled')
    
    def show(self):
        self.root.mainloop()