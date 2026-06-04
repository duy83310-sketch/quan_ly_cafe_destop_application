import pyodbc

class Database:
    def __init__(self):
        self.server = 'NGUYENDUCJUY'
        self.database = 'CafeTLU'
        self.conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'Trusted_Connection=yes;'
        )
    
    def get_connection(self):
        return pyodbc.connect(self.conn_str)

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        finally:
            conn.close()

    def fetch_data(self, query, params=()):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in result]
        finally:
            conn.close()
