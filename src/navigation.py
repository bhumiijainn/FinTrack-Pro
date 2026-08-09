from src.dashboard import Dashboard
from src.income import Income
from src.expense import Expense
from src.reports import Reports
from src.charts import Charts
from src.search import Search


class Navigation:
    def __init__(self, root, database, user):
        self.root = root
        self.db = database
        self.user = user

    # -------------------------
    # Dashboard
    # -------------------------

    def open_dashboard(self):
        Dashboard(
            self.root,
            self.db,
            self.user,
            self
        )

    # -------------------------
    # Income
    # -------------------------

    def open_income(self):
        Income(
            self.root,
            self.db,
            self.user,
            self
        )

    # -------------------------
    # Expense
    # -------------------------

    def open_expense(self):
        Expense(
            self.root,
            self.db,
            self.user,
            self
        )

    # -------------------------
    # Reports
    # -------------------------

    def open_reports(self):
        Reports(
            self.root,
            self.db,
            self.user,
            self
        )

    # -------------------------
    # Charts
    # -------------------------

    def open_charts(self):
        Charts(
            self.root,
            self.db,
            self.user,
            self
        )

    # -------------------------
    # Search
    # -------------------------

    def open_search(self):
        Search(
            self.root,
            self.db,
            self.user,
            self
        )