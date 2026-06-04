import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import Database
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class DashboardView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()
        self.build_ui()
        
    def build_ui(self):
        self.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=X, pady=(0, 20))
        ttk.Label(header_frame, text="Dashboard Overview", font=("Helvetica", 24, "bold")).pack(side=LEFT)
        ttk.Button(header_frame, text="Làm Mới", bootstyle="info", command=self.load_data).pack(side=RIGHT)
        
        kpi_frame = ttk.Frame(self)
        kpi_frame.pack(fill=X, pady=(0, 20))
        
        self.rev_card = self.create_kpi_card(kpi_frame, "TOTAL REVENUE (NĂM NAY)", "0 ₫")
        self.rev_card.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))
        
        self.ord_card = self.create_kpi_card(kpi_frame, "TOTAL ORDERS", "0")
        self.ord_card.pack(side=LEFT, fill=BOTH, expand=YES, padx=(10, 10))
        
        charts_frame = ttk.Frame(self)
        charts_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))
        
        self.fig = Figure(figsize=(10, 3.5), dpi=100) # Làm nhỏ biểu đồ lại cho gọn
        self.ax_bar = self.fig.add_subplot(121) 
        self.ax_pie = self.fig.add_subplot(122) 
        self.fig.tight_layout() # Bỏ pad=3.0 để biểu đồ tự động fit vừa khung
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        
        ttk.Label(self, text="Recent Transactions", font=("Helvetica", 16, "bold")).pack(anchor=W, pady=(10, 5))
        ttk.Label(self, text="* Mẹo: Click đúp vào một giao dịch để xem chi tiết các món đã mua", font=("Helvetica", 9, "italic")).pack(anchor=W, pady=(0, 5))
        
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES)
        
        columns = ("id", "date", "amount", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        self.tree.heading("id", text="ORDER ID")
        self.tree.heading("date", text="DATE")
        self.tree.heading("amount", text="AMOUNT")
        self.tree.heading("status", text="STATUS")
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.tree.bind("<Double-1>", self.show_order_details)

    def show_order_details(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        item = self.tree.item(selected[0])
        order_str = item['values'][0] # VD: "#ORD-3"
        order_id = int(str(order_str).replace("#ORD-", ""))
        
        try:
            details = self.db.fetch_data("""
                SELECT m.item_name, od.quantity, m.price
                FROM OrderDetails od
                JOIN Menu m ON od.menu_id = m.id
                WHERE od.order_id = ?
            """, (order_id,))
            
            from tkinter import messagebox
            if not details:
                messagebox.showinfo("Chi tiết đơn hàng", f"Không có thông tin chi tiết cho {order_str}")
                return
                
            msg = f"CHI TIẾT MÓN ĂN - {order_str}\n"
            msg += "-" * 40 + "\n"
            for d in details:
                msg += f"• {d['item_name']} (x{d['quantity']}): {int(d['price'] * d['quantity']):,} đ\n"
            msg += "-" * 40 + "\n"
            msg += f"TỔNG CỘNG: {item['values'][2]}"
            
            messagebox.showinfo("Chi tiết đơn hàng", msg)
        except Exception as e:
            print("Lỗi xem chi tiết:", e)

    def create_kpi_card(self, parent, title, value):
        frame = ttk.Frame(parent, bootstyle="secondary", padding=15)
        ttk.Label(frame, text=title, font=("Helvetica", 10, "bold"), bootstyle="inverse-secondary").pack(anchor=W)
        val_lbl = ttk.Label(frame, text=value, font=("Helvetica", 24, "bold"), bootstyle="inverse-secondary")
        val_lbl.pack(anchor=W, pady=(5, 0))
        frame.val_lbl = val_lbl
        return frame

    def load_data(self):
        try:
            current_year = datetime.now().year
            
            # 1. KPIs
            orders = self.db.fetch_data("SELECT id, total_amount, status, order_date FROM Orders WHERE status=N'Đã hoàn thành'")
            total_rev_year = sum(o['total_amount'] for o in orders if o['order_date'].year == current_year)
            total_count = len(orders)
            
            self.rev_card.val_lbl.config(text=f"{int(total_rev_year):,} ₫")
            self.ord_card.val_lbl.config(text=f"{total_count}")
            
            # 2. Bar Chart (Monthly Revenue)
            monthly_query = f"""
            SELECT MONTH(order_date) as month, SUM(total_amount) as revenue 
            FROM Orders 
            WHERE YEAR(order_date) = {current_year} AND status=N'Đã hoàn thành'
            GROUP BY MONTH(order_date)
            """
            monthly_data = self.db.fetch_data(monthly_query)
            
            # Khởi tạo 12 tháng với doanh thu 0
            months = [f"T{i}" for i in range(1, 13)]
            revenues = [0] * 12
            for m in monthly_data:
                revenues[m['month'] - 1] = m['revenue']
            
            self.ax_bar.clear()
            # Sử dụng màu xanh dương đậm của TLU
            self.ax_bar.bar(months, revenues, color='#00205B') 
            self.ax_bar.set_title(f"Doanh thu theo tháng ({current_year})", fontsize=11)
            self.ax_bar.tick_params(axis='x', rotation=45, labelsize=9)
            self.ax_bar.tick_params(axis='y', labelsize=9)
            
            # 3. Pie Chart (Best Selling)
            top_query = """
            SELECT TOP 5 m.item_name, SUM(od.quantity) as total_qty
            FROM OrderDetails od
            JOIN Menu m ON od.menu_id = m.id
            JOIN Orders o ON od.order_id = o.id
            WHERE o.status = N'Đã hoàn thành'
            GROUP BY m.item_name
            ORDER BY total_qty DESC
            """
            top_data = self.db.fetch_data(top_query)
            
            item_names = [item['item_name'] for item in top_data]
            item_qtys = [item['total_qty'] for item in top_data]
            
            self.ax_pie.clear()
            if item_qtys:
                # Sử dụng dải màu đỏ/xanh chuẩn logo TLU
                tlu_colors = ['#00205B', '#D11124', '#33508A', '#E04A55', '#6680B3']
                self.ax_pie.pie(item_qtys, labels=item_names, autopct='%1.1f%%', startangle=90, 
                                colors=tlu_colors[:len(item_qtys)], textprops={'fontsize': 9})
                self.ax_pie.set_title("Món Bán Chạy Nhất", fontsize=11)
            else:
                self.ax_pie.text(0.5, 0.5, "Chưa có dữ liệu món", ha='center')
                
            self.fig.tight_layout()
            self.canvas.draw()
            
            # 4. Recent Transactions
            for row in self.tree.get_children():
                self.tree.delete(row)
                
            recent_orders = self.db.fetch_data("SELECT TOP 10 * FROM Orders ORDER BY order_date DESC")
            for order in recent_orders:
                self.tree.insert("", "end", values=(f"#ORD-{order['id']}", order['order_date'].strftime('%Y-%m-%d %H:%M'), f"{int(order['total_amount']):,} ₫", order['status']))
                
        except Exception as e:
            print("Dashboard load error:", e)
