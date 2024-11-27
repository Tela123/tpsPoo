import sqlite3

DB_NAME = "auth_system.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Création des tables utilisateurs et permissions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            permission TEXT UNIQUE NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_permissions (
            user_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(permission_id) REFERENCES permissions(id),
            UNIQUE(user_id, permission_id)
        )
        """)

def execute_query(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def fetch_query(query, params=()):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()