import tkinter as tk
import shutil
from tkinter import ttk
from tkinter import filedialog, messagebox

# ==========================================================
# COLORS
# ==========================================================

BACKGROUND = "#F4F7FC"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
TEXT = "#111827"
GRAY = "#6B7280"


class SettingsPage:

    def __init__(self, parent, db, user):

        self.parent = parent
        self.db = db
        self.user = user

        self.build_page()

    # ==========================================================
    # Build Settings Page
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
        self.frame.grid_columnconfigure(1, weight=1)

        self.build_profile()

        self.build_preferences()
        self.build_system()

        self.build_about()

        self.build_actions()
      
    # ==========================================================
    # Profile Section
    # ==========================================================

    def build_profile(self):

        profile = tk.LabelFrame(
            self.frame,
            text="User Profile",
            bg=WHITE,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=20
        )

        profile.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,10),
            pady=(0,10)
        )

        # Username

        tk.Label(
            profile,
            text="Username",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI",10)
        ).pack(anchor="w")

        self.username = tk.Entry(
            profile,
            font=("Segoe UI",11)
        )

        self.username.pack(
            fill="x",
            pady=(5,15)
        )

        self.username.insert(
            0,
            self.user["username"]
        )

        # Full Name

        tk.Label(
            profile,
            text="Full Name",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI",10)
        ).pack(anchor="w")

        self.fullname = tk.Entry(
            profile,
            font=("Segoe UI",11)
        )

        self.fullname.pack(
            fill="x",
            pady=(5,15)
        )

        # Email

        tk.Label(
            profile,
            text="Email",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI",10)
        ).pack(anchor="w")

        self.email = tk.Entry(
            profile,
            font=("Segoe UI",11)
        )

        self.email.pack(
            fill="x",
            pady=(5,15)
        )

        # Phone

        tk.Label(
            profile,
            text="Phone",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI",10)
        ).pack(anchor="w")

        self.phone = tk.Entry(
            profile,
            font=("Segoe UI",11)
        )

        self.phone.pack(
            fill="x",
            pady=(5,20)
        )

    # ==========================================================
    # Preferences Section
    # ==========================================================

    def build_preferences(self):

        preferences = tk.LabelFrame(
            self.frame,
            text="Preferences",
            bg=WHITE,
            font=("Segoe UI",11,"bold"),
            padx=20,
            pady=20
        )

        preferences.grid(
            row=0,
            column=1,
            sticky="nsew",
            pady=(0,10)
        )

        # Currency

        tk.Label(
            preferences,
            text="Currency",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI",10)
        ).pack(anchor="w")

        self.currency = ttk.Combobox(
            preferences,
            state="readonly",
            values=[
                "Indian Rupee (₹)",
                "US Dollar ($)",
                "Euro (€)",
                "Pound (£)"
            ]
        )

        self.currency.current(0)

        self.currency.pack(
            fill="x",
            pady=(5,20)
        )

        # Theme

        tk.Label(
            preferences,
            text="Theme",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI",10)
        ).pack(anchor="w")

        self.theme = ttk.Combobox(
            preferences,
            state="readonly",
            values=[
                "Light",
                "Dark"
            ]
        )

        self.theme.current(0)

        self.theme.pack(
            fill="x",
            pady=(5,20)
        )

        # Notifications

        self.notifications = tk.BooleanVar(value=True)

        tk.Checkbutton(
            preferences,
            text="Enable Notifications",
            variable=self.notifications,
            bg=WHITE,
            font=("Segoe UI",10)
        ).pack(anchor="w")
    # ==========================================================
    # System Settings
    # ==========================================================

    def build_system(self):

        system = tk.LabelFrame(
            self.frame,
            text="System",
            bg=WHITE,
            font=("Segoe UI",11,"bold"),
            padx=20,
            pady=20
        )

        system.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0,10),
            pady=(0,10)
        )

        tk.Button(
            system,
            text="💾 Backup Database",
            command=self.backup_database,
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI",10,"bold")
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            system,
            text="♻ Restore Database",
            command=self.restore_database,
            bg="#16A34A",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI",10,"bold")
        ).pack(
            fill="x",
            pady=5
        )

        tk.Button(
            system,
            text="🔒 Change Password",
            command=self.change_password,
            bg="#F59E0B",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI",10,"bold")
        ).pack(
            fill="x",
            pady=5
        )

    # ==========================================================
    # About
    # ==========================================================

    def build_about(self):

        about = tk.LabelFrame(
            self.frame,
            text="About FinTrack Pro",
            bg=WHITE,
            font=("Segoe UI",11,"bold"),
            padx=20,
            pady=20
        )

        about.grid(
            row=1,
            column=1,
            sticky="nsew",
            pady=(0,10)
        )

        tk.Label(
            about,
            text="FinTrack Pro",
            bg=WHITE,
            fg=PRIMARY,
            font=("Segoe UI",18,"bold")
        ).pack()

        tk.Label(
            about,
            text="Version 1.0",
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI",10)
        ).pack(pady=5)

        tk.Label(
            about,
            text="A Personal Finance Management System\nbuilt using Python, Tkinter and SQLite.",
            bg=WHITE,
            fg=TEXT,
            justify="center",
            font=("Segoe UI",10)
        ).pack(pady=10)

        tk.Label(
            about,
            text="© 2026 FinTrack Pro",
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI",9)
        ).pack()

    # ==========================================================
    # Action Buttons
    # ==========================================================

    def build_actions(self):

        actions = tk.Frame(
            self.frame,
            bg=BACKGROUND
        )

        actions.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(10,0)
        )

        tk.Button(
            actions,
            text="Save Settings",
            command=self.save_settings,
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI",11,"bold"),
            padx=20,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            actions,
            text="Reset",
            command=self.reset_settings,
            bg="#DC2626",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI",11,"bold"),
            padx=20,
            pady=8
        ).pack(
            side="left",
            padx=5
        )        
    # ==========================================================
    # Save Settings
    # ==========================================================

    def save_settings(self):

        messagebox.showinfo(

            "Success",

            "Settings saved successfully."

        )

    # ==========================================================
    # Load Settings
    # ==========================================================

    def load_settings(self):

        self.username.delete(0, tk.END)

        self.username.insert(

            0,

            self.user["username"]

        )

        self.currency.current(0)

        self.theme.current(0)

        self.notifications.set(True)

    # ==========================================================
    # Reset Settings
    # ==========================================================

    def reset_settings(self):

        self.load_settings()

        self.fullname.delete(0, tk.END)

        self.email.delete(0, tk.END)

        self.phone.delete(0, tk.END)

        messagebox.showinfo(

            "Reset",

            "Settings restored to default."

        )

    # ==========================================================
    # Backup Database
    # ==========================================================

    def backup_database(self):

        destination = filedialog.asksaveasfilename(

            defaultextension=".db",

            filetypes=[

                ("Database File", "*.db")

            ],

            initialfile="finance_backup.db"

        )

        if not destination:

            return

        try:

            shutil.copy(

                "finance.db",

                destination

            )

            messagebox.showinfo(

                "Backup Complete",

                "Database backup created successfully."

            )

        except Exception as e:

            messagebox.showerror(

                "Backup Failed",

                str(e)

            )

    # ==========================================================
    # Restore Database
    # ==========================================================

    def restore_database(self):

        source = filedialog.askopenfilename(

            filetypes=[

                ("Database File", "*.db")

            ]

        )

        if not source:

            return

        try:

            shutil.copy(

                source,

                "finance.db"

            )

            messagebox.showinfo(

                "Restore Complete",

                "Database restored successfully.\nRestart the application."

            )

        except Exception as e:

            messagebox.showerror(

                "Restore Failed",

                str(e)

            )

    # ==========================================================
    # Change Password
    # ==========================================================

    def change_password(self):

        messagebox.showinfo(

            "Coming Soon",

            "Password encryption using bcrypt will be added later."

        )        
    # ==========================================================
    # Refresh Settings
    # ==========================================================

    def refresh(self):

        self.load_settings()

    # ==========================================================
    # Clear Fields
    # ==========================================================

    def clear_fields(self):

        self.fullname.delete(0, tk.END)

        self.email.delete(0, tk.END)

        self.phone.delete(0, tk.END)

    # ==========================================================
    # Validate Email
    # ==========================================================

    def validate_email(self, email):

        if "@" not in email:

            return False

        if "." not in email:

            return False

        return True

    # ==========================================================
    # Validate Phone
    # ==========================================================

    def validate_phone(self, phone):

        if phone == "":

            return True

        return phone.isdigit() and len(phone) == 10

    # ==========================================================
    # Update Profile
    # ==========================================================

    def update_profile(self):

        fullname = self.fullname.get().strip()

        email = self.email.get().strip()

        phone = self.phone.get().strip()

        if email and not self.validate_email(email):

            messagebox.showerror(

                "Invalid Email",

                "Please enter a valid email address."

            )

            return

        if phone and not self.validate_phone(phone):

            messagebox.showerror(

                "Invalid Phone",

                "Phone number must contain exactly 10 digits."

            )

            return

        messagebox.showinfo(

            "Profile Updated",

            "Profile updated successfully."

        )

    # ==========================================================
    # Apply Theme
    # ==========================================================

    def apply_theme(self):

        theme = self.theme.get()

        if theme == "Dark":

            messagebox.showinfo(

                "Coming Soon",

                "Dark Mode will be implemented later."

            )

        else:

            pass

    # ==========================================================
    # Close Settings
    # ==========================================================

    def close(self):

        self.frame.destroy()        