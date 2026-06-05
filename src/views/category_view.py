import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import Database

class CategoryView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()
        self.ensure_table_exists()
        self.build_ui()
        self.load_data()
        
    def ensure_table_exists(self):
        try:
            query = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Categories' and xtype='U')
            BEGIN
                CREATE TABLE Categories (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    name NVARCHAR(100) NOT NULL UNIQUE
                )
                INSERT INTO Categories (name) VALUES (N'Coffee'), (N'Tea'), (N'Snacks')
            END
            """
            self.db.execute_query(query)
        except Exception as e:
            print("Lỗi tạo bảng Categories:", e)

    def build_ui(self):
        form_frame = ttk.LabelFrame(self, text="Thông tin danh mục")
        form_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Tên danh mục:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.name_var = ttk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        self.id_var = ttk.StringVar()
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Thêm Mới", bootstyle="success", command=self.add_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cập Nhật", bootstyle="warning", command=self.update_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Xóa", bootstyle="danger", command=self.delete_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Làm Mới Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=5)
        
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        columns = ("id", "name")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID", anchor=CENTER)
        self.tree.heading("name", text="Tên danh mục", anchor=W)
        
        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("name", width=300, anchor=W)
        
        self.tree.bind("<Double-1>", self.on_select)
        self.tree.pack(fill=BOTH, expand=YES, side=LEFT)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        items = self.db.fetch_data("SELECT * FROM Categories ORDER BY id ASC")
        for item in items:
            self.tree.insert("", "end", values=(item['id'], item['name']))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected[0])['values'][0]
        
        items = self.db.fetch_data("SELECT * FROM Categories WHERE id=?", (item_id,))
        if items:
            item = items[0]
            self.id_var.set(item['id'])
            self.name_var.set(item['name'])

    def clear_form(self):
        self.id_var.set("")
        self.name_var.set("")

    def add_item(self):
        name = self.name_var.get()
        
        if not name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên danh mục!")
            return
            
        try:
            self.db.execute_query("INSERT INTO Categories (name) VALUES (?)", (name,))
            messagebox.showinfo("Thành công", "Đã thêm danh mục mới!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", "Có thể danh mục đã tồn tại. Chi tiết lỗi:\n" + str(e))

    def update_item(self):
        item_id = self.id_var.get()
        if not item_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn danh mục để sửa!")
            return
            
        name = self.name_var.get()
        
        try:
            self.db.execute_query("UPDATE Categories SET name=? WHERE id=?", (name, item_id))
            messagebox.showinfo("Thành công", "Đã cập nhật danh mục!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_item(self):
        item_id = self.id_var.get()
        if not item_id: return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa danh mục này?"):
            try:
                self.db.execute_query("DELETE FROM Categories WHERE id=?", (item_id,))
                messagebox.showinfo("Thành công", "Đã xóa danh mục!")
                self.clear_form()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", "Không thể xóa do ràng buộc dữ liệu hoặc lỗi:\n" + str(e))
