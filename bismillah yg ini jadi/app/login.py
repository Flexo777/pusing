import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .register import RegisterWindow 

class LoginWindow:
    def __init__(self, on_login_success, on_register_success=None):  # Tambahkan parameter ini
        self.root = tk.Tk()
        self.on_login_success = on_login_success
        self.on_register_success = on_register_success  # Simpan parameter baru
        self.setup_ui()
        
    def setup_ui(self):
        # Window Configuration
        self.root.title("RAPTOR CHAT")
        self.root.geometry("400x500")
        self.root.configure(bg='#1e1e2d')
        self.root.resizable(False, False)
        
        # Header
        header = tk.Frame(self.root, bg='#1e1e2d')
        header.pack(pady=40)
        
        logo_label = tk.Label(
            header, 
            text="RAPTOR CHAT", 
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#1e1e2d'
        )
        logo_label.pack()
        
        # Login Form
        form_frame = tk.Frame(self.root, bg='#1e1e2d')
        form_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Email Field
        tk.Label(
            form_frame, 
            text="Email", 
            bg='#1e1e2d',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.email_entry = ttk.Entry(
            form_frame, 
            style='Custom.TEntry'
        )
        self.email_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Password Field
        tk.Label(
            form_frame, 
            text="Password", 
            bg='#1e1e2d',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.password_entry = ttk.Entry(
            form_frame, 
            show="*",
            style='Custom.TEntry'
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Login Button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            command=self.attempt_login,
            bg='#3a3a5c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        login_btn.pack(fill=tk.X, pady=10)
        
        # Register Link
        register_frame = tk.Frame(self.root, bg='#1e1e2d')
        register_frame.pack()
        
        tk.Label(
            register_frame,
            text="Don't have an account?",
            bg='#1e1e2d',
            fg='white'
        ).pack(side=tk.LEFT)
        
        register_link = tk.Label(
            register_frame,
            text="Register here",
            fg='#4a90e2',
            bg='#1e1e2d',
            cursor="hand2"
        )
        register_link.pack(side=tk.LEFT)
        register_link.bind("<Button-1>", lambda e: self.show_register())

    def show_register(self):
        if not hasattr(self, 'on_register_success') or not self.on_register_success:
            messagebox.showinfo("Info", "Register feature not available")
            return
            
        self.root.withdraw()
        RegisterWindow(
            on_register_success=self.on_register_success,
            switch_to_login=self.show
        ).run()
        
    def attempt_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if email and password:
            self.on_login_success(email)  # Pindah ke main chat
        else:
            messagebox.showerror("Error", "Please fill all fields")
            
    def show_register(self):
        if not hasattr(self, 'on_register_success'):
            messagebox.showinfo("Info", "Register feature coming soon", parent=self.root)
            return
        
        self.root.withdraw()
        from .register import RegisterWindow  # Import langsung di sini
        RegisterWindow(
            on_register_success=self.on_register_success,
            switch_to_login=lambda: self.root.deiconify()
        ).run()
        
    def run(self):
        self.root.mainloop()