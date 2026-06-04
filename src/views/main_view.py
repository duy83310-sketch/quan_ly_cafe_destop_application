import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.pos_view import POSView
from views.menu_view import MenuView
from views.report_view import DashboardView
from views.category_view import CategoryView

class MainView(ttk.Frame):
    def __init__(self, master, user_info, logout_callback):
        super().__init__(master)
        self.master = master
        self.user_info = user_info
        self.logout_callback = logout_callback
        self.pack(fill=BOTH, expand=YES)
        self.frames = {}
        self.build_ui()
        
    def build_ui(self):
        # Sidebar Frame
        self.sidebar = ttk.Frame(self, bootstyle="dark", width=250)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = ttk.Frame(self.sidebar, bootstyle="dark")
        title_frame.pack(fill=X, pady=20, padx=10)
        
        # Hiển thị ảnh logo nếu có
        try:
            from PIL import Image, ImageTk
            import os
            if os.path.exists('logo.png'):
                img = Image.open('logo.png')
                img = img.resize((50, 50))
                self.logo_img = ImageTk.PhotoImage(img)
                ttk.Label(title_frame, image=self.logo_img, bootstyle="inverse-dark").pack(anchor=W, pady=(0, 10))
        except Exception:
            pass

        ttk.Label(title_frame, text="☕ TLU Café", font=("Helvetica", 20, "bold"), bootstyle="inverse-dark").pack(anchor=W)
        ttk.Label(title_frame, text="MANAGEMENT PORTAL", font=("Helvetica", 10), bootstyle="inverse-dark").pack(anchor=W)
        
        # Current User Info
        user_frame = ttk.Frame(self.sidebar, bootstyle="dark")
        user_frame.pack(fill=X, padx=10, pady=(0, 20))
        ttk.Label(user_frame, text=f"Xin chào, {self.user_info['username']}", font=("Helvetica", 12), bootstyle="inverse-dark").pack(anchor=W)
        ttk.Label(user_frame, text=f"Role: {self.user_info['role']}", font=("Helvetica", 10, "italic"), bootstyle="inverse-dark").pack(anchor=W)
        
        # Main Content Frame
        self.content = ttk.Frame(self)
        self.content.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        ttk.Separator(self.sidebar, orient=HORIZONTAL, bootstyle="secondary").pack(fill=X, padx=10, pady=10)
        
        # Nav buttons
        if self.user_info['role'] == 'Admin':
            self.add_nav_btn("📊 Dashboard Overview", lambda: self.show_frame(DashboardView))
            self.add_nav_btn("🍔 Menu Management", lambda: self.show_frame(MenuView))
            self.add_nav_btn("📂 Category Management", lambda: self.show_frame(CategoryView))
            self.add_nav_btn("🛒 POS (Bán Hàng)", lambda: self.show_frame(POSView, self.user_info))
        else:
            self.add_nav_btn("🛒 POS (Bán Hàng)", lambda: self.show_frame(POSView, self.user_info))
            
        # Logout button
        logout_btn = ttk.Button(self.sidebar, text="🚪 Logout", bootstyle="danger", command=self.logout)
        logout_btn.pack(side=BOTTOM, fill=X, pady=20, padx=10)
        
        # Show default frame
        if self.user_info['role'] == 'Admin':
            self.show_frame(DashboardView)
        else:
            self.show_frame(POSView, self.user_info)

    def add_nav_btn(self, text, command):
        btn = ttk.Button(self.sidebar, text=text, bootstyle="dark-outline", command=command)
        btn.pack(fill=X, padx=10, pady=5)
        
    def show_frame(self, FrameClass, *args):
        for widget in self.content.winfo_children():
            widget.pack_forget()
            
        if FrameClass not in self.frames:
            self.frames[FrameClass] = FrameClass(self.content, *args) if args else FrameClass(self.content)
            
        self.frames[FrameClass].pack(fill=BOTH, expand=YES)
        
        if hasattr(self.frames[FrameClass], 'load_data'):
            self.frames[FrameClass].load_data()

    def logout(self):
        self.logout_callback()
