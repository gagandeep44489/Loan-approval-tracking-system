"""Database helpers and initialization for SQLite."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager

try:
    from config import (
        DB_PATH,
        DEFAULT_ADMIN_PASSWORD,
        DEFAULT_ADMIN_USERNAME,
        DEFAULT_STAFF_PASSWORD,
        DEFAULT_STAFF_USERNAME,
    )
except ImportError:  # pragma: no cover - fallback for package execution
    from .config import (
        DB_PATH,
        DEFAULT_ADMIN_PASSWORD,
        DEFAULT_ADMIN_USERNAME,
        DEFAULT_STAFF_PASSWORD,
        DEFAULT_STAFF_USERNAME,
    )


class DatabaseManager:
    """Encapsulates DB connection and schema creation."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    applicant_name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    income REAL NOT NULL,
                    amount REAL NOT NULL,
                    loan_type TEXT NOT NULL,
                    credit_score INTEGER NOT NULL,
                    interest_rate REAL NOT NULL DEFAULT 11.5,
                    tenure_months INTEGER NOT NULL DEFAULT 60,
                    emi REAL NOT NULL DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    remarks TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, 'admin')",
                (DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD),
            )
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, 'staff')",
                (DEFAULT_STAFF_USERNAME, DEFAULT_STAFF_PASSWORD),
            )
