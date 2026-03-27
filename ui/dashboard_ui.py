"""Main dashboard containing tabs."""
from tkinter import ttk

try:
    from ui.approval_ui import ApprovalUI
    from ui.loan_form_ui import LoanFormUI
    from ui.report_ui import ReportUI
except ImportError:  # pragma: no cover - fallback for package execution
    from .approval_ui import ApprovalUI
    from .loan_form_ui import LoanFormUI
    from .report_ui import ReportUI


class DashboardUI(ttk.Frame):
    def __init__(self, master, loan_service, user):
        super().__init__(master, padding=12)
        self.loan_service = loan_service
        self.user = user

        self.stats_vars = {
            "total": ttk.Label(self, style="Stat.TLabel"),
            "approved": ttk.Label(self, style="Stat.TLabel"),
            "pending": ttk.Label(self, style="Stat.TLabel"),
            "rejected": ttk.Label(self, style="Stat.TLabel"),
        }
        self._build()
        self.refresh_stats()

    def _build(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))

        ttk.Label(
            header,
            text=f"Logged in as: {self.user.username} ({self.user.role.title()})",
            style="Info.TLabel",
        ).pack(anchor="w")

        stat_frame = ttk.Frame(self)
        stat_frame.pack(fill="x", pady=6)
        for idx, key in enumerate(("total", "approved", "pending", "rejected")):
            card = ttk.Frame(stat_frame, style="Card.TFrame", padding=10)
            card.grid(row=0, column=idx, padx=5, sticky="nsew")
            stat_frame.columnconfigure(idx, weight=1)
            ttk.Label(card, text=key.title()).pack()
            self.stats_vars[key].pack()

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, pady=8)

        self.loan_form_tab = LoanFormUI(notebook, self.loan_service, self.on_data_changed)
        self.approval_tab = ApprovalUI(notebook, self.loan_service, self.user, self.on_data_changed)
        self.report_tab = ReportUI(notebook, self.loan_service)

        notebook.add(self.loan_form_tab, text="New Application")
        notebook.add(self.approval_tab, text="Approval & Search")
        notebook.add(self.report_tab, text="Reports")

    def refresh_stats(self):
        data = self.loan_service.get_dashboard_data()
        for key, label in self.stats_vars.items():
            label.config(text=str(data.get(key, 0)))

    def on_data_changed(self):
        self.refresh_stats()
        self.approval_tab.load_data()
