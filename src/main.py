import ttkbootstrap as ttk
from views.login_view import LoginView
from views.main_view import MainView

class App(ttk.Window):
    def __init__(self):
        super().__init__(title="TLU Café", themename="litera")
        self.geometry("1200x800")
        self.state('zoomed')
        
        # Thiết lập icon ứng dụng (nếu có file logo.png)
        try:
            from PIL import Image, ImageTk
            import os
            if os.path.exists('logo.png'):
                icon = ImageTk.PhotoImage(Image.open('logo.png'))
                self.iconphoto(True, icon)
        except Exception:
            pass
            
        self.show_login()

    def show_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        LoginView(self, self.on_login_success)

    def on_login_success(self, user_info):
        for widget in self.winfo_children():
            widget.destroy()
        MainView(self, user_info, self.show_login)

if __name__ == '__main__':
    app = App()
    app.mainloop()
