import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"


class ChartsPage:

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
        self.frame.grid_rowconfigure(1, weight=1)

        self.build_toolbar()

        self.build_chart_area()

    # ==========================================================
    # Toolbar
    # ==========================================================

    def build_toolbar(self):

        toolbar = tk.LabelFrame(
            self.frame,
            text="Charts",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=15
        )

        toolbar.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        toolbar.grid_columnconfigure(1, weight=1)

        tk.Label(
            toolbar,
            text="Select Chart",
            bg=WHITE,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        self.chart_type = ttk.Combobox(
            toolbar,
            state="readonly",
            values=[
                "Income vs Expense",
                "Expense by Category",
                "Monthly Income",
                "Monthly Expense",
                "Balance Trend"
            ]
        )

        self.chart_type.current(0)

        self.chart_type.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        generate = tk.Button(
            toolbar,
            text="Generate",
            command=self.generate_chart,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )

        generate.grid(
            row=0,
            column=2,
            padx=10
        )

        refresh = tk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh,
            bg="#16A34A",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )

        refresh.grid(
            row=0,
            column=3
        )

    # ==========================================================
    # Chart Area
    # ==========================================================

    def build_chart_area(self):

        self.chart_frame = tk.Frame(
            self.frame,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        self.chart_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)

        self.figure = Figure(
            figsize=(8, 5),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.chart_frame
        )

        self.canvas.get_tk_widget().grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.generate_chart()
    # ==========================================================
    # Generate Chart
    # ==========================================================

    def generate_chart(self):

        chart = self.chart_type.get()

        self.ax.clear()

        if chart == "Income vs Expense":

            self.income_vs_expense()

        elif chart == "Expense by Category":

            self.expense_by_category()

        elif chart == "Monthly Income":

            self.monthly_income()

        elif chart == "Monthly Expense":

            self.monthly_expense()

        elif chart == "Balance Trend":

            self.balance_trend()

        self.canvas.draw()

    # ==========================================================
    # Income vs Expense
    # ==========================================================

    def income_vs_expense(self):

        income = self.db.fetch_one(

            """
            SELECT IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Income'
            """,

            (self.user["id"],)

        )["total"]

        expense = self.db.fetch_one(

            """
            SELECT IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Expense'
            """,

            (self.user["id"],)

        )["total"]

        labels = ["Income", "Expense"]

        values = [income, expense]

        colors = ["#16A34A", "#DC2626"]

        self.ax.bar(
            labels,
            values,
            color=colors,
            width=0.5
        )

        self.ax.set_title(
            "Income vs Expense",
            fontsize=14,
            weight="bold"
        )

        self.ax.set_ylabel("Amount (₹)")

        for i, value in enumerate(values):

            self.ax.text(

                i,

                value,

                f"₹{value:,.0f}",

                ha="center",

                va="bottom",

                fontsize=10,

                fontweight="bold"

            )

    # ==========================================================
    # Expense by Category
    # ==========================================================

    def expense_by_category(self):

        rows = self.db.fetch_all(

            """
            SELECT
                category,
                SUM(amount) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Expense'
            GROUP BY category
            """,

            (self.user["id"],)

        )

        if not rows:

            self.ax.text(

                0.5,

                0.5,

                "No Expense Data",

                ha="center",

                va="center",

                fontsize=16

            )

            self.ax.set_axis_off()

            return

        categories = []

        amounts = []

        for row in rows:

            categories.append(row["category"])

            amounts.append(row["total"])

        self.ax.pie(

            amounts,

            labels=categories,

            autopct="%1.1f%%",

            startangle=90

        )

        self.ax.set_title(

            "Expense by Category",

            fontsize=14,

            weight="bold"

        )        
    # ==========================================================
    # Monthly Income Trend
    # ==========================================================

    def monthly_income(self):

        rows = self.db.fetch_all(

            """
            SELECT
                substr(date,4,7) AS month,
                SUM(amount) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Income'
            GROUP BY month
            ORDER BY month
            """,

            (self.user["id"],)

        )

        if not rows:

            self.ax.text(
                0.5,
                0.5,
                "No Income Data",
                ha="center",
                va="center",
                fontsize=16
            )

            self.ax.set_axis_off()

            return

        months = []
        totals = []

        for row in rows:

            months.append(row["month"])
            totals.append(row["total"])

        self.ax.plot(
            months,
            totals,
            marker="o",
            linewidth=2
        )

        self.ax.set_title(
            "Monthly Income Trend",
            fontsize=14,
            weight="bold"
        )

        self.ax.set_xlabel("Month")

        self.ax.set_ylabel("Income (₹)")

        self.ax.grid(True)

    # ==========================================================
    # Monthly Expense Trend
    # ==========================================================

    def monthly_expense(self):

        rows = self.db.fetch_all(

            """
            SELECT
                substr(date,4,7) AS month,
                SUM(amount) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Expense'
            GROUP BY month
            ORDER BY month
            """,

            (self.user["id"],)

        )

        if not rows:

            self.ax.text(
                0.5,
                0.5,
                "No Expense Data",
                ha="center",
                va="center",
                fontsize=16
            )

            self.ax.set_axis_off()

            return

        months = []
        totals = []

        for row in rows:

            months.append(row["month"])
            totals.append(row["total"])

        self.ax.plot(
            months,
            totals,
            marker="o",
            linewidth=2
        )

        self.ax.set_title(
            "Monthly Expense Trend",
            fontsize=14,
            weight="bold"
        )

        self.ax.set_xlabel("Month")

        self.ax.set_ylabel("Expense (₹)")

        self.ax.grid(True)

    # ==========================================================
    # Balance Trend
    # ==========================================================

    def balance_trend(self):

        income = self.db.fetch_one(

            """
            SELECT IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Income'
            """,

            (self.user["id"],)

        )["total"]

        expense = self.db.fetch_one(

            """
            SELECT IFNULL(SUM(amount),0) AS total
            FROM transactions
            WHERE
                user_id=?
                AND type='Expense'
            """,

            (self.user["id"],)

        )["total"]

        balance = income - expense

        labels = ["Income", "Expense", "Balance"]

        values = [income, expense, balance]

        colors = ["#16A34A", "#DC2626", "#2563EB"]

        self.ax.bar(
            labels,
            values,
            color=colors
        )

        self.ax.set_title(
            "Financial Overview",
            fontsize=14,
            weight="bold"
        )

        self.ax.set_ylabel("Amount (₹)")

        for i, value in enumerate(values):

            self.ax.text(
                i,
                value,
                f"₹{value:,.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            ) 
    # ==========================================================
    # Refresh Charts
    # ==========================================================

    def refresh(self):

        self.chart_type.current(0)

        self.generate_chart()

    # ==========================================================
    # Clear Current Chart
    # ==========================================================

    def clear_chart(self):

        self.ax.clear()

        self.canvas.draw()

    # ==========================================================
    # Redraw Canvas
    # ==========================================================

    def redraw(self):

        self.canvas.draw_idle()

    # ==========================================================
    # Resize Chart
    # ==========================================================

    def resize_chart(self, event=None):

        self.figure.tight_layout()

        self.canvas.draw_idle()

    # ==========================================================
    # Save Chart (PNG)
    # ==========================================================

    def save_chart(self):

        from tkinter import filedialog, messagebox

        file = filedialog.asksaveasfilename(

            defaultextension=".png",

            filetypes=[

                ("PNG Image", "*.png"),

                ("JPEG Image", "*.jpg")

            ]

        )

        if not file:

            return

        self.figure.savefig(

            file,

            dpi=300,

            bbox_inches="tight"

        )

        messagebox.showinfo(

            "Success",

            "Chart saved successfully."

        )

    # ==========================================================
    # Export Chart PDF (Future)
    # ==========================================================

    def export_pdf(self):

        from tkinter import messagebox

        messagebox.showinfo(

            "Coming Soon",

            "Export to PDF will be available in the next version."

        )

    # ==========================================================
    # Export Excel (Future)
    # ==========================================================

    def export_excel(self):

        from tkinter import messagebox

        messagebox.showinfo(

            "Coming Soon",

            "Export to Excel will be available in the next version."

        )

    # ==========================================================
    # Export CSV (Future)
    # ==========================================================

    def export_csv(self):

        from tkinter import messagebox

        messagebox.showinfo(

            "Coming Soon",

            "Export to CSV will be available in the next version."

        )                   