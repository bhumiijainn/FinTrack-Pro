import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
TEXT = "#111827"
GRAY = "#6B7280"


class ReportsPage:

    def __init__(self, parent, db, user):

        self.parent = parent
        self.db = db
        self.user = user

        self.build_page()

    # ==========================================================
    # Build Reports Page
    # ==========================================================

    def build_page(self):

        self.frame = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        self.build_filter_panel()

        self.build_report_table()
        self.create_summary()

    # ==========================================================
    # Filter Panel
    # ==========================================================

    def build_filter_panel(self):

        panel = tk.LabelFrame(
            self.frame,
            text="Generate Report",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=20
        )

        panel.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        for i in range(6):
            panel.grid_columnconfigure(i, weight=1)

        # ----------------------------------
        # Report Type
        # ----------------------------------

        tk.Label(
            panel,
            text="Report Type",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.report_type = ttk.Combobox(
            panel,
            state="readonly",
            values=[
                "All Transactions",
                "Income",
                "Expense",
                "Daily",
                "Weekly",
                "Monthly",
                "Yearly"
            ]
        )

        self.report_type.current(0)

        self.report_type.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # ----------------------------------
        # From Date
        # ----------------------------------

        tk.Label(
            panel,
            text="From Date",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.from_date = tk.Entry(
            panel,
            font=("Segoe UI", 10)
        )

        self.from_date.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        self.from_date.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # ----------------------------------
        # To Date
        # ----------------------------------

        tk.Label(
            panel,
            text="To Date",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=2,
            sticky="w"
        )

        self.to_date = tk.Entry(
            panel,
            font=("Segoe UI", 10)
        )

        self.to_date.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        self.to_date.grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # ----------------------------------
        # Generate Button
        # ----------------------------------

        generate_btn = tk.Button(
            panel,
            text="Generate Report",
            bg=PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.generate_report
        )

        generate_btn.grid(
            row=1,
            column=3,
            padx=15,
            sticky="ew"
        )

        # ----------------------------------
        # Refresh Button
        # ----------------------------------

        refresh_btn = tk.Button(
            panel,
            text="Refresh",
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.refresh
        )

        refresh_btn.grid(
            row=1,
            column=4,
            padx=5,
            sticky="ew"
        )

        # ----------------------------------
        # Export Button
        # ----------------------------------

        export_btn = tk.Button(
            panel,
            text="Export",
            bg="#F59E0B",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self.export_report
        )

        export_btn.grid(
            row=1,
            column=5,
            padx=5,
            sticky="ew"
        )

    # ==========================================================
    # Report Table
    # ==========================================================

    def build_report_table(self):

        table_frame = tk.LabelFrame(
            self.frame,
            text="Transaction Report",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )

        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )
        # ======================================================
        # Report Table
        # ======================================================

        columns = (
            "Date",
            "Type",
            "Category",
            "Amount",
            "Description"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=18
        )

        # --------------------------------------------------
        # Headings
        # --------------------------------------------------

        for col in columns:

            self.table.heading(
                col,
                text=col
            )

        # --------------------------------------------------
        # Column Width
        # --------------------------------------------------

        self.table.column(
            "Date",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Type",
            width=100,
            anchor="center"
        )

        self.table.column(
            "Category",
            width=150,
            anchor="center"
        )

        self.table.column(
            "Amount",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Description",
            width=300,
            anchor="w"
        )

        # --------------------------------------------------
        # Scrollbar
        # --------------------------------------------------

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.load_all_transactions()

    # ==========================================================
    # Load All Transactions
    # ==========================================================

    def load_all_transactions(self):

        for item in self.table.get_children():

            self.table.delete(item)

        rows = self.db.fetch_all(

            """
            SELECT
                date,
                type,
                category,
                amount,
                description
            FROM transactions
            WHERE user_id=?
            ORDER BY id DESC
            """,

            (self.user["id"],)

        )

        for row in rows:

            self.table.insert(

                "",

                tk.END,

                values=(

                    row["date"],

                    row["type"],

                    row["category"],

                    f"₹{row['amount']:,.2f}",

                    row["description"]

                )

            )
    # ==========================================================
    # Generate Report
    # ==========================================================

    def generate_report(self):

        report_type = self.report_type.get()

        for item in self.table.get_children():

            self.table.delete(item)

        # ---------------------------------------
        # SQL Query
        # ---------------------------------------

        if report_type == "All Transactions":

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE user_id=?
                ORDER BY id DESC
            """

            params = (self.user["id"],)

        elif report_type == "Income":

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND type='Income'
                ORDER BY id DESC
            """

            params = (self.user["id"],)

        elif report_type == "Expense":

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND type='Expense'
                ORDER BY id DESC
            """

            params = (self.user["id"],)

        elif report_type == "Daily":

            today = datetime.now().strftime("%d-%m-%Y")

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND date=?
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                today
            )

        elif report_type == "Weekly":

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE user_id=?
                ORDER BY id DESC
            """

            params = (self.user["id"],)

        elif report_type == "Monthly":

            month = datetime.now().strftime("%m-%Y")

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                ORDER BY id DESC
            """

            params = (self.user["id"],)

        elif report_type == "Yearly":

            year = datetime.now().strftime("%Y")

            query = """
                SELECT
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                ORDER BY id DESC
            """

            params = (self.user["id"],)

        else:

            return

        rows = self.db.fetch_all(
            query,
            params
        )

        income = 0
        expense = 0

        for row in rows:

            self.table.insert(

                "",

                tk.END,

                values=(

                    row["date"],

                    row["type"],

                    row["category"],

                    f"₹{row['amount']:,.2f}",

                    row["description"]

                )

            )

            if row["type"] == "Income":

                income += row["amount"]

            else:

                expense += row["amount"]

        balance = income - expense

        self.summary_income.config(
            text=f"₹{income:,.2f}"
        )

        self.summary_expense.config(
            text=f"₹{expense:,.2f}"
        )

        self.summary_balance.config(
            text=f"₹{balance:,.2f}"
        )

    # ==========================================================
    # Refresh Reports
    # ==========================================================

    def refresh(self):

        self.report_type.current(0)

        self.from_date.delete(0, tk.END)
        self.to_date.delete(0, tk.END)

        today = datetime.now().strftime("%d-%m-%Y")

        self.from_date.insert(
            0,
            today
        )

        self.to_date.insert(
            0,
            today
        )

        self.load_all_transactions()

        self.summary_income.config(text="₹0.00")
        self.summary_expense.config(text="₹0.00")
        self.summary_balance.config(text="₹0.00")    
    # ==========================================================
    # Report Summary
    # ==========================================================

    def create_summary(self):

        summary = tk.LabelFrame(
            self.frame,
            text="Report Summary",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=15
        )

        summary.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(15,0)
        )

        summary.grid_columnconfigure((0,1,2), weight=1)

        # -----------------------------
        # Income
        # -----------------------------

        income_frame = tk.Frame(
            summary,
            bg="#DCFCE7",
            bd=1,
            relief="solid"
        )

        income_frame.grid(
            row=0,
            column=0,
            padx=8,
            sticky="ew"
        )

        tk.Label(
            income_frame,
            text="Total Income",
            bg="#DCFCE7",
            fg="#166534",
            font=("Segoe UI",10)
        ).pack(pady=(10,0))

        self.summary_income = tk.Label(
            income_frame,
            text="₹0.00",
            bg="#DCFCE7",
            fg="#166534",
            font=("Segoe UI",18,"bold")
        )

        self.summary_income.pack(pady=(5,10))

        # -----------------------------
        # Expense
        # -----------------------------

        expense_frame = tk.Frame(
            summary,
            bg="#FEE2E2",
            bd=1,
            relief="solid"
        )

        expense_frame.grid(
            row=0,
            column=1,
            padx=8,
            sticky="ew"
        )

        tk.Label(
            expense_frame,
            text="Total Expense",
            bg="#FEE2E2",
            fg="#991B1B",
            font=("Segoe UI",10)
        ).pack(pady=(10,0))

        self.summary_expense = tk.Label(
            expense_frame,
            text="₹0.00",
            bg="#FEE2E2",
            fg="#991B1B",
            font=("Segoe UI",18,"bold")
        )

        self.summary_expense.pack(pady=(5,10))

        # -----------------------------
        # Balance
        # -----------------------------

        balance_frame = tk.Frame(
            summary,
            bg="#DBEAFE",
            bd=1,
            relief="solid"
        )

        balance_frame.grid(
            row=0,
            column=2,
            padx=8,
            sticky="ew"
        )

        tk.Label(
            balance_frame,
            text="Net Balance",
            bg="#DBEAFE",
            fg="#1D4ED8",
            font=("Segoe UI",10)
        ).pack(pady=(10,0))

        self.summary_balance = tk.Label(
            balance_frame,
            text="₹0.00",
            bg="#DBEAFE",
            fg="#1D4ED8",
            font=("Segoe UI",18,"bold")
        )

        self.summary_balance.pack(pady=(5,10))

    # ==========================================================
    # Export Report
    # ==========================================================

    def export_report(self):

        messagebox.showinfo(

            "Coming Soon",

            "Export to PDF / Excel / CSV will be added in the next update."

        )                