import sqlite3
import os

DATABASE = 'profiles.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                height TEXT NOT NULL,
                weight INTEGER NOT NULL,
                caste TEXT NOT NULL,
                religion TEXT NOT NULL,
                mother_tongue TEXT NOT NULL,
                phone TEXT NOT NULL,
                state TEXT NOT NULL,
                city TEXT NOT NULL,
                marital_status TEXT NOT NULL,
                children TEXT NOT NULL,
                num_children INTEGER,
                occupation TEXT NOT NULL,
                education TEXT NOT NULL,
                bio TEXT NOT NULL,
                expectations TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized.")

if __name__ == '__main__':
    init_db()
