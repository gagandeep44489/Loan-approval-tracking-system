"""Configuration values for Loan Approval Tracking System."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = DATA_DIR / "loan_app.db"

APP_TITLE = "Loan Approval Tracking System"
WINDOW_SIZE = "1120x720"

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"
DEFAULT_STAFF_USERNAME = "staff"
DEFAULT_STAFF_PASSWORD = "staff123"

LOAN_TYPES = ["Personal", "Home", "Auto", "Education", "Business"]
LOAN_STATUSES = ["Pending", "Approved", "Rejected"]
DEFAULT_INTEREST_RATE = 11.5
DEFAULT_TENURE_MONTHS = 60
