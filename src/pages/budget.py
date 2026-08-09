import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#F59E0B"
TEXT = "#111827"
GRAY = "#6B7280"


class BudgetPage:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self, parent, db, user):

        self.parent = parent
        self.db = db
        self.user = user

        self.build_page()

    # ==========================================================
    # Build Complete Page
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

        self.frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.build_budget_form()

        self.build_summary()

    # ==========================================================
    # Budget Form
    # ==========================================================

    def build_budget_form(self):

        form = tk.LabelFrame(

            self.frame,

            text="Budget Planner",

            bg=WHITE,

            font=("Segoe UI", 11, "bold"),

            padx=20,

            pady=20

        )

        form.grid(

            row=0,

            column=0,

            sticky="ew",

            pady=(0, 15)

        )

        for i in range(4):

            form.grid_columnconfigure(
                i,
                weight=1
            )

        # ------------------------------------------------------
        # Category
        # ------------------------------------------------------

        tk.Label(

            form,

            text="Category",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI", 10)

        ).grid(

            row=0,

            column=0,

            sticky="w"

        )

        self.category = ttk.Combobox(

            form,

            state="readonly",

            values=[

                "Overall",

                "Food",

                "Transport",

                "Shopping",

                "Bills",

                "Entertainment",

                "Medical",

                "Education",

                "Other"

            ]

        )

        self.category.current(0)

        self.category.grid(

            row=1,

            column=0,

            padx=5,

            pady=5,

            sticky="ew"

        )

        # ------------------------------------------------------
        # Month
        # ------------------------------------------------------

        tk.Label(

            form,

            text="Month",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI", 10)

        ).grid(

            row=0,

            column=1,

            sticky="w"

        )

        months = [

            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"

        ]

        self.month = ttk.Combobox(

            form,

            state="readonly",

            values=months

        )

        self.month.current(
            datetime.now().month - 1
        )

        self.month.grid(

            row=1,

            column=1,

            padx=5,

            pady=5,

            sticky="ew"

        )

        # ------------------------------------------------------
        # Amount
        # ------------------------------------------------------

        tk.Label(

            form,

            text="Budget Amount",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI", 10)

        ).grid(

            row=0,

            column=2,

            sticky="w"

        )

        self.amount = tk.Entry(

            form,

            font=("Segoe UI", 11)

        )

        self.amount.grid(

            row=1,

            column=2,

            padx=5,

            pady=5,

            sticky="ew"

        )

        # ------------------------------------------------------
        # Save Button
        # ------------------------------------------------------

        self.save_btn = tk.Button(

            form,

            text="Save Budget",

            command=self.save_budget,

            bg=SUCCESS,

            fg="white",

            relief="flat",

            cursor="hand2",

            font=("Segoe UI", 10, "bold")

        )

        self.save_btn.grid(

            row=1,

            column=3,

            padx=10,

            sticky="ew"

        )
    # ==========================================================
    # Summary Section
    # ==========================================================

    def build_summary(self):

        summary = tk.Frame(
            self.frame,
            bg=BACKGROUND
        )

        summary.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        summary.grid_columnconfigure(0, weight=2)
        summary.grid_columnconfigure(1, weight=1)
        summary.grid_rowconfigure(0, weight=1)

        # IMPORTANT:
        # Build the status panel FIRST so all labels exist.
        self.build_budget_status(summary)

        # Then build the table.
        self.build_budget_table(summary)

        # Finally load data.
        self.load_budgets()

    # ==========================================================
    # Budget Overview
    # ==========================================================

    def build_budget_status(self, parent):

        status = tk.LabelFrame(

            parent,

            text="Budget Overview",

            bg=WHITE,

            font=("Segoe UI", 11, "bold"),

            padx=20,

            pady=20

        )

        status.grid(

            row=0,

            column=1,

            sticky="nsew",

            padx=(10, 0)

        )

        # -------------------------
        # Total Budget
        # -------------------------

        tk.Label(

            status,

            text="Total Budget",

            bg=WHITE,

            fg=GRAY,

            font=("Segoe UI", 10)

        ).pack(anchor="w")

        self.total_budget = tk.Label(

            status,

            text="₹0.00",

            bg=WHITE,

            fg=PRIMARY,

            font=("Segoe UI", 20, "bold")

        )

        self.total_budget.pack(
            anchor="w",
            pady=(0, 15)
        )

        # -------------------------
        # Total Expense
        # -------------------------

        tk.Label(

            status,

            text="Total Expense",

            bg=WHITE,

            fg=GRAY,

            font=("Segoe UI", 10)

        ).pack(anchor="w")

        self.total_spent = tk.Label(

            status,

            text="₹0.00",

            bg=WHITE,

            fg=DANGER,

            font=("Segoe UI", 20, "bold")

        )

        self.total_spent.pack(
            anchor="w",
            pady=(0, 15)
        )

        # -------------------------
        # Remaining
        # -------------------------

        tk.Label(

            status,

            text="Remaining Budget",

            bg=WHITE,

            fg=GRAY,

            font=("Segoe UI", 10)

        ).pack(anchor="w")

        self.remaining = tk.Label(

            status,

            text="₹0.00",

            bg=WHITE,

            fg=SUCCESS,

            font=("Segoe UI", 20, "bold")

        )

        self.remaining.pack(
            anchor="w",
            pady=(0, 20)
        )

        # -------------------------
        # Progress Bar
        # -------------------------

        self.progress = ttk.Progressbar(

            status,

            orient="horizontal",

            mode="determinate",

            length=260

        )

        self.progress.pack(
            fill="x",
            pady=(5, 15)
        )

        self.progress["maximum"] = 100
        self.progress["value"] = 0

        # -------------------------
        # Status Label
        # -------------------------

        self.status_label = tk.Label(

            status,

            text="No budget set",

            bg=WHITE,

            fg=GRAY,

            font=("Segoe UI", 10)

        )

        self.status_label.pack(anchor="w")

    # ==========================================================
    # Budget Table
    # ==========================================================

    def build_budget_table(self, parent):

        table_frame = tk.LabelFrame(

            parent,

            text="Saved Budgets",

            bg=WHITE,

            font=("Segoe UI", 11, "bold"),

            padx=10,

            pady=10

        )

        table_frame.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

        columns = (

            "Category",

            "Month",

            "Budget"

        )

        self.table = ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings",

            height=14

        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(

                column,

                anchor="center",

                width=150

            )

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
    # ==========================================================
    # Save Budget
    # ==========================================================

    def save_budget(self):

        category = self.category.get().strip()
        month = self.month.get().strip()
        amount = self.amount.get().strip()

        if not amount:

            messagebox.showerror(
                "Validation Error",
                "Please enter a budget amount."
            )

            return

        try:

            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Budget amount must be numeric."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Validation Error",
                "Budget amount must be greater than zero."
            )

            return

        existing = self.db.fetch_one(

            """
            SELECT id
            FROM budgets
            WHERE
                user_id=?
                AND category=?
                AND month=?
            """,

            (
                self.user["id"],
                category,
                month
            )

        )

        if existing:

            self.db.execute(

                """
                UPDATE budgets
                SET budget=?
                WHERE id=?
                """,

                (
                    amount,
                    existing["id"]
                )

            )

        else:

            self.db.execute(

                """
                INSERT INTO budgets
                (
                    user_id,
                    category,
                    budget,
                    month
                )
                VALUES
                (
                    ?,?,?,?
                )
                """,

                (
                    self.user["id"],
                    category,
                    amount,
                    month
                )

            )

        self.amount.delete(0, tk.END)

        self.load_budgets()

        messagebox.showinfo(

            "Success",

            "Budget saved successfully."

        )

    # ==========================================================
    # Load Budgets
    # ==========================================================

    def load_budgets(self):

        self.table.delete(*self.table.get_children())

        rows = self.db.fetch_all(

            """
            SELECT
                id,
                category,
                month,
                budget
            FROM budgets
            WHERE user_id=?
            ORDER BY created_at DESC
            """,

            (
                self.user["id"],
            )

        )

        total_budget = 0.0

        for row in rows:

            budget = float(row["budget"] or 0)

            total_budget += budget

            self.table.insert(

                "",

                tk.END,

                iid=row["id"],

                values=(

                    row["category"],

                    row["month"],

                    f"₹{budget:,.2f}"

                )

            )

        self.update_budget_status(total_budget)
        self.update_progress_style()

        self.check_budget_alert()

    # ==========================================================
    # Update Budget Status
    # ==========================================================

    def update_budget_status(self, total_budget):

        expense_row = self.db.fetch_one(

            """
            SELECT
                IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Expense'
            """,

            (
                self.user["id"],
            )

        )

        expense = expense_row["total"] if expense_row else 0

        remaining = total_budget - expense

        self.total_budget.config(

            text=f"₹{total_budget:,.2f}"

        )

        self.total_spent.config(

            text=f"₹{expense:,.2f}"

        )

        self.remaining.config(

            text=f"₹{remaining:,.2f}"

        )

        if total_budget <= 0:

            percentage = 0

        else:

            percentage = min(
                (expense / total_budget) * 100,
                100
            )

        self.progress["value"] = percentage

        # ---------------------------------------
        # Status
        # ---------------------------------------

        if total_budget == 0:

            self.status_label.config(

                text="No budget has been created.",

                fg=GRAY

            )

        elif expense > total_budget:

            self.status_label.config(

                text="Budget exceeded.",

                fg=DANGER

            )

        elif percentage >= 90:

            self.status_label.config(

                text="Approaching budget limit.",

                fg=WARNING

            )

        else:

            self.status_label.config(

                text="Budget is healthy.",

                fg=SUCCESS

            ) 
    # ==========================================================
    # Delete Selected Budget
    # ==========================================================

    def delete_budget(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Delete Budget",
                "Please select a budget to delete."
            )

            return

        budget_id = selected[0]

        confirm = messagebox.askyesno(
            "Delete Budget",
            "Are you sure you want to delete the selected budget?"
        )

        if not confirm:
            return

        self.db.execute(

            """
            DELETE FROM budgets
            WHERE id=?
            """,

            (budget_id,)

        )

        self.load_budgets()

        messagebox.showinfo(
            "Success",
            "Budget deleted successfully."
        )

    # ==========================================================
    # Refresh Page
    # ==========================================================

    def refresh(self):

        self.amount.delete(0, tk.END)

        self.category.current(0)

        self.month.current(
            datetime.now().month - 1
        )

        self.load_budgets()

    # ==========================================================
    # Progress Bar Style
    # ==========================================================

    def update_progress_style(self):

        value = self.progress["value"]

        style = ttk.Style()

        if value < 60:

            style.configure(
                "Budget.Green.Horizontal.TProgressbar",
                troughcolor="#E5E7EB",
                background=SUCCESS
            )

            self.progress.configure(
                style="Budget.Green.Horizontal.TProgressbar"
            )

        elif value < 90:

            style.configure(
                "Budget.Yellow.Horizontal.TProgressbar",
                troughcolor="#E5E7EB",
                background=WARNING
            )

            self.progress.configure(
                style="Budget.Yellow.Horizontal.TProgressbar"
            )

        else:

            style.configure(
                "Budget.Red.Horizontal.TProgressbar",
                troughcolor="#E5E7EB",
                background=DANGER
            )

            self.progress.configure(
                style="Budget.Red.Horizontal.TProgressbar"
            )

    # ==========================================================
    # Budget Alert
    # ==========================================================

    def check_budget_alert(self):

        value = self.progress["value"]

        if value >= 100:

            messagebox.showwarning(

                "Budget Alert",

                "You have exceeded your total budget."

            )

        elif value >= 90:

            messagebox.showwarning(

                "Budget Alert",

                "You have used more than 90% of your budget."

            )

    # ==========================================================
    # Refresh Dashboard Data
    # ==========================================================

    def refresh_dashboard(self):

        self.load_budgets()

        self.update_progress_style()

    # ==========================================================
    # Reset Form
    # ==========================================================

    def reset_form(self):

        self.amount.delete(0, tk.END)

        self.category.current(0)

        self.month.current(
            datetime.now().month - 1
        )

    # ==========================================================
    # Close Page
    # ==========================================================

    def close(self):

        self.frame.destroy()                   