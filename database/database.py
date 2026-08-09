import sqlite3
from pathlib import Path


class DatabaseManager:
    """
    FinTrack Pro Database Manager
    Handles all SQLite operations.
    """

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self):

        # Database Location

        self.db_path = Path(__file__).parent / "finance.db"

        # Connection

        self.connection = sqlite3.connect(
            self.db_path
        )
        self.connection.execute("PRAGMA foreign_keys = ON")
        # Return rows as dictionaries

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        # Initialize Database

        self.initialize_database()

    # ==========================================================
    # Initialize Database
    # ==========================================================

    def initialize_database(self):

        self.create_users_table()

        self.create_transactions_table()

        self.create_budgets_table()

        self.create_settings_table()

        self.connection.commit()

    # ==========================================================
    # Users Table
    # ==========================================================

    def create_users_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT NOT NULL UNIQUE,

                password TEXT NOT NULL,

                fullname TEXT,

                email TEXT,

                phone TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )      
    # ==========================================================
    # Transactions Table
    # ==========================================================

    def create_transactions_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                type TEXT NOT NULL,

                category TEXT NOT NULL,

                amount REAL NOT NULL,

                description TEXT,

                date TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

            )
            """
        )  

    # ==========================================================
    # Budgets Table
    # ==========================================================

    def create_budgets_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS budgets (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                category TEXT NOT NULL,

                budget REAL NOT NULL,

                month TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

            )
            """
        )

   
  

    # ==========================================================
    # Settings Table
    # ==========================================================

    def create_settings_table(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL UNIQUE,

                currency TEXT DEFAULT '₹',

                theme TEXT DEFAULT 'Light',

                notifications INTEGER DEFAULT 1,

                FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

            )
            """
        )

        
    # ==========================================================
    # Execute Query
    # ==========================================================

    def execute(self, query, parameters=()):

        self.cursor.execute(query, parameters)

        self.connection.commit()

    # ==========================================================
    # Execute Many
    # ==========================================================

    def executemany(self, query, values):

        self.cursor.executemany(query, values)

        self.connection.commit()

    # ==========================================================
    # Fetch One
    # ==========================================================

    def fetch_one(self, query, parameters=()):

        self.cursor.execute(query, parameters)

        return self.cursor.fetchone()

    # ==========================================================
    # Fetch All
    # ==========================================================

    def fetch_all(self, query, parameters=()):

        self.cursor.execute(query, parameters)

        return self.cursor.fetchall()

    # ==========================================================
    # Last Insert ID
    # ==========================================================

    def last_insert_id(self):

        return self.cursor.lastrowid        
    # ==========================================================
    # Begin Transaction
    # ==========================================================

    def begin(self):

        self.connection.execute("BEGIN")

    # ==========================================================
    # Commit Transaction
    # ==========================================================

    def commit(self):

        self.connection.commit()

    # ==========================================================
    # Rollback Transaction
    # ==========================================================

    def rollback(self):

        self.connection.rollback()

    # ==========================================================
    # Check if User Exists
    # ==========================================================

    def user_exists(self, username):

        row = self.fetch_one(

            """
            SELECT id
            FROM users
            WHERE username=?
            """,

            (username,)

        )

        return row is not None

    # ==========================================================
    # Get User by Username
    # ==========================================================

    def get_user(self, username):

        return self.fetch_one(

            """
            SELECT *
            FROM users
            WHERE username=?
            """,

            (username,)

        )

    # ==========================================================
    # Close Database
    # ==========================================================

    def close(self):

        if self.connection:

            self.connection.close()


# ==========================================================
# Create Database
# ==========================================================

if __name__ == "__main__":

    db = DatabaseManager()

    print("=" * 55)
    print("         FinTrack Pro Database Initialized")
    print("=" * 55)
    print(f"Database : {db.db_path}")
    print()
    print("Tables Created:")
    print("  • users")
    print("  • transactions")
    print("  • budgets")
    print("  • settings")
    print()
    print("Status : Ready")
    print("=" * 55)

    db.close()    