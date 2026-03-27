"""Login screen."""
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from config import APP_TITLE
except ImportError:  # pragma: no cover - fallback for package execution
    from ..config import APP_TITLE


class LoginUI(ttk.Frame):
    def __init__(self, master, auth_service, on_login_success):
        super().__init__(master, padding=30)
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.master.title(f"{APP_TITLE} - Login")

        self.columnconfigure(0, weight=1)
        card = ttk.Frame(self, padding=30, style="Card.TFrame")
        card.grid(row=0, column=0, sticky="nsew")

        ttk.Label(card, text="Loan Approval Tracking System", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )
        ttk.Label(card, text="Username").grid(row=1, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.username_var, width=28).grid(
            row=1, column=1, sticky="ew", pady=5
        )

        ttk.Label(card, text="Password").grid(row=2, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(card, textvariable=self.password_var, show="*", width=28)
        password_entry.grid(row=2, column=1, sticky="ew", pady=5)
        password_entry.bind("<Return>", lambda _e: self.perform_login())

        ttk.Button(card, text="Login", command=self.perform_login).grid(
            row=3, column=0, columnspan=2, pady=14
        )

        ttk.Label(
            card,
            text="Default users: admin/admin123 and staff/staff123",
            foreground="#666",
        ).grid(row=4, column=0, columnspan=2)

    def perform_login(self):
        user, message = self.auth_service.login(self.username_var.get(), self.password_var.get())
        if not user:
            messagebox.showerror("Login Failed", message)
            return
        messagebox.showinfo("Welcome", f"Logged in as {user.role.title()}")
        self.on_login_success(user)
