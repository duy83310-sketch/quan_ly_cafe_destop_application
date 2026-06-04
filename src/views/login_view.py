import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import Database

class LoginView(ttk.Frame):
    def __init__(self, master, on_success_callback):
        super().__init__(master)
        self.master = master
        self.on_success_callback = on_success_callback
        self.pack(fill=BOTH, expand=YES)
        self.db = Database()
        self.build_ui()
        
    def build_ui(self):
        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        title_lbl = ttk.Label(container, text="TLU Coffee", font=("Helvetica", 32, "bold"), bootstyle="danger")
        title_lbl.pack(pady=(0, 5))
        
        sub_lbl = ttk.Label(container, text="Management Portal", font=("Helvetica", 12))
        sub_lbl.pack(pady=(0, 20))
        
        ttk.Label(container, text="Tên đăng nhập").pack(anchor=W)
        self.username_var = ttk.StringVar()
        user_entry = ttk.Entry(container, textvariable=self.username_var, width=40)
        user_entry.pack(pady=(5, 15), ipady=5)
        
        ttk.Label(container, text="Mật khẩu").pack(anchor=W)
        self.password_var = ttk.StringVar()
        pass_entry = ttk.Entry(container, textvariable=self.password_var, width=40, show="*")
        pass_entry.pack(pady=(5, 20), ipady=5)
        
        login_btn = ttk.Button(container, text="Đăng Nhập", bootstyle="danger", command=self.handle_login, width=38)
        login_btn.pack(ipady=5)
        
    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu")
            return
            
        try:
            users = self.db.fetch_data("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
            if users:
                user = users[0]
                self.on_success_callback(user)
            else:
                messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", str(e))
