import tkinter as tk
from tkinter import messagebox
from .dashboard import Dashboard

class AuthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_login()
        
    def setup_login(self):
        # Hapus widget sebelumnya jika ada
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("RAPTOR CHAT - Login")
        
        # Header
        tk.Label(self.root, text="RAPTOR CHAT", font=('Arial', 24), 
                bg='#f5f5f5').pack(pady=30)
        
        # Login Form
        form_frame = tk.Frame(self.root, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Email", bg='#f5f5f5').grid(row=0, sticky='w')
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=1, pady=5)
        
        tk.Label(form_frame, text="Password", bg='#f5f5f5').grid(row=2, sticky='w')
        self.password_entry = tk.Entry(form_frame, width=30, show='*')
        self.password_entry.grid(row=3, pady=5)
        
        # Login Button
        tk.Button(form_frame, text="Login", command=self.login,
                 bg='#4a90e2', fg='white').grid(row=4, pady=20)
        
        # Register Link
        tk.Button(form_frame, text="Register", command=self.show_register,
                 bg='#f5f5f5', fg='#4a90e2', relief=tk.FLAT).grid(row=5)
    
    def show_register(self):
        # Hapus widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("RAPTOR CHAT - Register")
        
        self.entries = {}  # Dictionary untuk menyimpan entry fields
        
        # Header
        tk.Label(self.root, text="RAPTOR CHAT", font=('Arial', 24), 
                bg='#f5f5f5').pack(pady=30)
        
        # Register Form Frame
        form_frame = tk.Frame(self.root, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Field Register
        fields = [
            ("Username", False),
            ("Email", False),
            ("Password", True),
            ("Confirm Password", True)
        ]
        
        for i, (label, is_password) in enumerate(fields):
            tk.Label(form_frame, text=label, bg='#f5f5f5').grid(row=i*2, sticky='w')
            entry = tk.Entry(form_frame, width=30, show='*' if is_password else None)
            entry.grid(row=i*2+1, pady=5, padx=10)
            self.entries[label] = entry
        
        # Register Button
        tk.Button(form_frame, text="Register", command=self.register,
                 bg='#4a90e2', fg='white').grid(row=8, pady=20)
        
        # Back to Login
        tk.Button(form_frame, text="Back to Login", command=self.setup_login,
                 bg='#f5f5f5', fg='#4a90e2', relief=tk.FLAT).grid(row=9)
    
    def register(self):
        try:
            # Validasi input
            if not all(entry.get() for entry in self.entries.values()):
                messagebox.showerror("Error", "All fields are required!")
                return
                
            if self.entries["Password"].get() != self.entries["Confirm Password"].get():
                messagebox.showerror("Error", "Passwords don't match!")
                return
                
            # Dapatkan username
            username = self.entries["Username"].get()
            
            # Sembunyikan window auth
            self.root.withdraw()
            
            # Tampilkan dashboard
            dashboard = Dashboard(username)
            dashboard.show()
            
            # Tutup window auth saat dashboard ditutup
            self.root.wait_window(dashboard.root)
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
            self.root.deiconify()
    
    def on_close(self):
        self.root.destroy()
