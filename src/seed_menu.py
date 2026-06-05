import sys
import codecs
from database import Database

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def seed_menu():
    db = Database()
    
    categories = ['Coffee', 'Tea', 'Juice/Smoothie', 'Snacks']
    for cat in categories:
        try:
            db.execute_query("INSERT INTO Categories (name) VALUES (?)", (cat,))
        except Exception:
            pass

    items = [
        ('Cà phê sữa đá', 'Coffee', 29000, 'Đang bán', 'https://images.unsplash.com/photo-1517701550927-30cfcb64ac45?w=500&q=80'),
        ('Bạc xỉu', 'Coffee', 35000, 'Đang bán', 'https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?w=500&q=80'),
        ('Espresso', 'Coffee', 25000, 'Đang bán', 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=500&q=80'),
        ('Cappuccino', 'Coffee', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=500&q=80'),
        ('Latte Macchiato', 'Coffee', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1561882468-9110e03e0f78?w=500&q=80'),
        ('Cold Brew', 'Coffee', 50000, 'Đang bán', 'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=500&q=80'),
        
        ('Trà đào cam sả', 'Tea', 40000, 'Đang bán', 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500&q=80'),
        ('Trà vải nhiệt đới', 'Tea', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1626844131082-256783844137?w=500&q=80'),
        ('Matcha Latte', 'Tea', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1515823662415-e4148e1c67d4?w=500&q=80'),
        ('Trà ô long hạt sen', 'Tea', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1576092762791-dd9e2220abd1?w=500&q=80'),
        
        ('Nước ép cam tươi', 'Juice/Smoothie', 40000, 'Đang bán', 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500&q=80'),
        ('Sinh tố bơ', 'Juice/Smoothie', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=500&q=80'),
        ('Sinh tố dâu tây', 'Juice/Smoothie', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=500&q=80'),
        
        ('Bánh Sừng Bò (Croissant)', 'Snacks', 30000, 'Đang bán', 'https://images.unsplash.com/photo-1555507036-ab1f40ce88f7?w=500&q=80'),
        ('Bánh Tiramisu', 'Snacks', 45000, 'Đang bán', 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=500&q=80'),
        ('Bánh Phô mai nướng', 'Snacks', 40000, 'Đang bán', 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500&q=80'),
    ]

    count = 0
    for item in items:
        try:
            existing = db.fetch_data("SELECT id FROM Menu WHERE item_name=?", (item[0],))
            if not existing:
                db.execute_query(
                    "INSERT INTO Menu (item_name, category, price, status, image_path) VALUES (?, ?, ?, ?, ?)",
                    item
                )
                count += 1
        except Exception as e:
            print(f"Lỗi khi thêm {item[0]}: {e}")

    print(f"Thêm thành công {count} món nước mới vào Menu!")

if __name__ == '__main__':
    seed_menu()
