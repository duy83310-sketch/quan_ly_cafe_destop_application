import pyodbc
import sys
import codecs

# Fix print encoding
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def setup_database():
    server = 'NGUYENDUCJUY'
    master_conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE=master;'
        f'Trusted_Connection=yes;'
    )
    
    try:
        conn = pyodbc.connect(master_conn_str, autocommit=True)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sys.databases WHERE name = N'CafeTLU'")
        if not cursor.fetchone():
            print("Creating database CafeTLU...")
            cursor.execute("CREATE DATABASE CafeTLU")
        else:
            print("Database CafeTLU already exists.")
            
        conn.close()
        
        cafe_conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE=CafeTLU;'
            f'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(cafe_conn_str)
        cursor = conn.cursor()
        
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' and xtype='U')
        CREATE TABLE Users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) CHECK (role IN ('Admin', 'Staff')) NOT NULL
        )
        """)
        
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Categories' and xtype='U')
        CREATE TABLE Categories (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL UNIQUE
        )
        """)
        
        try:
            cursor.execute("INSERT INTO Categories (name) VALUES (N'Coffee'), (N'Tea'), (N'Snacks')")
        except:
            pass

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Menu' and xtype='U')
        CREATE TABLE Menu (
            id INT IDENTITY(1,1) PRIMARY KEY,
            item_name NVARCHAR(100) NOT NULL,
            category NVARCHAR(50) NOT NULL,
            price DECIMAL(18, 2) NOT NULL,
            status NVARCHAR(20) DEFAULT N'Đang bán',
            image_path NVARCHAR(255) NULL
        )
        """)
        
        try:
            cursor.execute("ALTER TABLE Menu ADD image_path NVARCHAR(255) NULL")
        except:
            pass

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Orders' and xtype='U')
        CREATE TABLE Orders (
            id INT IDENTITY(1,1) PRIMARY KEY,
            user_id INT,
            total_amount DECIMAL(18, 2) NOT NULL,
            order_date DATETIME DEFAULT GETDATE(),
            status NVARCHAR(30) CHECK (status IN (N'Đang xử lý', N'Đã hoàn thành')) DEFAULT N'Đang xử lý',
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
        """)
        
        try:
            cursor.execute("ALTER TABLE Orders ADD user_id INT FOREIGN KEY REFERENCES Users(id)")
        except:
            pass
        
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='OrderDetails' and xtype='U')
        CREATE TABLE OrderDetails (
            order_id INT,
            menu_id INT,
            quantity INT NOT NULL,
            PRIMARY KEY (order_id, menu_id),
            FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
            FOREIGN KEY (menu_id) REFERENCES Menu(id)
        )
        """)
        
        try:
            cursor.execute("INSERT INTO Users (username, password, role) VALUES ('admin', '123456', 'Admin')")
            cursor.execute("INSERT INTO Users (username, password, role) VALUES ('staff1', '123456', 'Staff')")
            
            cursor.execute("INSERT INTO Menu (item_name, category, price, status, image_path) VALUES (N'Cà phê đen', N'Coffee', 25000, N'Đang bán', 'https://lh3.googleusercontent.com/aida-public/AB6AXuAEebLilQbfSit0Ad3EQJ8csvU1UROTnNn4fermUihwL0EMuU_7la6uIUYWD29STVg1NcPciHhiQZ7DvaLRTgbWCxCzAfHIgxAEvB6GU_elfCIEAHiF5IGftgF6KIwA-2tg8sKelrEzNOaDYED6IHAW4ZYjMWKV6OIpe5Y8X6WpTiENaRvHifkYVkSFevCwSFcTk6i_fUksWF_yPlxuLssBIHk1bHnZ4a1Dc_PP0zOceXaC61NumaydM7LtYt96wvbIvJj57pmc3zo')")
            cursor.execute("INSERT INTO Menu (item_name, category, price, status, image_path) VALUES (N'Trà đào cam sả', N'Tea', 35000, N'Đang bán', 'https://lh3.googleusercontent.com/aida-public/AB6AXuCyWHLlFS_OZ8AZB9_H5E5rSgcCYSDarQxrPHahE3FnztziX3Pwgy1oZ9tq0iyZtJBThyMXqLD3wK1Zj-TDBvenS3-e6YCWjJXHbpn1vf0wv_hwE14r6risvLCSCk7l4cievkR9Z4ZlQYHjKUln3NeZOIFuS8yjsD-ojwRhFXJlxEdenJiimKSczRHe0KZHD9kGvI4BlMKxuNc5JhtVSp6vQ5SCDMJTIEjTAC3o0jeBIc5U3Pe15_0rgG4fJGvfWgtD-vJdbN7EzeE')")
        except:
            pass
            
        conn.commit()
        conn.close()
        print("Database setup completed successfully.")
        
    except Exception as e:
        print(f"Database setup error: {e}")

if __name__ == '__main__':
    setup_database()
