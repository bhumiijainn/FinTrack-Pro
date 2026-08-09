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


class ExpensePage:

    def __init__(self, parent, db, user):

        self.parent = parent
        self.db = db
        self.user = user

        self.build_page()

    # ==========================================================
    # Build Page
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
        self.frame.grid_columnconfigure(1, weight=2)
        self.frame.grid_rowconfigure(0, weight=1)

        self.build_form()

        self.build_table()

    # ==========================================================
    # Expense Form
    # ==========================================================

    def build_form(self):

        form = tk.LabelFrame(
            self.frame,
            text="Add Expense",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=20
        )

        form.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 15)
        )

        # ---------------------------------
        # Expense Source
        # ---------------------------------

        tk.Label(
            form,
            text="Expense Source",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        self.source = tk.Entry(
            form,
            font=("Segoe UI", 11)
        )

        self.source.pack(
            fill="x",
            pady=(5, 15)
        )

        # ---------------------------------
        # Category
        # ---------------------------------

        tk.Label(
            form,
            text="Category",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        self.category = ttk.Combobox(
            form,
            state="readonly",
            values=[
                "Food",
                "Shopping",
                "Bills",
                "Fuel",
                "Travel",
                "Health",
                "Education",
                "Entertainment",
                "Rent",
                "Other"
            ]
        )

        self.category.pack(
            fill="x",
            pady=(5, 15)
        )

        # ---------------------------------
        # Amount
        # ---------------------------------

        tk.Label(
            form,
            text="Amount",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        self.amount = tk.Entry(
            form,
            font=("Segoe UI", 11)
        )

        self.amount.pack(
            fill="x",
            pady=(5, 15)
        )

        # ---------------------------------
        # Date
        # ---------------------------------

        tk.Label(
            form,
            text="Date",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        self.date = tk.Entry(
            form,
            font=("Segoe UI", 11)
        )

        self.date.insert(
            0,
            datetime.now().strftime("%d-%m-%Y")
        )

        self.date.pack(
            fill="x",
            pady=(5, 15)
        )

        # ---------------------------------
        # Description
        # ---------------------------------

        tk.Label(
            form,
            text="Description",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        self.description = tk.Text(
            form,
            height=5,
            font=("Segoe UI", 10)
        )

        self.description.pack(
            fill="x",
            pady=(5, 20)
        )

        # ---------------------------------
        # Save Button
        # ---------------------------------

        save_btn = tk.Button(
            form,
            text="Save Expense",
            command=self.save_expense,
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            pady=10
        )

        save_btn.pack(
            fill="x"
        )

    # ==========================================================
    # Expense Table
    # ==========================================================

    def build_table(self):

        table_frame = tk.LabelFrame(
            self.frame,
            text="Recent Expenses",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )

        table_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # ======================================================
        # Expense Table
        # ======================================================

        columns = (
            "Date",
            "Source",
            "Category",
            "Amount"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=16
        )

        # -----------------------------------
        # Headings
        # -----------------------------------

        self.table.heading(
            "Date",
            text="Date"
        )

        self.table.heading(
            "Source",
            text="Source"
        )

        self.table.heading(
            "Category",
            text="Category"
        )

        self.table.heading(
            "Amount",
            text="Amount"
        )

        # -----------------------------------
        # Column Width
        # -----------------------------------

        self.table.column(
            "Date",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Source",
            width=180,
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

        # -----------------------------------
        # Scrollbar
        # -----------------------------------

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

        # Load Expenses

        self.load_expenses()

    # ==========================================================
    # Load Expenses
    # ==========================================================

    def load_expenses(self):

        # Clear old records

        for row in self.table.get_children():

            self.table.delete(row)

        rows = self.db.fetch_all(

            """
            SELECT
                id,
                date,
                category,
                amount,
                description
            FROM transactions
            WHERE
                user_id = ?
                AND type = 'Expense'
            ORDER BY id DESC
            """,

            (self.user["id"],)

        )

        for row in rows:

            self.table.insert(

                "",

                tk.END,

                iid=row["id"],

                values=(

                    row["date"],

                    row["description"],

                    row["category"],

                    f"₹{row['amount']:,.2f}"

                )

            )
    # ==========================================================
    # Save Expense
    # ==========================================================

    def save_expense(self):

        source = self.source.get().strip()
        category = self.category.get().strip()
        amount = self.amount.get().strip()
        date = self.date.get().strip()
        description = self.description.get(
            "1.0",
            tk.END
        ).strip()

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        if not source:

            messagebox.showerror(
                "Error",
                "Please enter Expense Source."
            )

            return

        if not category:

            messagebox.showerror(
                "Error",
                "Please select a Category."
            )

            return

        if not amount:

            messagebox.showerror(
                "Error",
                "Please enter Amount."
            )

            return

        try:

            amount = float(amount)

            if amount <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(

                "Invalid Amount",

                "Amount must be greater than 0."

            )

            return

        # --------------------------------------------------
        # Store Source + Description
        # --------------------------------------------------

        full_description = source

        if description:

            full_description += f" | {description}"

        # --------------------------------------------------
        # Insert into Database
        # --------------------------------------------------

        self.db.execute(

            """
            INSERT INTO transactions
            (
                user_id,
                type,
                category,
                amount,
                description,
                date
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,

            (

                self.user["id"],

                "Expense",

                category,

                amount,

                full_description,

                date

            )

        )

        # --------------------------------------------------
        # Reload Table
        # --------------------------------------------------

        self.load_expenses()

        # --------------------------------------------------
        # Clear Form
        # --------------------------------------------------

        self.clear_form()

        messagebox.showinfo(

            "Success",

            "Expense added successfully."

        )

    # ==========================================================
    # Clear Form
    # ==========================================================

    def clear_form(self):

        self.source.delete(0, tk.END)

        self.category.set("")

        self.amount.delete(0, tk.END)

        self.date.delete(0, tk.END)

        self.date.insert(

            0,

            datetime.now().strftime("%d-%m-%Y")

        )

        self.description.delete(

            "1.0",

            tk.END

        )

    # ==========================================================
    # Delete Expense
    # ==========================================================

    def delete_expense(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(

                "Warning",

                "Please select a record."

            )

            return

        transaction_id = selected[0]

        self.db.execute(

            "DELETE FROM transactions WHERE id=?",

            (transaction_id,)

        )

        self.load_expenses()

        messagebox.showinfo(

            "Deleted",

            "Expense deleted successfully."

        )

    # ==========================================================
    # Refresh Page
    # ==========================================================

    def refresh(self):

        self.load_expenses()            