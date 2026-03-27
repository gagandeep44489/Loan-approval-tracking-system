# Loan Approval Tracking System (Desktop - Tkinter + SQLite)

A modular Python desktop application for managing loan applications, approval workflow, EMI calculation, and CSV reporting.

## Features
- Admin/Staff authentication with role-based access
- Loan application form with data validation
- Automatic Application ID generation (`APP-00001` pattern)
- Approval workflow (Pending / Approved / Rejected)
- EMI calculation
- Dashboard counters (Total, Approved, Pending, Rejected)
- Search by applicant name or application ID and status filter
- CSV export reports
- SQLite auto-initialization with default users

## Default Login
- **Admin**: `admin` / `admin123`
- **Staff**: `staff` / `staff123`

## Project Structure
```
loan_app/
├── main.py
├── config.py
├── database.py
├── models.py
├── auth.py
├── loan_service.py
├── utils.py
├── ui/
│   ├── login_ui.py
│   ├── dashboard_ui.py
│   ├── loan_form_ui.py
│   ├── approval_ui.py
│   ├── report_ui.py
├── assets/
│   └── logo.png
├── data/
│   └── loan_app.db
├── requirements.txt
├── README.md
└── .gitignore
```

## Run
```bash
cd loan_app
python main.py
```

## Build EXE (PyInstaller)
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name LoanApprovalTracking main.py
```

Generated binary will be in `dist/`.

## Notes
- The database file is created automatically if not present.
- For production use, store hashed passwords instead of plain text.
