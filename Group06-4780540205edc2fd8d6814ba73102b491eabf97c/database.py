"""
database.py

This file handles everything related to the SQLite database:
- connecting to the database file
- creating the 3 tables (User, Groups, Contact) the first time the program runs

We use SQLite because it does not need a separate database server -
it just saves everything into a single file (data/phonebook.db).
"""

import sqlite3
import os
import hashlib

# The database file will be saved inside the "data" folder
DB_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
DB_FILE = os.path.join(DB_FOLDER, "phonebook.db")


def get_connection():
    """Open a connection to the database file (creates the file if it does not exist yet)."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row  # lets us access columns by name, e.g. row["username"]
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def hash_password(plain_password):
    """
    We never store passwords as plain text in the database.
    Instead we store a "hash" (a scrambled version) using SHA-256.
    """
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def create_tables():
    """Create the 3 tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table 1: User (also stores Admin accounts, using the "role" column)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            is_locked INTEGER DEFAULT 0
        )
    """)

    # Table 2: Groups (each User can create their own contact groups)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
    """)

    # Table 3: Contact (each contact belongs to one User, and optionally one Group)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contact (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT,
            address TEXT,
            note TEXT,
            is_favorite INTEGER DEFAULT 0,
            group_id INTEGER,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES Groups(group_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            UNIQUE (phone_number, user_id)
        )
    """)

    conn.commit()

    # Create one default Admin account so there is always an Admin to log in with.
    cursor.execute("SELECT COUNT(*) AS total FROM User WHERE role = 'admin'")
    if cursor.fetchone()["total"] == 0:
        cursor.execute(
            "INSERT INTO User (username, password, email, role) VALUES (?, ?, ?, 'admin')",
            ("admin", hash_password("admin123"), "admin@phonebook.local"),
        )
        conn.commit()

    conn.close()
