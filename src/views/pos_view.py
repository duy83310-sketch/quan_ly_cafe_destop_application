import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
from database import Database
import os
import urllib.request
from io import BytesIO
import threading

class POSView(ttk.Frame):
    def __init__(self, master, user_info):
        super().__init__(master)
        self.db = Database()
        self.user_info = user_info
        self.cart = []
        self.images_cache = {}
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.right_frame = ttk.Frame(self, width=350, bootstyle="light")
        self.right_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)
        self.right_frame.pack_propagate(False)
        
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(search_frame, text="Tìm món:").pack(side=LEFT, padx=5)
        self.search_var = ttk.StringVar()
        self.search_var = ttk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.load_data())
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=LEFT, fill=X, expand=YES, padx=5)
        
        self.category_var = ttk.StringVar(value="All")
        cats = ["All", "Coffee", "Tea", "Snacks", "Juice/Smoothie"]
        for cat in cats:
            ttk.Radiobutton(search_frame, text=cat, variable=self.category_var, value=cat, bootstyle="danger-toolbutton", command=self.load_data).pack(side=LEFT, padx=2)
            
        self.canvas = ttk.Canvas(self.left_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        ttk.Label(self.right_frame, text="Hóa Đơn Tạm Tính", font=("Helvetica", 16, "bold"), bootstyle="danger").pack(pady=10)
        
        columns = ("name", "qty", "price")
        self.cart_tree = ttk.Treeview(self.right_frame, columns=columns, show="headings", height=15)
        self.cart_tree.heading("name", text="Món")
        self.cart_tree.heading("qty", text="SL")
        self.cart_tree.heading("price", text="Thành tiền")
        self.cart_tree.column("name", width=140)
        self.cart_tree.column("qty", width=40, anchor=CENTER)
        self.cart_tree.column("price", width=110, anchor=E)
        self.cart_tree.pack(fill=BOTH, expand=YES, pady=5)
        
        self.cart_tree.bind("<Double-1>", self.edit_cart_item)
        ttk.Label(self.right_frame, text="* Mẹo: Click đúp vào món để sửa SL/Xóa", font=("Helvetica", 9, "italic")).pack(anchor=W, padx=5)
        
        self.total_lbl = ttk.Label(self.right_frame, text="Tổng cộng: 0 ₫", font=("Helvetica", 16, "bold"), bootstyle="danger")
        self.total_lbl.pack(pady=10, anchor=E)
        
        btn_frame = ttk.Frame(self.right_frame)
        btn_frame.pack(fill=X, pady=10)
        ttk.Button(btn_frame, text="Xóa Hết", bootstyle="secondary", command=self.clear_cart).pack(side=LEFT, fill=X, expand=YES, padx=5)
        ttk.Button(btn_frame, text="Thanh Toán", bootstyle="success", command=self.checkout).pack(side=LEFT, fill=X, expand=YES, padx=5)

    def load_data(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        keyword = self.search_var.get()
        cat = self.category_var.get()
        
        query = "SELECT * FROM Menu WHERE status=N'Đang bán'"
        params = []
        if cat != "All":
            query += " AND category=?"
            params.append(cat)
        if keyword:
            query += " AND item_name LIKE ?"
            params.append(f"%{keyword}%")
            
        products = self.db.fetch_data(query, tuple(params))
        
        row, col = 0, 0
        max_cols = 4
        
        for p in products:
            card = ttk.Frame(self.scrollable_frame, borderwidth=1, relief="solid")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            img_path = p.get('image_path')
            
            img_lbl = ttk.Label(card, text="[Loading Image...]", width=15, anchor=CENTER)
            img_lbl.pack(pady=5)
            
            def update_img(photo, lbl=img_lbl):
                if lbl.winfo_exists():
                    lbl.config(image=photo, text="")
                    lbl.image = photo
                    
            img_tk = self.get_product_image(img_path, update_img)
            if img_tk:
                update_img(img_tk)
            
            ttk.Label(card, text=p['item_name'], font=("Helvetica", 12, "bold")).pack()
            ttk.Label(card, text=f"{int(p['price']):,} ₫", font=("Helvetica", 10), bootstyle="danger").pack()
            
            qty_frame = ttk.Frame(card)
            qty_frame.pack(pady=5)
            ttk.Label(qty_frame, text="SL:").pack(side=LEFT, padx=(0, 5))
            qty_var = ttk.IntVar(value=1)
            ttk.Spinbox(qty_frame, from_=1, to=99, textvariable=qty_var, width=5).pack(side=LEFT)
            
            ttk.Button(card, text="Thêm vào giỏ", bootstyle="outline-danger", command=lambda item=p, q=qty_var: self.add_to_cart(item, q.get())).pack(pady=5, fill=X, padx=10)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def get_product_image(self, path, callback=None):
        if not path: return None
        
        cache_key = path
        if not path.startswith('http') and os.path.exists(path):
            try:
                mtime = os.path.getmtime(path)
                cache_key = f"{path}_{mtime}"
            except Exception:
                pass
                
        if cache_key in self.images_cache:
            return self.images_cache[cache_key]
            
        try:
            if path.startswith('http'):
                def download_task():
                    try:
                        req = urllib.request.urlopen(path)
                        img = Image.open(BytesIO(req.read()))
                        img = img.resize((120, 120), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.images_cache[cache_key] = photo
                        if callback:
                            self.after(0, lambda: callback(photo))
                    except Exception:
                        pass
                threading.Thread(target=download_task, daemon=True).start()
                return None
            elif os.path.exists(path):
                img = Image.open(path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                self.images_cache[cache_key] = ImageTk.PhotoImage(img)
                return self.images_cache[cache_key]
        except Exception:
            pass
        return None

    def add_to_cart(self, item, qty=1):
        try:
            qty = int(qty)
            if qty <= 0: return
        except ValueError:
            return

        for i, cart_item in enumerate(self.cart):
            if cart_item['id'] == item['id']:
                self.cart[i]['qty'] += qty
                self.update_cart_ui()
                return
                
        self.cart.append({'id': item['id'], 'name': item['item_name'], 'price': item['price'], 'qty': qty})
        self.update_cart_ui()
        
    def update_cart_ui(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
            
        total = 0
        for item in self.cart:
            row_total = item['price'] * item['qty']
            total += row_total
            self.cart_tree.insert("", "end", values=(item['name'], item['qty'], f"{int(row_total):,} ₫"))
            
        self.total_lbl.config(text=f"Tổng cộng: {int(total):,} ₫")

    def edit_cart_item(self, event):
        selected = self.cart_tree.selection()
        if not selected: return
        
        from tkinter import simpledialog
        
        index = self.cart_tree.index(selected[0])
        item = self.cart[index]
        
        new_qty = simpledialog.askinteger(
            "Sửa giỏ hàng", 
            f"Nhập số lượng mới cho {item['name']}\n(Nhập 0 để xóa món này):", 
            initialvalue=item['qty'], 
            minvalue=0, 
            maxvalue=999,
            parent=self
        )
        
        if new_qty is not None:
            if new_qty == 0:
                self.cart.pop(index)
            else:
                self.cart[index]['qty'] = new_qty
            self.update_cart_ui()

    def clear_cart(self):
        self.cart = []
        self.update_cart_ui()

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Cảnh báo", "Giỏ hàng đang trống!")
            return
            
        total = sum([item['price'] * item['qty'] for item in self.cart])
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            user_id = self.user_info.get('id')
            cursor.execute("INSERT INTO Orders (user_id, total_amount, status) OUTPUT INSERTED.id VALUES (?, ?, N'Đã hoàn thành')", (user_id, total,))
            order_id = cursor.fetchone()[0]
            
            for item in self.cart:
                cursor.execute("INSERT INTO OrderDetails (order_id, menu_id, quantity) VALUES (?, ?, ?)", (order_id, item['id'], item['qty']))
                
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thành công", f"Đã thanh toán thành công!\nMã đơn hàng: {order_id}")
            
            self.print_invoice(order_id, total, self.cart.copy())
            
            self.show_qr_payment(order_id, total)
            
            self.clear_cart()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def print_invoice(self, order_id, total, cart_items):
        from datetime import datetime
        import os
        
        invoice_dir = "HoaDon"
        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)
            
        filename = os.path.join(invoice_dir, f"hoadon_ORD_{order_id}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("="*45 + "\n")
            f.write("                TLU CAFÉ\n")
            f.write("           HÓA ĐƠN THANH TOÁN\n")
            f.write("="*45 + "\n")
            f.write(f"Mã Đơn: ORD-{order_id}\n")
            f.write(f"Ngày: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Thu ngân: {self.user_info.get('username', 'Admin')}\n")
            f.write("-" * 45 + "\n")
            f.write(f"{'Tên món':<22} | {'SL':<4} | {'Thành tiền':>11}\n")
            f.write("-" * 45 + "\n")
            
            for item in cart_items:
                name = item['name'][:21]
                qty = item['qty']
                price = int(item['price'] * qty)
                f.write(f"{name:<22} | {qty:<4} | {price:>11,}\n")
                
            f.write("-" * 45 + "\n")
            f.write(f"TỔNG TIỀN: {int(total):>32,} đ\n")
            f.write("="*45 + "\n")
            f.write("         CẢM ƠN QUÝ KHÁCH!\n")
            f.write("          HẸN GẶP LẠI!\n")
            
        try:
            os.startfile(filename)
        except Exception as e:
            print("Không thể mở file hóa đơn:", e)

    def show_qr_payment(self, order_id, total):
        import urllib.parse
        
        qr_window = ttk.Toplevel(self)
        qr_window.title("Thanh toán mã QR - VietQR")
        qr_window.geometry("400x550")
        qr_window.transient(self.winfo_toplevel())
        qr_window.grab_set()
        
        ttk.Label(qr_window, text="VUI LÒNG QUÉT MÃ ĐỂ THANH TOÁN", font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
        ttk.Label(qr_window, text=f"Số tiền: {int(total):,} đ", font=("Helvetica", 18, "bold"), bootstyle="danger").pack(pady=5)
        
        img_lbl = ttk.Label(qr_window, text="Đang tạo mã QR...", font=("Helvetica", 12))
        img_lbl.pack(pady=10, expand=True)
        
        def fetch_qr():
            try:
                bank_id = "techcombank"
                account_no = "19071713001010"
                account_name = urllib.parse.quote("QUAN CAFE TLU")
                add_info = urllib.parse.quote(f"Thanh toan don {order_id}")
                
                url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={int(total)}&addInfo={add_info}&accountName={account_name}"
                
                req = urllib.request.urlopen(url)
                img = Image.open(BytesIO(req.read()))
                img = img.resize((320, 350), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                if img_lbl.winfo_exists():
                    img_lbl.config(image=photo, text="")
                    img_lbl.image = photo
            except Exception as e:
                if img_lbl.winfo_exists():
                    img_lbl.config(text=f"Lỗi tải mã QR. Vui lòng kiểm tra mạng!\n{e}", bootstyle="danger")
                    
        threading.Thread(target=fetch_qr, daemon=True).start()
        
        ttk.Button(qr_window, text="Xác nhận khách đã thanh toán", bootstyle="success", command=qr_window.destroy).pack(pady=20)
