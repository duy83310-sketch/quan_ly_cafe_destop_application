import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import Database

class AccountView(ttk.Frame):
    def __init__(self, master, user_info):
        super().__init__(master)
        self.db = Database()
        self.user_info = user_info
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        form_frame = ttk.LabelFrame(self, text="Thông tin tài khoản")
        form_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.username_var = ttk.StringVar()
        ttk.Entry(form_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        ttk.Label(form_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.password_var = ttk.StringVar()
        ttk.Entry(form_frame, textvariable=self.password_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky=W)
        
        ttk.Label(form_frame, text="Vai trò:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.role_var = ttk.StringVar()
        role_cb = ttk.Combobox(form_frame, textvariable=self.role_var, values=["Admin", "Staff"], state="readonly", width=28)
        role_cb.grid(row=2, column=1, padx=5, pady=5, sticky=W)
        role_cb.current(1)
        
        self.id_var = ttk.StringVar()
        self.current_role_var = ttk.StringVar()
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Thêm Mới", bootstyle="success", command=self.add_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cập Nhật", bootstyle="warning", command=self.update_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Xóa", bootstyle="danger", command=self.delete_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Làm Mới Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=5)
        
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        columns = ("id", "username", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID", anchor=CENTER)
        self.tree.heading("username", text="Tên đăng nhập", anchor=W)
        self.tree.heading("role", text="Vai trò", anchor=CENTER)
        
        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("username", width=200, anchor=W)
        self.tree.column("role", width=100, anchor=CENTER)
        
        self.tree.bind("<Double-1>", self.on_select)
        self.tree.pack(fill=BOTH, expand=YES, side=LEFT)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        items = self.db.fetch_data("SELECT id, username, role FROM Users ORDER BY id ASC")
        for item in items:
            self.tree.insert("", "end", values=(item['id'], item['username'], item['role']))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected[0])['values'][0]
        
        items = self.db.fetch_data("SELECT * FROM Users WHERE id=?", (item_id,))
        if items:
            item = items[0]
            self.id_var.set(item['id'])
            self.username_var.set(item['username'])
            self.password_var.set(item['password'])
            self.role_var.set(item['role'])
            self.current_role_var.set(item['role'])

    def clear_form(self):
        self.id_var.set("")
        self.username_var.set("")
        self.password_var.set("")
        self.role_var.set("Staff")
        self.current_role_var.set("")

    def add_item(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        role = self.role_var.get()
        
        if not username or not password or not role:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        if len(password) < 6:
            messagebox.showwarning("Lỗi", "Mật khẩu phải có độ dài từ 6 kí tự trở lên!")
            return
            
        try:
            self.db.execute_query("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            messagebox.showinfo("Thành công", "Đã thêm tài khoản mới!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", "Có thể tên đăng nhập đã tồn tại. Chi tiết lỗi:\n" + str(e))

    def update_item(self):
        item_id = self.id_var.get()
        if not item_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn tài khoản để sửa!")
            return
            
        item_id = int(item_id)
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        role = self.role_var.get()
        old_role = self.current_role_var.get()
        
        if not username or not password or not role:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        if len(password) < 6:
            messagebox.showwarning("Lỗi", "Mật khẩu phải có độ dài từ 6 kí tự trở lên!")
            return
            
        if item_id == self.user_info['id'] and role != old_role:
            messagebox.showwarning("Lỗi", "Bạn không thể tự thay đổi quyền của chính mình!")
            self.role_var.set(old_role)
            return
            
        if old_role == 'Admin' and role != 'Admin':
            admins = self.db.fetch_data("SELECT id FROM Users WHERE role='Admin'")
            if len(admins) <= 1:
                messagebox.showwarning("Lỗi", "Hệ thống phải có ít nhất 1 tài khoản Admin!")
                self.role_var.set(old_role)
                return
                
        try:
            self.db.execute_query("UPDATE Users SET username=?, password=?, role=? WHERE id=?", (username, password, role, item_id))
            messagebox.showinfo("Thành công", "Đã cập nhật tài khoản!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", "Chi tiết lỗi:\n" + str(e))

    def delete_item(self):
        item_id = self.id_var.get()
        if not item_id: return
        
        item_id = int(item_id)
        
        if item_id == self.user_info['id']:
            messagebox.showwarning("Lỗi", "Bạn không thể xóa chính mình!")
            return
            
        old_role = self.current_role_var.get()
        
        if old_role == 'Admin':
            admins = self.db.fetch_data("SELECT id FROM Users WHERE role='Admin'")
            if len(admins) <= 1:
                messagebox.showwarning("Lỗi", "Hệ thống phải có ít nhất 1 tài khoản Admin!")
                return
                
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tài khoản này?"):
            try:
                self.db.execute_query("DELETE FROM Users WHERE id=?", (item_id,))
                messagebox.showinfo("Thành công", "Đã xóa tài khoản!")
                self.clear_form()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", "Không thể xóa do ràng buộc dữ liệu hoặc lỗi:\n" + str(e))
