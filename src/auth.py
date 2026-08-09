import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from src.dashboard import Dashboard


# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"
PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
WHITE = "#FFFFFF"
TEXT = "#111827"
GRAY = "#6B7280"


class AuthScreen:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, root, database):

        self.root = root
        self.db = database

        self.logo = None

        self.create_layout()

        self.show_login()

    # ======================================================
    # Clear Window
    # ======================================================

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ======================================================
    # Clear Right Content
    # ======================================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ======================================================
    # Create Layout
    # ======================================================

    def create_layout(self):

        self.clear_screen()

        self.root.configure(bg=BACKGROUND)

        # Reset dashboard grid
        for i in range(10):

            self.root.grid_rowconfigure(i, weight=0)

            self.root.grid_columnconfigure(i, weight=0)

        self.root.grid_rowconfigure(0, weight=1)

        self.root.grid_columnconfigure(0, weight=1)

        # -----------------------------
        # Main Authentication Card
        # -----------------------------

        self.main_frame = tk.Frame(

            self.root,

            bg=WHITE,

            width=1050,

            height=560,

            highlightbackground="#D1D5DB",

            highlightthickness=1

        )

        self.main_frame.place(

            relx=0.5,

            rely=0.5,

            anchor="center"

        )

        self.main_frame.pack_propagate(False)

        self.main_frame.grid_rowconfigure(0, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=4)

        self.main_frame.grid_columnconfigure(1, weight=3)

        self.build_left_panel()

        self.build_right_panel()

    # ======================================================
    # Left Branding Panel
    # ======================================================

    def build_left_panel(self):

        self.left_panel = tk.Frame(

            self.main_frame,

            bg=PRIMARY,

            width=380

        )

        self.left_panel.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

        self.left_panel.grid_propagate(False)

        self.left_panel.grid_rowconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(6, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        # ----------------------------------
        # Logo
        # ----------------------------------

        try:

            image = Image.open("assets/logo.png")
            image = image.resize((300, 100), Image.LANCZOS)

            self.logo = ImageTk.PhotoImage(image)
            

            logo = tk.Label(

                self.left_panel,

                image=self.logo,

                bg=PRIMARY

            )

        except Exception:

            logo = tk.Label(

                self.left_panel,

                text="FinTrack Pro",

                bg=PRIMARY,

                fg="white",

                font=("Segoe UI", 28, "bold")

            )

        logo.grid(

            row=1,

            column=0,

            pady=(40,20)

        )

        # ----------------------------------
        # Heading
        # ----------------------------------

        heading = tk.Label(

            self.left_panel,

            text="Personal Finance\nManager",

            bg=PRIMARY,

            fg="white",

            justify="center",

            font=("Segoe UI",24,"bold")

        )

        heading.grid(

            row=2,

            column=0,

            pady=(20,15)

        )

        # ----------------------------------
        # Description
        # ----------------------------------

        description = tk.Label(

            self.left_panel,

            text=(

                "Track your income,\n"

                "expenses, budgets,\n"

                "and financial reports\n"

                "from one place."

            ),

            bg=PRIMARY,

            fg="white",

            justify="center",

            font=("Segoe UI",11)

        )

        description.grid(

            row=3,

            column=0,

            padx=40,

            pady=15

        )

        # ----------------------------------
        # Footer
        # ----------------------------------

        footer = tk.Label(

            self.left_panel,

            text="© FinTrack Pro 2026",

            bg=PRIMARY,

            fg="white",

            font=("Segoe UI",10)

        )

        footer.grid(

            row=5,

            column=0,

            pady=(20,40)

        )

    # ======================================================
    # Right Panel
    # ======================================================

    def build_right_panel(self):

        self.right_panel = tk.Frame(

            self.main_frame,

            bg=WHITE

        )

        self.right_panel.grid(

            row=0,

            column=1,

            sticky="nsew"

        )

        self.right_panel.grid_propagate(False)

        self.right_panel.grid_rowconfigure(
            0,
            weight=1
        )

        self.right_panel.grid_columnconfigure(
            0,
            weight=1
        )

        self.content_frame = tk.Frame(

            self.right_panel,

            bg=WHITE

        )

        self.content_frame.pack(

            expand=True,
            padx=40,
            pady=40
        )        
    # ======================================================
    # Login Screen
    # ======================================================

    def show_login(self):

        self.clear_content()

        self.content_frame.grid_columnconfigure(0, weight=1)

        # ----------------------------------
        # Heading
        # ----------------------------------

        title = tk.Label(

            self.content_frame,

            text="Welcome Back",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI", 24, "bold")

        )

        title.grid(
            row=0,
            column=0,
            pady=(0, 8)
        )

        subtitle = tk.Label(

            self.content_frame,

            text="Sign in to your FinTrack account",

            bg=WHITE,

            fg=GRAY,

            font=("Segoe UI", 11)

        )

        subtitle.grid(
            row=1,
            column=0,
            pady=(0, 40)
        )

        # ----------------------------------
        # Username
        # ----------------------------------

        tk.Label(

            self.content_frame,

            text="Username",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI", 10)

        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.username_entry = tk.Entry(

            self.content_frame,

            font=("Segoe UI", 12),

            width=34

        )

        self.username_entry.grid(

            row=3,

            column=0,

            ipady=10,

            pady=(0, 20)

        )

        # ----------------------------------
        # Password
        # ----------------------------------

        tk.Label(

            self.content_frame,

            text="Password",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI", 10)

        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.password_entry = tk.Entry(

            self.content_frame,

            show="*",

            font=("Segoe UI", 12),

            width=34

        )

        self.password_entry.grid(

            row=5,

            column=0,

            ipady=10,

            pady=(0, 25)

        )

        # Press Enter to Login

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

        # ----------------------------------
        # Login Button
        # ----------------------------------

        login_btn = tk.Button(

            self.content_frame,

            text="LOGIN",

            command=self.login,

            bg=PRIMARY,

            fg="white",

            activebackground=PRIMARY_DARK,

            activeforeground="white",

            relief="flat",

            cursor="hand2",

            font=("Segoe UI", 11, "bold"),

            width=30

        )

        login_btn.grid(

            row=6,

            column=0,

            ipady=10,

            pady=(0, 15)

        )

        # ----------------------------------
        # Register Button
        # ----------------------------------

        register_btn = tk.Button(

            self.content_frame,

            text="Create New Account",

            command=self.show_register,

            bg=WHITE,

            fg=PRIMARY,

            relief="flat",

            cursor="hand2",

            font=("Segoe UI", 10, "underline")

        )

        register_btn.grid(

            row=7,

            column=0

        )

        # Cursor starts in Username

        self.username_entry.focus_set()

    # ======================================================
    # Login
    # ======================================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:

            messagebox.showerror(

                "Login",

                "Please enter both username and password."

            )

            return

        user = self.db.fetch_one(

            """
            SELECT *
            FROM users
            WHERE username=? AND password=?
            """,

            (
                username,
                password
            )

        )

        if not user:

            messagebox.showerror(

                "Login Failed",

                "Invalid username or password."

            )

            return

        Dashboard(

            self.root,

            self.db,

            user

        )        
    # ======================================================
    # Register Screen
    # ======================================================

    def show_register(self):

        self.clear_content()

        self.content_frame.grid_columnconfigure(0, weight=1)

        title = tk.Label(

            self.content_frame,

            text="Create Account",

            font=("Segoe UI", 28, "bold"),

            bg=WHITE,

            fg=TEXT

        )

        title.grid(

            row=0,

            column=0,

            pady=(0,10)

        )

        subtitle = tk.Label(

            self.content_frame,

            text="Create your FinTrack Pro account",

            font=("Segoe UI",11),

            bg=WHITE,

            fg=GRAY

        )

        subtitle.grid(

            row=1,

            column=0,

            pady=(0,30)

        )

        # --------------------------------------------------
        # Username
        # --------------------------------------------------

        tk.Label(

            self.content_frame,

            text="Username",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI",10)

        ).grid(

            row=2,

            column=0,

            sticky="w",

            pady=(0,5)

        )

        self.reg_username = tk.Entry(

            self.content_frame,

            font=("Segoe UI",12),

            width=34

        )

        self.reg_username.grid(

            row=3,

            column=0,

            ipady=10,

            pady=(0,20)

        )

        # --------------------------------------------------
        # Password
        # --------------------------------------------------

        tk.Label(

            self.content_frame,

            text="Password",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI",10)

        ).grid(

            row=4,

            column=0,

            sticky="w",

            pady=(0,5)

        )

        self.reg_password = tk.Entry(

            self.content_frame,

            show="*",

            font=("Segoe UI",12),

            width=34

        )

        self.reg_password.grid(

            row=5,

            column=0,

            ipady=10,

            pady=(0,20)

        )

        # --------------------------------------------------
        # Confirm Password
        # --------------------------------------------------

        tk.Label(

            self.content_frame,

            text="Confirm Password",

            bg=WHITE,

            fg=TEXT,

            font=("Segoe UI",10)

        ).grid(

            row=6,

            column=0,

            sticky="w",

            pady=(0,5)

        )

        self.confirm_password = tk.Entry(

            self.content_frame,

            show="*",

            font=("Segoe UI",12),

            width=34

        )

        self.confirm_password.grid(

            row=7,

            column=0,

            ipady=10,

            pady=(0,30)

        )

        self.confirm_password.bind(

            "<Return>",

            lambda event: self.register()

        )

        # --------------------------------------------------
        # Register Button
        # --------------------------------------------------

        register_btn = tk.Button(

            self.content_frame,

            text="CREATE ACCOUNT",

            command=self.register,

            bg=PRIMARY,

            fg="white",

            activebackground=PRIMARY_DARK,

            activeforeground="white",

            relief="flat",

            cursor="hand2",

            font=("Segoe UI",11,"bold"),

            width=30

        )

        register_btn.grid(

            row=8,

            column=0,

            ipady=10

        )

        # --------------------------------------------------
        # Back Button
        # --------------------------------------------------

        back_btn = tk.Button(

            self.content_frame,

            text="← Back to Login",

            command=self.show_login,

            bg=WHITE,

            fg=PRIMARY,

            relief="flat",

            cursor="hand2",

            font=("Segoe UI",10,"underline")

        )

        back_btn.grid(

            row=9,

            column=0,

            pady=20

        )

        self.reg_username.focus_set()

    # ======================================================
    # Register
    # ======================================================

    def register(self):

        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        confirm = self.confirm_password.get().strip()

        if not username or not password or not confirm:

            messagebox.showerror(

                "Registration",

                "Please fill all fields."

            )

            return

        if len(username) < 4:

            messagebox.showerror(

                "Registration",

                "Username must contain at least 4 characters."

            )

            return

        if len(password) < 6:

            messagebox.showerror(

                "Registration",

                "Password must contain at least 6 characters."

            )

            return

        if password != confirm:

            messagebox.showerror(

                "Registration",

                "Passwords do not match."

            )

            return

        existing = self.db.fetch_one(

            """
            SELECT id
            FROM users
            WHERE username=?
            """,

            (username,)

        )

        if existing:

            messagebox.showerror(

                "Registration",

                "Username already exists."

            )

            return

        self.db.execute(

            """
            INSERT INTO users
            (
                username,
                password
            )
            VALUES
            (
                ?,?
            )
            """,

            (
                username,
                password
            )

        )

        messagebox.showinfo(

            "Success",

            "Account created successfully."

        )

        self.show_login()        