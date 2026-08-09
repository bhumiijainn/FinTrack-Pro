import tkinter as tk
from tkinter import messagebox
from src.components.sidebar import Sidebar
from src.components.header import Header
from src.pages.dashboard_page import DashboardPage
from src.pages.income import IncomePage
from src.pages.expense import ExpensePage
from src.pages.reports import ReportsPage
from src.pages.charts import ChartsPage
from src.pages.search import SearchPage
from src.pages.budget import BudgetPage
from src.pages.settings import SettingsPage


# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"


class Dashboard:

    def __init__(self, root, database, user):

        self.root = root
        self.db = database
        self.user = user

        self.build_dashboard()

    # ==========================================================
    # Clear Window
    # ==========================================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================================
    # Build Dashboard
    # ==========================================================

    def build_dashboard(self):

        self.clear_window()

        self.root.configure(bg=BACKGROUND)

        self.root.grid_rowconfigure(0, weight=1)

# Fixed sidebar column
        self.root.grid_columnconfigure(
            0,
            weight=0,
            minsize=280
        )

# Expandable content column
        self.root.grid_columnconfigure(
            1,
            weight=1
        )
       

        self.create_sidebar()

        self.create_main_area()

        self.load_default_page()

    # ==========================================================
    # Sidebar
    # ==========================================================

    def create_sidebar(self):

        commands = {

            "Dashboard": self.show_dashboard,

            "Income": self.show_income,

            "Expense": self.show_expense,

            "Reports": self.show_reports,

            "Charts": self.show_charts,

            "Search": self.show_search,

            "Budget": self.show_budget,

            "Settings": self.show_settings,

            "Logout": self.logout

        }

        self.sidebar = Sidebar(

            self.root,

            active_page="Dashboard",

            commands=commands

        )

        self.sidebar.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

# Keep sidebar fixed
        self.sidebar.configure(width=280)
        self.sidebar.grid_propagate(False)
    # ==========================================================
    # Main Area
    # ==========================================================

    def create_main_area(self):

        self.main_frame = tk.Frame(

            self.root,

            bg=BACKGROUND

        )

        self.main_frame.grid(

            row=0,

            column=1,

            sticky="nsew"

        )

        self.main_frame.grid_rowconfigure(1, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.create_header()

        self.create_content_frame()
    # ==========================================================
    # Header
    # ==========================================================

    def create_header(self):

        self.header = Header(

            self.main_frame,

            title="Dashboard",

            username=self.user["username"]

        )

        self.header.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=20,

            pady=(20, 10)

        )

    # ==========================================================
    # Content Frame
    # ==========================================================

    def create_content_frame(self):

        self.content_frame = tk.Frame(

            self.main_frame,

            bg=BACKGROUND

        )

        self.content_frame.grid(

            row=1,

            column=0,

            sticky="nsew",

            padx=20,

            pady=(0, 20)

        )

        self.content_frame.grid_rowconfigure(0, weight=1)

        self.content_frame.grid_columnconfigure(0, weight=1)

    # ==========================================================
    # Clear Current Page
    # ==========================================================

    def clear_page(self):

        for widget in self.content_frame.winfo_children():

            widget.destroy()

    # ==========================================================
    # Load Page
    # ==========================================================

    def load_page(self, page_class, title):

        self.sidebar.set_active(title)

        self.header.update_title(title)

        self.clear_page()

        self.current_page = page_class(

            self.content_frame,

            self.db,

            self.user

        )

    # ==========================================================
    # Get Current User
    # ==========================================================

    def get_user(self):

        return self.user

    # ==========================================================
    # Get Database
    # ==========================================================

    def get_database(self):

        return self.db        
    # ==========================================================
    # Dashboard
    # ==========================================================

    def show_dashboard(self):

        self.load_page(
            DashboardPage,
            "Dashboard"
        )

    # ==========================================================
    # Income
    # ==========================================================

    def show_income(self):

        self.load_page(
            IncomePage,
            "Income"
        )

    # ==========================================================
    # Expense
    # ==========================================================

    def show_expense(self):

        self.load_page(
            ExpensePage,
            "Expense"
        )

    # ==========================================================
    # Reports
    # ==========================================================

    def show_reports(self):

        self.load_page(
            ReportsPage,
            "Reports"
        )

    # ==========================================================
    # Charts
    # ==========================================================

    def show_charts(self):

        self.load_page(
            ChartsPage,
            "Charts"
        )

    # ==========================================================
    # Search
    # ==========================================================

    def show_search(self):

        self.load_page(
            SearchPage,
            "Search"
        )

    # ==========================================================
    # Budget Planner
    # ==========================================================

    def show_budget(self):

        self.load_page(
            BudgetPage,
            "Budget"
        )

    # ==========================================================
    # Settings
    # ==========================================================

    def show_settings(self):

        self.load_page(
            SettingsPage,
            "Settings"
        )    
    # ==========================================================
    # Logout
    # ==========================================================

    def logout(self):

        

        if not messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        ):
            return

        # Destroy all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reset grid configuration
        for i in range(20):
            self.root.grid_rowconfigure(i, weight=0)
            self.root.grid_columnconfigure(i, weight=0)

        self.root.configure(bg="white")

        # Open login screen
        from src.auth import AuthScreen

        AuthScreen(
            self.root,
            self.db
        )
    # ==========================================================
    # Refresh Current Page
    # ==========================================================

    def refresh_current_page(self):

        current = self.sidebar.active_page

        pages = {

            "Dashboard": self.show_dashboard,

            "Income": self.show_income,

            "Expense": self.show_expense,

            "Reports": self.show_reports,

            "Charts": self.show_charts,

            "Search": self.show_search,

            "Budget": self.show_budget,

            "Settings": self.show_settings

        }

        if current in pages:

            pages[current]()

    # ==========================================================
    # Load Default Page
    # ==========================================================

    def load_default_page(self):

        self.show_dashboard()

    # ==========================================================
    # Window Resize Handler
    # ==========================================================

    def on_resize(self, event=None):

        self.root.update_idletasks()

    # ==========================================================
    # Set Window Title
    # ==========================================================

    def set_title(self, title):

        self.root.title(f"FinTrack Pro - {title}")

    # ==========================================================
    # Close Dashboard
    # ==========================================================

    def close(self):

        self.root.destroy()        