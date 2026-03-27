"""Loan application form screen."""
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from config import DEFAULT_INTEREST_RATE, DEFAULT_TENURE_MONTHS, LOAN_TYPES
    from utils import format_application_id
except ImportError:  # pragma: no cover - fallback for package execution
    from ..config import DEFAULT_INTEREST_RATE, DEFAULT_TENURE_MONTHS, LOAN_TYPES
    from ..utils import format_application_id


class LoanFormUI(ttk.Frame):
    def __init__(self, master, loan_service, on_created):
        super().__init__(master, padding=12)
        self.loan_service = loan_service
        self.on_created = on_created
        self._build()

    def _build(self):
        for c in range(2):
            self.columnconfigure(c, weight=1)

        self.fields = {
            "applicant_name": tk.StringVar(),
            "age": tk.StringVar(),
            "income": tk.StringVar(),
            "amount": tk.StringVar(),
            "loan_type": tk.StringVar(value=LOAN_TYPES[0]),
            "credit_score": tk.StringVar(),
            "interest_rate": tk.StringVar(value=str(DEFAULT_INTEREST_RATE)),
            "tenure_months": tk.StringVar(value=str(DEFAULT_TENURE_MONTHS)),
            "remarks": tk.StringVar(),
        }

        labels = [
            ("Applicant Name", "applicant_name"),
            ("Age", "age"),
            ("Monthly Income", "income"),
            ("Loan Amount", "amount"),
            ("Loan Type", "loan_type"),
            ("Credit Score", "credit_score"),
            ("Interest Rate (Annual %)", "interest_rate"),
            ("Tenure (Months)", "tenure_months"),
            ("Remarks", "remarks"),
        ]

        for idx, (text, key) in enumerate(labels):
            ttk.Label(self, text=text).grid(row=idx, column=0, sticky="w", pady=4)
            if key == "loan_type":
                ttk.Combobox(
                    self,
                    textvariable=self.fields[key],
                    values=LOAN_TYPES,
                    state="readonly",
                ).grid(row=idx, column=1, sticky="ew", pady=4)
            else:
                ttk.Entry(self, textvariable=self.fields[key]).grid(
                    row=idx, column=1, sticky="ew", pady=4
                )

        self.emi_var = tk.StringVar(value="EMI: -")
        ttk.Label(self, textvariable=self.emi_var, style="Info.TLabel").grid(
            row=len(labels), column=0, sticky="w", pady=10
        )

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=len(labels) + 1, column=0, columnspan=2, sticky="e")
        ttk.Button(btn_frame, text="Calculate EMI", command=self.calculate_emi).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(btn_frame, text="Submit Application", command=self.submit).grid(
            row=0, column=1, padx=5
        )

    def _payload(self):
        return {key: var.get() for key, var in self.fields.items()}

    def calculate_emi(self):
        payload = self._payload()
        try:
            emi = self.loan_service.calculate_emi(
                float(payload["amount"]),
                float(payload["interest_rate"]),
                int(payload["tenure_months"]),
            )
            self.emi_var.set(f"EMI: ₹{emi:,.2f}")
        except Exception as exc:
            messagebox.showerror("EMI Error", f"Unable to calculate EMI: {exc}")

    def submit(self):
        payload = self._payload()
        ok, msg, loan_id = self.loan_service.add_loan_application(payload)
        if not ok:
            messagebox.showerror("Validation Error", msg)
            return

        app_id = format_application_id(loan_id)
        messagebox.showinfo("Saved", f"Application saved successfully\nID: {app_id}")

        for key, var in self.fields.items():
            if key == "loan_type":
                var.set(LOAN_TYPES[0])
            elif key == "interest_rate":
                var.set(str(DEFAULT_INTEREST_RATE))
            elif key == "tenure_months":
                var.set(str(DEFAULT_TENURE_MONTHS))
            else:
                var.set("")

        self.emi_var.set("EMI: -")
        self.on_created()
