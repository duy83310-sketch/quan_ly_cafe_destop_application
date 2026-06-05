import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import filedialog
from database import Database

class MenuView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        form_frame = ttk.LabelFrame(self, text="Thông tin món")
        form_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Tên món:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.name_var = ttk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Danh mục:").grid(row=0, column=2, padx=5, pady=5, sticky=E)
        self.cat_var = ttk.StringVar()
        self.cat_cb = ttk.Combobox(form_frame, textvariable=self.cat_var, state="readonly")
        self.cat_cb.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Giá tiền:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.price_var = ttk.StringVar()
        ttk.Entry(form_frame, textvariable=self.price_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Đường dẫn ảnh/URL:").grid(row=1, column=2, padx=5, pady=5, sticky=E)
        self.image_var = ttk.StringVar()
        ttk.Entry(form_frame, textvariable=self.image_var, width=30).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(form_frame, text="Chọn ảnh", command=self.choose_image, bootstyle="info-outline").grid(row=1, column=4, padx=5, pady=5)
        
        self.id_var = ttk.StringVar()
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=5, pady=10)
        ttk.Button(btn_frame, text="Thêm Mới", bootstyle="success", command=self.add_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cập Nhật", bootstyle="warning", command=self.update_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Ngừng Bán (Xóa)", bootstyle="danger", command=self.delete_item).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Làm Mới Form", bootstyle="secondary", command=self.clear_form).pack(side=LEFT, padx=5)
        
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        columns = ("id", "name", "cat", "price", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID", anchor=CENTER)
        self.tree.heading("name", text="Tên món", anchor=W)
        self.tree.heading("cat", text="Danh mục", anchor=W)
        self.tree.heading("price", text="Giá tiền", anchor=E)
        self.tree.heading("status", text="Trạng thái", anchor=CENTER)
        
        self.tree.column("id", width=50, anchor=CENTER)
        self.tree.column("name", width=250, anchor=W)
        self.tree.column("cat", width=150, anchor=W)
        self.tree.column("price", width=100, anchor=E)
        self.tree.column("status", width=100, anchor=CENTER)
        
        self.tree.bind("<Double-1>", self.on_select)
        self.tree.pack(fill=BOTH, expand=YES, side=LEFT)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def choose_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            self.image_var.set(path)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        items = self.db.fetch_data("SELECT * FROM Menu WHERE status != N'Ngừng bán' ORDER BY id ASC")
        for item in items:
            self.tree.insert("", "end", values=(item['id'], item['item_name'], item['category'], f"{int(item['price']):,}", item['status']))
            
        try:
            cats = self.db.fetch_data("SELECT name FROM Categories")
            self.cat_cb['values'] = [c['name'] for c in cats]
        except Exception:
            self.cat_cb['values'] = ["Coffee", "Tea", "Snacks"]

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected[0])['values'][0]
        
        items = self.db.fetch_data("SELECT * FROM Menu WHERE id=?", (item_id,))
        if items:
            item = items[0]
            self.id_var.set(item['id'])
            self.name_var.set(item['item_name'])
            self.cat_var.set(item['category'])
            self.price_var.set(int(item['price']))
            self.image_var.set(item['image_path'] if item['image_path'] else "")

    def clear_form(self):
        self.id_var.set("")
        self.name_var.set("")
        self.cat_var.set("")
        self.price_var.set("")
        self.image_var.set("")

    def add_item(self):
        name = self.name_var.get()
        cat = self.cat_var.get()
        price = self.price_var.get()
        img = self.image_var.get()
        
        if not name or not price:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên và giá!")
            return
            
        try:
            self.db.execute_query("INSERT INTO Menu (item_name, category, price, image_path) VALUES (?, ?, ?, ?)", (name, cat, float(price), img))
            messagebox.showinfo("Thành công", "Đã thêm món mới!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def update_item(self):
        item_id = self.id_var.get()
        if not item_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn món để sửa!")
            return
            
        name = self.name_var.get()
        cat = self.cat_var.get()
        price = self.price_var.get()
        img = self.image_var.get()
        
        try:
            self.db.execute_query("UPDATE Menu SET item_name=?, category=?, price=?, image_path=? WHERE id=?", (name, cat, float(price), img, item_id))
            messagebox.showinfo("Thành công", "Đã cập nhật!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_item(self):
        item_id = self.id_var.get()
        if not item_id: return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn XÓA VĨNH VIỄN món này?"):
            try:
                self.db.execute_query("DELETE FROM Menu WHERE id=?", (item_id,))
                messagebox.showinfo("Thành công", "Đã xóa món khỏi danh sách!")
                self.clear_form()
                self.load_data()
            except Exception as e:
                self.db.execute_query("UPDATE Menu SET status=N'Ngừng bán' WHERE id=?", (item_id,))
                messagebox.showinfo("Thông báo", "Món này đã từng được order nên không thể xóa hoàn toàn khỏi hệ thống để giữ lịch sử doanh thu.\nHệ thống đã chuyển trạng thái sang 'Ngừng bán' và ẩn đi.")
                self.clear_form()
                self.load_data()
