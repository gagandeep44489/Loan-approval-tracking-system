"""Report and CSV export screen."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from tkinter import ttk, filedialog, messagebox


class ReportUI(ttk.Frame):
    def __init__(self, master, loan_service):
        super().__init__(master, padding=12)
        self.loan_service = loan_service

        ttk.Label(self, text="Export all loan data to CSV").pack(anchor="w", pady=5)
        ttk.Button(self, text="Export CSV", command=self.export_csv).pack(anchor="w", pady=5)

    def export_csv(self):
        default_name = f"loan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_to = filedialog.asksaveasfilename(
            title="Save Loan Report",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV", "*.csv")],
        )
        if not save_to:
            return

        try:
            path = self.loan_service.export_csv(Path(save_to))
            messagebox.showinfo("Export Complete", f"Report exported to:\n{path}")
        except Exception as exc:
            messagebox.showerror("Export Failed", str(exc))
