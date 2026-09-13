import sqlite3

class UserService:
    def __init__(self, db_path="phonebook.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    is_locked BOOLEAN DEFAULT 0
                )
            """)
            conn.commit()

    def get_all_users(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, email, role, is_locked FROM users")
            rows = cursor.fetchall()
            return [
                {
                    "user_id": r[0],
                    "username": r[1],
                    "email": r[2],
                    "role": r[3],
                    "is_locked": bool(r[4])
                }
                for r in rows
            ]

    def get_total_users(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                return cursor.fetchone()[0]
        except Exception:
            return 0

    def add_user(self, username, email, password, role="user"):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                    (username, email, password, role)
                )
                conn.commit()
                return True
        except Exception:
            return False

    def update_user(self, user_id, username, email):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET username = ?, email = ? WHERE user_id = ?",
                    (username, email, user_id)
                )
                conn.commit()
                return True
        except Exception:
            return False

    def delete_user(self, user_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                conn.commit()
                return True
        except Exception:
            return False

    def lock_user(self, user_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET is_locked = 1 WHERE user_id = ?", (user_id,))
                conn.commit()
                return True
        except Exception:
            return False

    def unlock_user(self, user_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET is_locked = 0 WHERE user_id = ?", (user_id,))
                conn.commit()
                return True
        except Exception:
            return False

    # Alias để hỗ trợ tương thích với các bài test hoặc giao diện gọi hàm tên khác
    lock_account = lock_user
    unlock_account = unlock_user