import tkinter as tk
from datetime import datetime

# ==========================================================
# COLORS
# ==========================================================

HEADER_BG = "#FFFFFF"

BACKGROUND = "#F4F7FC"

PRIMARY = "#2563EB"

TEXT = "#111827"

GRAY = "#6B7280"

BORDER = "#E5E7EB"


class Header(tk.Frame):

    def __init__(
        self,
        parent,
        title="Dashboard",
        username="User"
    ):

        super().__init__(
            parent,
            bg=HEADER_BG,
            height=90,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0
        )

        self.title = title

        self.username = username

        self.grid_propagate(False)

        self.build_header()

    # ==========================================================
    # Build Header
    # ==========================================================

    def build_header(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.build_left()

        self.build_right()
    # ==========================================================
    # Left Section
    # ==========================================================

    def build_left(self):

        left = tk.Frame(
            self,
            bg=HEADER_BG
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25
        )

        # --------------------------------------
        # Page Title
        # --------------------------------------

        self.title_label = tk.Label(

            left,

            text=self.title,

            bg=HEADER_BG,

            fg=TEXT,

            font=("Segoe UI", 24, "bold")

        )

        self.title_label.pack(
            anchor="w"
        )

        # --------------------------------------
        # Today's Date
        # --------------------------------------

        today = datetime.now().strftime("%A, %d %B %Y")

        self.date_label = tk.Label(

            left,

            text=today,

            bg=HEADER_BG,

            fg=GRAY,

            font=("Segoe UI", 10)

        )

        self.date_label.pack(
            anchor="w",
            pady=(3,0)
        )

    # ==========================================================
    # Right Section
    # ==========================================================

    def build_right(self):

        right = tk.Frame(
            self,
            bg=HEADER_BG
        )

        right.grid(
            row=0,
            column=1,
            sticky="e",
            padx=25
        )


        # --------------------------------------
        # Avatar
        # --------------------------------------

        self.avatar = tk.Canvas(

            right,

            width=42,

            height=42,

            bg=HEADER_BG,

            highlightthickness=0

        )

        self.avatar.grid(
            row=0,
            column=2,
            padx=(0,10)
        )

        self.avatar.create_oval(

            2,
            2,
            40,
            40,

            fill=PRIMARY,

            outline=""

        )

        self.avatar.create_text(

            21,

            21,

            text=self.username[:1].upper(),

            fill="white",

            font=("Segoe UI",14,"bold")

        )

        # --------------------------------------
        # Welcome Label
        # --------------------------------------

        self.username_label = tk.Label(

            right,

            text=f"Welcome, {self.username}",

            bg=HEADER_BG,

            fg=TEXT,

            font=("Segoe UI",11,"bold")

        )

        self.username_label.grid(
            row=0,
            column=3
        )        
    # ==========================================================
    # Update Page Title
    # ==========================================================

    def update_title(self, title):

        self.title = title

        self.title_label.config(
            text=title
        )

    # ==========================================================
    # Update Username
    # ==========================================================

    def update_username(self, username):

        self.username = username

        self.username_label.config(
            text=f"Welcome, {username}"
        )

        self.avatar.delete("all")

        self.avatar.create_oval(
            2,
            2,
            40,
            40,
            fill=PRIMARY,
            outline=""
        )

        self.avatar.create_text(
            21,
            21,
            text=username[:1].upper(),
            fill="white",
            font=("Segoe UI", 14, "bold")
        )

    # ==========================================================
    # Set Notification Button Command
    # ==========================================================

    def set_notification_command(self, command):

        self.notification_btn.configure(
            command=command
        )

    # ==========================================================
    # Set Search Button Command
    # ==========================================================

    def set_search_command(self, command):

        self.search_btn.configure(
            command=command
        )

    # ==========================================================
    # Update Date
    # ==========================================================

    def update_date(self):

        today = datetime.now().strftime("%A, %d %B %Y")

        self.date_label.config(
            text=today
        )        
    # ==========================================================
    # Refresh Header
    # ==========================================================

    def refresh(self):

        self.update_date()

        self.update_title(self.title)

        self.update_username(self.username)

    # ==========================================================
    # Set Theme
    # ==========================================================

    def set_theme(self, bg_color=HEADER_BG):

        self.configure(
            bg=bg_color
        )

        for widget in self.winfo_children():

            try:

                widget.configure(bg=bg_color)

            except tk.TclError:

                pass

    # ==========================================================
    # Set Header Height
    # ==========================================================

    def set_height(self, height):

        self.configure(height=height)

        self.grid_propagate(False)

    # ==========================================================
    # Show Header
    # ==========================================================

    def show(self):

        self.grid()

    # ==========================================================
    # Hide Header
    # ==========================================================

    def hide(self):

        self.grid_remove()

    # ==========================================================
    # Set Welcome Text
    # ==========================================================

    def set_welcome_message(self, message):

        self.username_label.config(text=message)

    # ==========================================================
    # Get Current Title
    # ==========================================================

    def get_title(self):

        return self.title

    # ==========================================================
    # Get Current Username
    # ==========================================================

    def get_username(self):

        return self.username

    # ==========================================================
    # Destroy Header
    # ==========================================================

    def destroy_header(self):

        self.destroy()        