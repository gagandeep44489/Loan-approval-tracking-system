"""Utility helpers for formatting and validation."""
from __future__ import annotations

from typing import Tuple


def validate_loan_input(payload: dict) -> Tuple[bool, str]:
    required = [
        "applicant_name",
        "age",
        "income",
        "amount",
        "loan_type",
        "credit_score",
        "interest_rate",
        "tenure_months",
    ]
    for key in required:
        if str(payload.get(key, "")).strip() == "":
            return False, f"{key.replace('_', ' ').title()} is required"

    try:
        age = int(payload["age"])
        credit = int(payload["credit_score"])
        tenure = int(payload["tenure_months"])
        income = float(payload["income"])
        amount = float(payload["amount"])
        rate = float(payload["interest_rate"])
    except ValueError:
        return False, "Age, income, amount, credit score, interest rate and tenure must be numeric"

    if age < 18 or age > 75:
        return False, "Age must be between 18 and 75"
    if income <= 0 or amount <= 0:
        return False, "Income and loan amount must be greater than zero"
    if credit < 300 or credit > 900:
        return False, "Credit score must be between 300 and 900"
    if rate <= 0:
        return False, "Interest rate must be greater than zero"
    if tenure < 1:
        return False, "Tenure must be at least 1 month"
    return True, ""


def format_application_id(loan_id: int) -> str:
    return f"APP-{loan_id:05d}"
