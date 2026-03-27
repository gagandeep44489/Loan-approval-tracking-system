"""Entry point for Loan Approval Tracking System desktop app."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

try:
    from auth import AuthService
    from config import APP_TITLE, WINDOW_SIZE
    from database import DatabaseManager
    from models import LoanModel, UserModel
    from loan_service import LoanService
    from ui.dashboard_ui import DashboardUI
    from ui.login_ui import LoginUI
except ImportError:  # pragma: no cover - fallback for package execution
    from .auth import AuthService
    from .config import APP_TITLE, WINDOW_SIZE
    from .database import DatabaseManager
    from .models import LoanModel, UserModel
    from .loan_service import LoanService
    from .ui.dashboard_ui import DashboardUI
    from .ui.login_ui import LoginUI


class LoanApprovalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(980, 620)

        self._setup_style()

        self.db = DatabaseManager()
        self.db.initialize()

        user_model = UserModel(self.db)
        loan_model = LoanModel(self.db)

        self.auth_service = AuthService(user_model)
        self.loan_service = LoanService(loan_model)
        self.current_frame = None

        self.show_login()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Info.TLabel", font=("Segoe UI", 10), foreground="#2c3e50")
        style.configure("Stat.TLabel", font=("Segoe UI", 14, "bold"), foreground="#0b6e4f")
        style.configure("Card.TFrame", relief="groove", borderwidth=1)

    def _swap_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        frame = LoginUI(self, self.auth_service, self.show_dashboard)
        self._swap_frame(frame)

    def show_dashboard(self, user):
        try:
            frame = DashboardUI(self, self.loan_service, user)
            self._swap_frame(frame)
            self.title(f"{APP_TITLE} - Dashboard")
        except Exception as exc:
            messagebox.showerror("Error", f"Unable to load dashboard: {exc}")
            self.show_login()


def main():
    try:
        app = LoanApprovalApp()
        app.mainloop()
    except Exception as exc:
        messagebox.showerror("Fatal Error", str(exc))


if __name__ == "__main__":
    main()
