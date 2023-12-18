import sqlite3

def get_db_connection():
    conn = sqlite3.connect('orders.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            );
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                vm_name TEXT NOT NULL,
                rg_name TEXT NOT NULL,
                location TEXT NOT NULL,
                user_id INTEGER,
                recipient_id INTEGER,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (recipient_id) REFERENCES users(id)
            );
        ''')