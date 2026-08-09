import tkinter as tk
from tkinter import ttk

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
TEXT = "#111827"
GRAY = "#6B7280"


class SearchPage:

    def __init__(self, parent, db, user):

        self.parent = parent
        self.db = db
        self.user = user

        self.build_page()

    # ==========================================================
    # Build Search Page
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

        self.build_search_bar()

        self.build_table()

    # ==========================================================
    # Search Panel
    # ==========================================================

    def build_search_bar(self):

        panel = tk.LabelFrame(
            self.frame,
            text="Search Transactions",
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

        for i in range(5):
            panel.grid_columnconfigure(i, weight=1)

        # -----------------------------------
        # Search Keyword
        # -----------------------------------

        tk.Label(
            panel,
            text="Keyword",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.keyword = tk.Entry(
            panel,
            font=("Segoe UI", 10)
        )

        self.keyword.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # -----------------------------------
        # Filter Type
        # -----------------------------------

        tk.Label(
            panel,
            text="Search By",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.filter_type = ttk.Combobox(
            panel,
            state="readonly",
            values=[
                "All",
                "Date",
                "Type",
                "Category",
                "Amount",
                "Description"
            ]
        )

        self.filter_type.current(0)

        self.filter_type.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew"
        )

        # -----------------------------------
        # Search Button
        # -----------------------------------

        search_btn = tk.Button(
            panel,
            text="Search",
            command=self.perform_search,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )

        search_btn.grid(
            row=1,
            column=2,
            padx=10,
            sticky="ew"
        )

        # -----------------------------------
        # Clear Button
        # -----------------------------------

        clear_btn = tk.Button(
            panel,
            text="Clear",
            command=self.clear_search,
            bg="#DC2626",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )

        clear_btn.grid(
            row=1,
            column=3,
            padx=5,
            sticky="ew"
        )

        # -----------------------------------
        # Refresh Button
        # -----------------------------------

        refresh_btn = tk.Button(
            panel,
            text="Refresh",
            command=self.refresh,
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        )

        refresh_btn.grid(
            row=1,
            column=4,
            padx=5,
            sticky="ew"
        )

    # ==========================================================
    # Transaction Table
    # ==========================================================

    def build_table(self):

        table_frame = tk.LabelFrame(
            self.frame,
            text="Search Results",
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
        # Transaction Table
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

        # ---------------------------------------
        # Headings
        # ---------------------------------------

        for col in columns:

            self.table.heading(
                col,
                text=col
            )

        # ---------------------------------------
        # Column Width
        # ---------------------------------------

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
            width=160,
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

        # ---------------------------------------
        # Scrollbar
        # ---------------------------------------

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

        # Load Transactions

        self.load_transactions()

    # ==========================================================
    # Load Transactions
    # ==========================================================

    def load_transactions(self):

        # Clear existing rows

        for item in self.table.get_children():

            self.table.delete(item)

        rows = self.db.fetch_all(

            """
            SELECT
                id,
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

                iid=row["id"],

                values=(

                    row["date"],

                    row["type"],

                    row["category"],

                    f"₹{row['amount']:,.2f}",

                    row["description"]

                )

            )
    # ==========================================================
    # Search Transactions
    # ==========================================================

    def search_transactions(self):

        keyword = self.keyword.get().strip()
        search_by = self.filter_type.get()

        # Clear Table
        for item in self.table.get_children():
            self.table.delete(item)

        if search_by == "All":

            query = """
                SELECT
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE user_id=?
                AND (
                    date LIKE ?
                    OR type LIKE ?
                    OR category LIKE ?
                    OR CAST(amount AS TEXT) LIKE ?
                    OR description LIKE ?
                )
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%"
            )

        elif search_by == "Date":

            query = """
                SELECT
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND date LIKE ?
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                f"%{keyword}%"
            )

        elif search_by == "Type":

            query = """
                SELECT
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND type LIKE ?
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                f"%{keyword}%"
            )

        elif search_by == "Category":

            query = """
                SELECT
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND category LIKE ?
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                f"%{keyword}%"
            )

        elif search_by == "Amount":

            query = """
                SELECT
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND CAST(amount AS TEXT) LIKE ?
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                f"%{keyword}%"
            )

        elif search_by == "Description":

            query = """
                SELECT
                    id,
                    date,
                    type,
                    category,
                    amount,
                    description
                FROM transactions
                WHERE
                    user_id=?
                    AND description LIKE ?
                ORDER BY id DESC
            """

            params = (
                self.user["id"],
                f"%{keyword}%"
            )

        else:
            return

        rows = self.db.fetch_all(query, params)

        for row in rows:

            self.table.insert(

                "",

                tk.END,

                iid=row["id"],

                values=(

                    row["date"],

                    row["type"],

                    row["category"],

                    f"₹{row['amount']:,.2f}",

                    row["description"]

                )

            )            
    # ==========================================================
    # Clear Search
    # ==========================================================

    def clear_search(self):

        self.keyword.delete(0, tk.END)

        self.filter_type.current(0)

        self.load_transactions()

    # ==========================================================
    # Refresh Page
    # ==========================================================

    def refresh(self):

        self.clear_search()

    # ==========================================================
    # Live Search
    # ==========================================================

    def enable_live_search(self):

        self.keyword.bind(
            "<KeyRelease>",
            lambda event: self.search_transactions()
        )

    # ==========================================================
    # Result Count
    # ==========================================================

    def update_result_count(self):

        count = len(self.table.get_children())

        if hasattr(self, "result_label"):

            self.result_label.config(
                text=f"Results Found: {count}"
            )

    # ==========================================================
    # Show No Results Message
    # ==========================================================

    def show_no_results(self):

        if len(self.table.get_children()) == 0:

            self.table.insert(
                "",
                tk.END,
                values=(
                    "-",
                    "-",
                    "No matching records found",
                    "-",
                    "-"
                )
            )

    # ==========================================================
    # Search Wrapper
    # ==========================================================

    def perform_search(self):

        self.search_transactions()

        self.update_result_count()

        self.show_no_results()            