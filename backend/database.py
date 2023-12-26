import sqlite3

def get_db_connection():
    conn = sqlite3.connect('orders.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_db():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
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
        conn.commit()
        print("Database and tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def insert_user_into_db(conn, user_data):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, first_name, last_name) VALUES (?, ?, ?)
    ''', (user_data.username, user_data.first_name, user_data.last_name))
    conn.commit()