"""Data access models for users and loans."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:
    from database import DatabaseManager
except ImportError:  # pragma: no cover - fallback for package execution
    from .database import DatabaseManager


@dataclass
class User:
    id: int
    username: str
    role: str


@dataclass
class LoanApplication:
    id: int
    applicant_name: str
    age: int
    income: float
    amount: float
    loan_type: str
    credit_score: int
    interest_rate: float
    tenure_months: int
    emi: float
    status: str
    remarks: str


class UserModel:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def authenticate(self, username: str, password: str) -> Optional[User]:
        with self.db.connection() as conn:
            row = conn.execute(
                "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
                (username.strip(), password),
            ).fetchone()
        if not row:
            return None
        return User(id=row["id"], username=row["username"], role=row["role"])


class LoanModel:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create(self, data: dict) -> int:
        with self.db.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO loans
                (applicant_name, age, income, amount, loan_type, credit_score,
                 interest_rate, tenure_months, emi, status, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
                """,
                (
                    data["applicant_name"],
                    data["age"],
                    data["income"],
                    data["amount"],
                    data["loan_type"],
                    data["credit_score"],
                    data["interest_rate"],
                    data["tenure_months"],
                    data["emi"],
                    data.get("remarks", ""),
                ),
            )
            return cursor.lastrowid

    def list_all(self):
        with self.db.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM loans ORDER BY id DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    def search(self, search_text: str = "", status: str = "All"):
        clauses = []
        params = []
        if search_text.strip():
            clauses.append("(applicant_name LIKE ? OR id LIKE ?)")
            term = f"%{search_text.strip()}%"
            params.extend([term, term])
        if status and status != "All":
            clauses.append("status = ?")
            params.append(status)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT * FROM loans {where_sql} ORDER BY id DESC"

        with self.db.connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

    def update_status(self, loan_id: int, status: str, remarks: str):
        with self.db.connection() as conn:
            conn.execute(
                "UPDATE loans SET status = ?, remarks = ? WHERE id = ?",
                (status, remarks.strip(), loan_id),
            )

    def dashboard_counts(self):
        with self.db.connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM loans").fetchone()[0]
            approved = conn.execute(
                "SELECT COUNT(*) FROM loans WHERE status='Approved'"
            ).fetchone()[0]
            pending = conn.execute(
                "SELECT COUNT(*) FROM loans WHERE status='Pending'"
            ).fetchone()[0]
            rejected = conn.execute(
                "SELECT COUNT(*) FROM loans WHERE status='Rejected'"
            ).fetchone()[0]
        return {
            "total": total,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
        }
