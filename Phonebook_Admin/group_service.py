import sqlite3

class GroupService:
    def __init__(self, db_path="phonebook.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT NOT NULL
                )
            """)
            conn.commit()

    def get_total_groups(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM groups")
            return cursor.fetchone()[0]