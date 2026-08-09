import tkinter as tk

from database.database import DatabaseManager
from src.auth import AuthScreen


class FinTrackApp:
    def __init__(self):

        # Initialize Database
        self.db = DatabaseManager()

        # Create Main Window
        self.root = tk.Tk()

        self.root.title("FinTrack Pro")

        # Window Size
        window_width = 1200
        window_height = 700

        # Center Window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # Load Authentication Screen
        self.auth = AuthScreen(self.root, self.db)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FinTrackApp()
    app.run()