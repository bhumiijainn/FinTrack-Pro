import tkinter as tk


# ==========================================================
# COLORS
# ==========================================================

CARD_BG = "#FFFFFF"
TEXT = "#111827"
GRAY = "#6B7280"
BORDER = "#E5E7EB"


class InfoCard(tk.Frame):

    def __init__(
        self,
        parent,
        title="Title",
        value="₹0",
        subtitle="",
        icon=None,
        accent="#2563EB",
        width=250,
        height=140
    ):

        super().__init__(
            parent,
            bg=CARD_BG,
            width=width,
            height=height,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0
        )

        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
        self.accent = accent

        self.grid_propagate(False)

        self.build_card()

    # ======================================================
    # Build Card
    # ======================================================

    def build_card(self):

        self.grid_columnconfigure(1, weight=1)

        # ------------------------------------
        # Accent Line
        # ------------------------------------

        accent = tk.Frame(
            self,
            bg=self.accent,
            width=6
        )

        accent.grid(
            row=0,
            column=0,
            rowspan=3,
            sticky="ns"
        )

        # ------------------------------------
        # Icon
        # ------------------------------------

        if self.icon:

            icon_label = tk.Label(
                self,
                image=self.icon,
                bg=CARD_BG
            )

            icon_label.image = self.icon

            icon_label.grid(
                row=0,
                column=1,
                sticky="e",
                padx=15,
                pady=(15, 0)
            )

        # ------------------------------------
        # Title
        # ------------------------------------

        title = tk.Label(
            self,
            text=self.title,
            font=("Segoe UI", 11),
            fg=GRAY,
            bg=CARD_BG
        )

        title.grid(
            row=0,
            column=1,
            sticky="w",
            padx=20,
            pady=(15, 5)
        )

        # ------------------------------------
        # Value
        # ------------------------------------

        value = tk.Label(
            self,
            text=self.value,
            font=("Segoe UI", 22, "bold"),
            fg=TEXT,
            bg=CARD_BG
        )

        value.grid(
            row=1,
            column=1,
            sticky="w",
            padx=20
        )

        # ------------------------------------
        # Subtitle
        # ------------------------------------

        subtitle = tk.Label(
            self,
            text=self.subtitle,
            font=("Segoe UI", 10),
            fg=GRAY,
            bg=CARD_BG
        )

        subtitle.grid(
            row=2,
            column=1,
            sticky="w",
            padx=20,
            pady=(5, 15)
        )

    # ======================================================
    # Update Card
    # ======================================================

    def update_data(
        self,
        title=None,
        value=None,
        subtitle=None
    ):

        if title is not None:
            self.title = title

        if value is not None:
            self.value = value

        if subtitle is not None:
            self.subtitle = subtitle

        self.refresh()

    # ======================================================
    # Refresh
    # ======================================================

    def refresh(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.build_card()