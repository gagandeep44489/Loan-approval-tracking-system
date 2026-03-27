"""Business logic for loan processing and reporting."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Tuple

from models import LoanModel
from utils import validate_loan_input


class LoanService:
    def __init__(self, loan_model: LoanModel):
        self.loan_model = loan_model

    @staticmethod
    def calculate_emi(amount: float, annual_rate: float, tenure_months: int) -> float:
        monthly_rate = annual_rate / (12 * 100)
        if monthly_rate == 0:
            return round(amount / tenure_months, 2)
        factor = (1 + monthly_rate) ** tenure_months
        emi = (amount * monthly_rate * factor) / (factor - 1)
        return round(emi, 2)

    def add_loan_application(self, payload: dict) -> Tuple[bool, str, int | None]:
        valid, msg = validate_loan_input(payload)
        if not valid:
            return False, msg, None

        normalized = {
            "applicant_name": payload["applicant_name"].strip(),
            "age": int(payload["age"]),
            "income": float(payload["income"]),
            "amount": float(payload["amount"]),
            "loan_type": payload["loan_type"].strip(),
            "credit_score": int(payload["credit_score"]),
            "interest_rate": float(payload["interest_rate"]),
            "tenure_months": int(payload["tenure_months"]),
            "remarks": payload.get("remarks", "").strip(),
        }
        normalized["emi"] = self.calculate_emi(
            normalized["amount"], normalized["interest_rate"], normalized["tenure_months"]
        )

        try:
            loan_id = self.loan_model.create(normalized)
            return True, "Loan application created successfully", loan_id
        except Exception as exc:
            return False, f"Failed to save loan application: {exc}", None

    def get_dashboard_data(self):
        return self.loan_model.dashboard_counts()

    def get_loans(self, search_text: str = "", status: str = "All"):
        return self.loan_model.search(search_text=search_text, status=status)

    def change_status(self, loan_id: int, status: str, remarks: str):
        try:
            self.loan_model.update_status(loan_id=loan_id, status=status, remarks=remarks)
            return True, "Status updated successfully"
        except Exception as exc:
            return False, f"Could not update status: {exc}"

    def export_csv(self, destination: Path):
        loans = self.loan_model.list_all()
        headers = [
            "id",
            "applicant_name",
            "age",
            "income",
            "amount",
            "loan_type",
            "credit_score",
            "interest_rate",
            "tenure_months",
            "emi",
            "status",
            "remarks",
            "created_at",
        ]
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(loans)
        return destination
