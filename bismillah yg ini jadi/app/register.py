import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class RegisterWindow:
    def __init__(self, on_register_success, switch_to_login):
        self.root = tk.Toplevel()
        self.on_register_success = on_register_success
        self.switch_to_login = switch_to_login
        self.setup_ui()
        
    def setup_ui(self):
        # Window Configuration
        self.root.title("RAPTOR CHAT - Register")
        self.root.geometry("400x600")
        self.root.configure(bg='#1e1e2d')
        self.root.resizable(False, False)
        
        # Header
        header = tk.Frame(self.root, bg='#1e1e2d')
        header.pack(pady=30)
        
        logo_label = tk.Label(
            header, 
            text="RAPTOR CHAT", 
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#1e1e2d'
        )
        logo_label.pack()
        
        # Register Form
        form_frame = tk.Frame(self.root, bg='#1e1e2d')
        form_frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Username Field
        tk.Label(
            form_frame, 
            text="Username", 
            bg='#1e1e2d',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.username_entry = ttk.Entry(
            form_frame, 
            style='Custom.TEntry'
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
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
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        
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
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Gender Field
        tk.Label(
            form_frame, 
            text="Gender", 
            bg='#1e1e2d',
            fg='white'
        ).pack(anchor=tk.W)
        
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = tk.Frame(form_frame, bg='#1e1e2d')
        gender_frame.pack(fill=tk.X)
        
        tk.Radiobutton(
            gender_frame,
            text="Male",
            variable=self.gender_var,
            value="Male",
            bg='#1e1e2d',
            fg='white',
            selectcolor='#25253b'
        ).pack(side=tk.LEFT)
        
        tk.Radiobutton(
            gender_frame,
            text="Female",
            variable=self.gender_var,
            value="Female",
            bg='#1e1e2d',
            fg='white',
            selectcolor='#25253b'
        ).pack(side=tk.LEFT, padx=10)
        
        # Register Button
        register_btn = tk.Button(
            form_frame,
            text="Register",
            command=self.attempt_register,
            bg='#3a3a5c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        register_btn.pack(fill=tk.X, pady=(20, 10))
        
        # Login Link
        login_frame = tk.Frame(self.root, bg='#1e1e2d')
        login_frame.pack()
        
        tk.Label(
            login_frame,
            text="Already have an account?",
            bg='#1e1e2d',
            fg='white'
        ).pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text="Login here",
            fg='#4a90e2',
            bg='#1e1e2d',
            cursor="hand2"
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.switch_to_login())
        
    def attempt_register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        gender = self.gender_var.get()
        
        if all([username, email, password]):
            # Simpan data register (bisa ke database)
            user_data = {
                'username': username,
                'email': email,
                'password': password,  # Note: Harus di-hash di production
                'gender': gender
            }
            
            self.on_register_success(user_data)
        else:
            messagebox.showerror("Error", "Please fill all fields")
            
    def show(self):
        self.root.deiconify()
        
    def hide(self):
        self.root.withdraw()
        
    def run(self):
        self.root.mainloop()