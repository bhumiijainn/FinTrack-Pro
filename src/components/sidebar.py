import tkinter as tk

# ==========================================================
# COLORS
# ==========================================================

SIDEBAR_BG = "#1E293B"

PRIMARY = "#2563EB"

ACTIVE = "#2563EB"

HOVER = "#334155"

TEXT = "#FFFFFF"

LOGO = "#60A5FA"


class Sidebar(tk.Frame):

    def __init__(
        self,
        parent,
        commands=None,
        icons=None,
        active_page="Dashboard"
    ):

        super().__init__(
            parent,
            bg=SIDEBAR_BG,
            width=280
        )

        # Keep sidebar width fixed
        self.grid_propagate(False)

        self.commands = commands if commands else {}

        self.icons = icons if icons else {}

        self.active_page = active_page

        self.buttons = {}

        self.build_sidebar()

    # ==========================================================
    # Build Sidebar
    # ==========================================================

    def build_sidebar(self):

        self.grid_rowconfigure(99, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.build_logo()

        self.build_navigation()

    # ==========================================================
    # Logo
    # ==========================================================

    def build_logo(self):

        logo_frame = tk.Frame(
            self,
            bg=SIDEBAR_BG
        )

        logo_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(25, 35)
        )

        if "logo" in self.icons:

            logo = tk.Label(
                logo_frame,
                image=self.icons["logo"],
                bg=SIDEBAR_BG
            )

            logo.image = self.icons["logo"]

            logo.pack()

        else:

            tk.Label(
                logo_frame,
                text="FinTrack Pro",
                bg=SIDEBAR_BG,
                fg=LOGO,
                font=("Segoe UI", 20, "bold")
            ).pack()

    # ==========================================================
    # Navigation Menu
    # ==========================================================

    def build_navigation(self):

        self.menu = [

            "Dashboard",

            "Income",

            "Expense",

            "Reports",

            "Charts",

            "Search",

            "Budget",

            "Settings",

            

        ]

        row = 1

        for page in self.menu:

            self.create_button(
                row,
                page,
                
                
            )

            row += 1
        # ==========================================================
# Push Logout to Bottom
# ==========================================================

        self.grid_rowconfigure(100, weight=1)

        self.add_divider(101)

        self.create_button(

        102,

        "Logout",

        

)    
    # ==========================================================
    # Create Navigation Button
    # ==========================================================

    def create_button(self, row, page):

        active = page == self.active_page

        bg = ACTIVE if active else SIDEBAR_BG

        button = tk.Button(

            self,

            text=page,

            bg=bg,

            fg=TEXT,

            activebackground=ACTIVE,

            activeforeground="white",

            relief="flat",

            bd=0,

            anchor="w",

            padx=28,

            pady=14,

            cursor="hand2",

            font=("Segoe UI", 23),

            command=lambda p=page: self.navigate(p)

        )

        button.grid(

            row=row,

            column=0,

            sticky="ew",

            padx=10,

            pady=4

        )

        self.buttons[page] = button

        # Hover Effects
        if not active:

            button.bind(

                "<Enter>",

                lambda e, b=button: self.on_hover(b)

            )

            button.bind(

                "<Leave>",

                lambda e, b=button: self.on_leave(b)

            )

    # ==========================================================
    # Hover
    # ==========================================================

    def on_hover(self, button):

        if button.cget("bg") != ACTIVE:

            button.configure(bg=HOVER)

    # ==========================================================
    # Leave
    # ==========================================================

    def on_leave(self, button):

        if button.cget("bg") != ACTIVE:

            button.configure(bg=SIDEBAR_BG)

    # ==========================================================
    # Divider
    # ==========================================================

    def add_divider(self, row):

        divider = tk.Frame(

            self,

            bg="#475569",

            height=1

        )

        divider.grid(

            row=row,

            column=0,

            sticky="ew",

            padx=15,

            pady=10

        )            
    # ==========================================================
    # Set Active Page
    # ==========================================================

    def set_active(self, page):

        self.active_page = page

        for name, button in self.buttons.items():

            if name == page:

                button.configure(

                    bg=ACTIVE,

                    fg="white",

                    font=("Segoe UI", 11, "bold")

                )

            else:

                button.configure(

                    bg=SIDEBAR_BG,

                    fg=TEXT,

                    font=("Segoe UI", 11)

                )
    # ==========================================================
    # Navigate
    # ==========================================================

    def navigate(self, page):

        self.set_active(page)

        command = self.commands.get(page)

        if callable(command):

            command()

    # ==========================================================
    # Refresh Sidebar
    # ==========================================================

    def refresh(self):

        for widget in self.winfo_children():

            widget.destroy()

        self.buttons.clear()

        self.build_sidebar()

    # ==========================================================
    # Update Commands
    # ==========================================================

    def set_commands(self, commands):

        self.commands = commands

        self.refresh()

    # ==========================================================
    # Update Icons
    # ==========================================================

    def update_icons(self, icons):

        self.icons = icons

        self.refresh()

    # ==========================================================
    # Current Page
    # ==========================================================

    def get_active_page(self):

        return self.active_page        
    # ==========================================================
    # Enable Sidebar
    # ==========================================================

    def enable(self):

        for button in self.buttons.values():

            button.configure(
                state="normal"
            )

    # ==========================================================
    # Disable Sidebar
    # ==========================================================

    def disable(self):

        for button in self.buttons.values():

            button.configure(
                state="disabled"
            )

    # ==========================================================
    # Enable Hover Effects
    # ==========================================================

    def enable_hover(self):

        for page, button in self.buttons.items():

            if page == self.active_page:
                continue

            button.bind(

                "<Enter>",

                lambda e, b=button: self.on_hover(b)

            )

            button.bind(

                "<Leave>",

                lambda e, b=button: self.on_leave(b)

            )

    # ==========================================================
    # Disable Hover Effects
    # ==========================================================

    def disable_hover(self):

        for button in self.buttons.values():

            button.unbind("<Enter>")

            button.unbind("<Leave>")

    # ==========================================================
    # Set Sidebar Width
    # ==========================================================

    def set_width(self, width):

        self.configure(width=width)

        self.grid_propagate(False)

    # ==========================================================
    # Show Sidebar
    # ==========================================================

    def show(self):

        self.grid()

    # ==========================================================
    # Hide Sidebar
    # ==========================================================

    def hide(self):

        self.grid_remove()

    # ==========================================================
    # Destroy Sidebar
    # ==========================================================

    def destroy_sidebar(self):

        self.destroy()    