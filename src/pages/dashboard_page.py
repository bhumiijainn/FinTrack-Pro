import tkinter as tk
from tkinter import ttk

from src.components.card import InfoCard

BACKGROUND = "#F4F7FC"
WHITE = "#FFFFFF"


class DashboardPage:

    def __init__(self, parent, db, user):

        self.parent = parent
        self.db = db
        self.user = user

        self.build()

    # ==========================================================
    # Build Dashboard
    # ==========================================================

    def build(self):

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

        self.create_cards()

        self.create_body()

    # ==========================================================
    # Database Helper Methods
    # ==========================================================

    def get_total_income(self):

        row = self.db.fetch_one(

            """
            SELECT
                IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Income'
            """,

            (self.user["id"],)

        )

        return row["total"]

    def get_total_expense(self):

        row = self.db.fetch_one(

            """
            SELECT
                IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Expense'
            """,

            (self.user["id"],)

        )

        return row["total"]

    def get_balance(self):

        return self.get_total_income() - self.get_total_expense()

    def get_savings(self):

        return self.get_balance()

    # ==========================================================
    # Dashboard Cards
    # ==========================================================

    def create_cards(self):

        cards_frame = tk.Frame(
            self.frame,
            bg=BACKGROUND
        )

        cards_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0,20)
        )

        for i in range(4):

            cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        balance = self.get_balance()
        income = self.get_total_income()
        expense = self.get_total_expense()
        savings = self.get_savings()

        InfoCard(
            cards_frame,
            title="Balance",
            value=f"₹{balance:,.2f}",
            subtitle="Current Balance",
            accent="#2563EB"
        ).grid(
            row=0,
            column=0,
            padx=10,
            sticky="ew"
        )

        InfoCard(
            cards_frame,
            title="Income",
            value=f"₹{income:,.2f}",
            subtitle="Total Income",
            accent="#16A34A"
        ).grid(
            row=0,
            column=1,
            padx=10,
            sticky="ew"
        )

        InfoCard(
            cards_frame,
            title="Expense",
            value=f"₹{expense:,.2f}",
            subtitle="Total Expense",
            accent="#DC2626"
        ).grid(
            row=0,
            column=2,
            padx=10,
            sticky="ew"
        )

        InfoCard(
            cards_frame,
            title="Savings",
            value=f"₹{savings:,.2f}",
            subtitle="Available",
            accent="#F59E0B"
        ).grid(
            row=0,
            column=3,
            padx=10,
            sticky="ew"
        )
    # ==========================================================
    # Dashboard Body
    # ==========================================================

    def create_body(self):

        body = tk.Frame(
            self.frame,
            bg=BACKGROUND
        )

        body.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.create_transaction_table(body)

        self.create_analytics(body)

    # ==========================================================
    # Recent Transactions
    # ==========================================================

    def create_transaction_table(self, parent):

        transactions = tk.LabelFrame(

            parent,

            text="Recent Transactions",

            bg=WHITE,

            font=("Segoe UI", 11, "bold")

        )

        transactions.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=(0, 10)

        )

        columns = (

            "Date",

            "Type",

            "Category",

            "Amount"

        )

        self.table = ttk.Treeview(

            transactions,

            columns=columns,

            show="headings",

            height=16

        )

        # -------------------------------------
        # Headings
        # -------------------------------------

        for col in columns:

            self.table.heading(
                col,
                text=col
            )

        # -------------------------------------
        # Column Width
        # -------------------------------------

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
            width=180,
            anchor="center"
        )

        self.table.column(
            "Amount",
            width=120,
            anchor="center"
        )

        # -------------------------------------
        # Scrollbar
        # -------------------------------------

        scrollbar = ttk.Scrollbar(

            transactions,

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

        self.load_transactions()

    # ==========================================================
    # Load Transactions
    # ==========================================================

    def load_transactions(self):

        for item in self.table.get_children():

            self.table.delete(item)

        rows = self.db.fetch_all(

            """
            SELECT
                date,
                type,
                category,
                amount
            FROM transactions
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 10
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

                    f"₹{row['amount']:,.2f}"

                )

            )        
    # ==========================================================
    # Monthly Analytics
    # ==========================================================

    def create_analytics(self, parent):

        analytics = tk.LabelFrame(
            parent,
            text="Monthly Analytics",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=20
        )

        analytics.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        analytics.grid_columnconfigure(0, weight=1)

        income = self.get_total_income()
        expense = self.get_total_expense()
        balance = self.get_balance()

        transactions = self.db.fetch_one(

            """
            SELECT COUNT(*) AS total
            FROM transactions
            WHERE user_id=?
            """,

            (self.user["id"],)

        )["total"]

        total_flow = income + expense

        if total_flow == 0:

            income_percent = 0
            expense_percent = 0

        else:

            income_percent = int((income / total_flow) * 100)
            expense_percent = int((expense / total_flow) * 100)

        # ---------------------------------------
        # Statistics
        # ---------------------------------------

        self.stat_card(
            analytics,
            "Total Transactions",
            str(transactions),
            0
        )

        self.stat_card(
            analytics,
            "Income",
            f"₹{income:,.2f}",
            1
        )

        self.stat_card(
            analytics,
            "Expense",
            f"₹{expense:,.2f}",
            2
        )

        self.stat_card(
            analytics,
            "Current Balance",
            f"₹{balance:,.2f}",
            3
        )

        # ---------------------------------------
        # Income Progress
        # ---------------------------------------

        tk.Label(

            analytics,

            text=f"Income Ratio ({income_percent}%)",

            bg=WHITE,

            anchor="w",

            font=("Segoe UI",10)

        ).grid(

            row=4,

            column=0,

            sticky="ew",

            pady=(20,5)

        )

        income_bar = ttk.Progressbar(

            analytics,

            length=250,

            maximum=100,

            value=income_percent

        )

        income_bar.grid(

            row=5,

            column=0,

            sticky="ew"

        )

        # ---------------------------------------
        # Expense Progress
        # ---------------------------------------

        tk.Label(

            analytics,

            text=f"Expense Ratio ({expense_percent}%)",

            bg=WHITE,

            anchor="w",

            font=("Segoe UI",10)

        ).grid(

            row=6,

            column=0,

            sticky="ew",

            pady=(20,5)

        )

        expense_bar = ttk.Progressbar(

            analytics,

            length=250,

            maximum=100,

            value=expense_percent

        )

        expense_bar.grid(

            row=7,

            column=0,

            sticky="ew"

        )

        # ---------------------------------------
        # Financial Status
        # ---------------------------------------

        if balance > 0:

            status = "🟢 Your finances are healthy."

        elif balance == 0:

            status = "🟡 Break-even."

        else:

            status = "🔴 Expenses exceed income."

        tk.Label(

            analytics,

            text=status,

            bg=WHITE,

            fg="#2563EB",

            font=("Segoe UI",10,"bold"),

            wraplength=250,

            justify="left"

        ).grid(

            row=8,

            column=0,

            sticky="w",

            pady=(25,0)

        )

    # ==========================================================
    # Statistic Card
    # ==========================================================

    def stat_card(self, parent, title, value, row):

        card = tk.Frame(
            parent,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        card.grid(
            row=row,
            column=0,
            sticky="ew",
            pady=5
        )

        tk.Label(

            card,

            text=title,

            bg="#F8FAFC",

            fg="gray",

            font=("Segoe UI",9)

        ).pack(
            anchor="w",
            padx=12,
            pady=(10,2)
        )

        tk.Label(

            card,

            text=value,

            bg="#F8FAFC",

            fg="#111827",

            font=("Segoe UI",15,"bold")

        ).pack(
            anchor="w",
            padx=12,
            pady=(0,10)
        )

    # ==========================================================
    # Refresh Dashboard
    # ==========================================================

    def refresh(self):

        self.frame.destroy()

        self.build()            
    # ==========================================================
    # Quick Actions
    # ==========================================================

    def create_quick_actions(self, parent):

        actions = tk.LabelFrame(
            parent,
            text="Quick Actions",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )

        actions.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0)
        )

        actions.grid_columnconfigure((0, 1, 2, 3), weight=1)

        tk.Button(
            actions,
            text="➕ Add Income",
            bg="#16A34A",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=5,
            sticky="ew"
        )

        tk.Button(
            actions,
            text="➖ Add Expense",
            bg="#DC2626",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=5,
            sticky="ew"
        )

        tk.Button(
            actions,
            text="📊 Reports",
            bg="#2563EB",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).grid(
            row=0,
            column=2,
            padx=8,
            pady=5,
            sticky="ew"
        )

        tk.Button(
            actions,
            text="📈 Charts",
            bg="#F59E0B",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).grid(
            row=0,
            column=3,
            padx=8,
            pady=5,
            sticky="ew"
        )

    # ==========================================================
    # Recent Activity
    # ==========================================================

    def create_recent_activity(self, parent):

        activity = tk.LabelFrame(
            parent,
            text="Recent Activity",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=15
        )

        activity.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0)
        )

        rows = self.db.fetch_all(
            """
            SELECT type,category,amount,date
            FROM transactions
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 5
            """,
            (self.user["id"],)
        )

        if not rows:

            tk.Label(
                activity,
                text="No recent activity.",
                bg=WHITE,
                fg="gray",
                font=("Segoe UI", 10)
            ).pack(anchor="w")

            return

        for row in rows:

            color = "#16A34A" if row["type"] == "Income" else "#DC2626"

            text = (
                f"{row['date']}    "
                f"{row['type']} • "
                f"{row['category']} • "
                f"₹{row['amount']:,.2f}"
            )

            tk.Label(
                activity,
                text=text,
                bg=WHITE,
                fg=color,
                anchor="w",
                font=("Segoe UI", 10)
            ).pack(
                fill="x",
                pady=3
            )        