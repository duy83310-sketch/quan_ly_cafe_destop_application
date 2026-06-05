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
        # Tạo hiệu ứng nền (background frame)
        bg_frame = ttk.Frame(self, bootstyle="light")
        bg_frame.pack(fill=BOTH, expand=YES)
        
        container = ttk.Frame(bg_frame, padding=40, borderwidth=1, relief="solid", bootstyle="default")
        container.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Hiển thị logo nếu có
        try:
            from PIL import Image, ImageTk
            import os
            if os.path.exists('logo.png'):
                img = Image.open('logo.png')
                img.thumbnail((120, 120))
                self.logo_img = ImageTk.PhotoImage(img)
                ttk.Label(container, image=self.logo_img).pack(pady=(0, 15))
        except Exception:
            pass

        title_lbl = ttk.Label(container, text="TLU Café", font=("Helvetica", 28, "bold"), bootstyle="primary")
        title_lbl.pack(pady=(0, 5))
        
        sub_lbl = ttk.Label(container, text="QUẢN LÝ CỬA HÀNG", font=("Helvetica", 12, "bold"), bootstyle="secondary")
        sub_lbl.pack(pady=(0, 25))
        
        ttk.Label(container, text="Tên đăng nhập", font=("Helvetica", 10, "bold")).pack(anchor=W)
        self.username_var = ttk.StringVar()
        user_entry = ttk.Entry(container, textvariable=self.username_var, width=35, font=("Helvetica", 11))
        user_entry.pack(pady=(5, 15), ipady=6)
        
        ttk.Label(container, text="Mật khẩu", font=("Helvetica", 10, "bold")).pack(anchor=W)
        self.password_var = ttk.StringVar()
        pass_entry = ttk.Entry(container, textvariable=self.password_var, width=35, show="*", font=("Helvetica", 11))
        pass_entry.pack(pady=(5, 25), ipady=6)
        
        login_btn = ttk.Button(container, text="ĐĂNG NHẬP", bootstyle="primary", command=self.handle_login, width=35)
        
        # Hover cho nút Đăng Nhập
        def on_enter_login(e):
            login_btn.configure(bootstyle="danger")
        def on_leave_login(e):
            login_btn.configure(bootstyle="primary")
        login_btn.bind("<Enter>", on_enter_login)
        login_btn.bind("<Leave>", on_leave_login)
        
        login_btn.pack(ipady=8)
        
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
