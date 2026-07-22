"""
Database Manager — SQLite Data Persistence
===========================================
Manages local SQLite database for conversation history, messages,
user settings, and productivity items.
"""

import sqlite3
import json
from datetime import datetime
from bujji.config import DB_PATH


class DatabaseManager:
    """
    SQLite database wrapper providing thread-safe connection management
    and CRUD helper methods.
    """

    def __init__(self, db_path=None):
        self.db_path = str(db_path or DB_PATH)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Create database tables if they do not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Conversations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    personality TEXT DEFAULT 'friendly'
                )
            """)

            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
                )
            """)

            # Settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

            # Reminders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    due_time TEXT,
                    completed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    # ─── Settings CRUD ────────────────────────────────────────────────────────

    def set_setting(self, key, value):
        val_str = json.dumps(value) if not isinstance(value, str) else value
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, val_str)
            )
            conn.commit()

    def get_setting(self, key, default=None):
        with self.get_connection() as conn:
            cur = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cur.fetchone()
            if row:
                try:
                    return json.loads(row["value"])
                except Exception:
                    return row["value"]
            return default

    # ─── Conversations CRUD ───────────────────────────────────────────────────

    def save_conversation(self, conv_id, title, personality="friendly"):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO conversations (id, title, updated_at, personality)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    updated_at=CURRENT_TIMESTAMP,
                    personality=excluded.personality
                """,
                (conv_id, title, personality)
            )
            conn.commit()

    def get_conversations(self):
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM conversations ORDER BY updated_at DESC"
            )
            return [dict(row) for row in cur.fetchall()]

    def delete_conversation(self, conv_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
            conn.commit()

    # ─── Messages CRUD ────────────────────────────────────────────────────────

    def add_message(self, conv_id, role, content):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conv_id, role, content)
            )
            conn.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conv_id,)
            )
            conn.commit()

    def get_messages(self, conv_id):
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM messages WHERE conversation_id = ? ORDER BY id ASC",
                (conv_id,)
            )
            return [dict(row) for row in cur.fetchall()]
