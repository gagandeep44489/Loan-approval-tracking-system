"""Approval and search list screen."""
import tkinter as tk
from tkinter import ttk, messagebox


class ApprovalUI(ttk.Frame):
    def __init__(self, master, loan_service, current_user, on_data_changed):
        super().__init__(master, padding=12)
        self.loan_service = loan_service
        self.current_user = current_user
        self.on_data_changed = on_data_changed

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="All")
        self.remarks_var = tk.StringVar()
        self._build()
        self.load_data()

    def _build(self):
        control = ttk.Frame(self)
        control.pack(fill="x", pady=(0, 8))

        ttk.Label(control, text="Search (Name/ID)").grid(row=0, column=0, padx=4)
        ttk.Entry(control, textvariable=self.search_var, width=22).grid(row=0, column=1, padx=4)

        ttk.Label(control, text="Status").grid(row=0, column=2, padx=4)
        ttk.Combobox(
            control,
            textvariable=self.status_var,
            state="readonly",
            values=["All", "Pending", "Approved", "Rejected"],
            width=10,
        ).grid(row=0, column=3, padx=4)

        ttk.Button(control, text="Apply", command=self.load_data).grid(row=0, column=4, padx=4)

        columns = (
            "id",
            "applicant_name",
            "amount",
            "loan_type",
            "credit_score",
            "emi",
            "status",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=130, anchor="center")
        self.tree.pack(fill="both", expand=True)

        footer = ttk.Frame(self)
        footer.pack(fill="x", pady=8)
        ttk.Label(footer, text="Remarks").pack(side="left")
        ttk.Entry(footer, textvariable=self.remarks_var, width=40).pack(side="left", padx=8)

        self.approve_btn = ttk.Button(footer, text="Approve", command=lambda: self.update_status("Approved"))
        self.reject_btn = ttk.Button(footer, text="Reject", command=lambda: self.update_status("Rejected"))
        self.approve_btn.pack(side="left", padx=4)
        self.reject_btn.pack(side="left", padx=4)

        if self.current_user.role != "admin":
            self.approve_btn.state(["disabled"])
            self.reject_btn.state(["disabled"])

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.loan_service.get_loans(self.search_var.get(), self.status_var.get())
        for loan in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    loan["id"],
                    loan["applicant_name"],
                    f"₹{loan['amount']:,.0f}",
                    loan["loan_type"],
                    loan["credit_score"],
                    f"₹{loan['emi']:,.0f}",
                    loan["status"],
                ),
            )

    def update_status(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Row", "Please select one application")
            return

        loan_id = self.tree.item(selected[0], "values")[0]
        ok, msg = self.loan_service.change_status(int(loan_id), status, self.remarks_var.get())
        if not ok:
            messagebox.showerror("Update Failed", msg)
            return

        self.remarks_var.set("")
        messagebox.showinfo("Updated", msg)
        self.load_data()
        self.on_data_changed()
