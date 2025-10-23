import sqlite3
from typing import Optional


class BankDatabase:
    """Encapsulates all database operations for the banking application."""

    def __init__(self, db_path: str = "card.s3db") -> None:
        """Initialize and prepare the database schema."""
        self.db_path = db_path
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        """Establish a database connection."""
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        """Ensure that the 'card' table exists."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS card (
                    id INTEGER PRIMARY KEY,
                    number TEXT UNIQUE NOT NULL,
                    pin TEXT NOT NULL,
                    balance INTEGER DEFAULT 0
                );
            """)

    # -------------------------- CRUD Operations --------------------------

    def insert_account(self, number: str, pin: str) -> None:
        """Insert a new account into the database."""
        with self._connect() as conn:
            conn.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (number, pin))

    def get_pin(self, number: str) -> Optional[str]:
        """Retrieve the stored PIN for a given account number."""
        with self._connect() as conn:
            result = conn.execute("SELECT pin FROM card WHERE number = ?", (number,)).fetchone()
        return result[0] if result else None

    def get_balance(self, number: str) -> Optional[int]:
        """Retrieve the account balance."""
        with self._connect() as conn:
            result = conn.execute("SELECT balance FROM card WHERE number = ?", (number,)).fetchone()
        return result[0] if result else None

    def update_balance(self, number: str, delta: int) -> None:
        """Update account balance by a delta (positive or negative)."""
        with self._connect() as conn:
            conn.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (delta, number))

    def transfer(self, sender: str, receiver: str, amount: int) -> bool:
        """Execute a transfer between two accounts."""
        with self._connect() as conn:
            sender_balance = self.get_balance(sender)
            if sender_balance is None or sender_balance < amount:
                return False
            conn.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (amount, sender))
            conn.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (amount, receiver))
        return True

    def delete_account(self, number: str) -> None:
        """Delete an account from the database."""
        with self._connect() as conn:
            conn.execute("DELETE FROM card WHERE number = ?", (number,))

    def account_exists(self, number: str) -> bool:
        """Check if an account exists."""
        with self._connect() as conn:
            result = conn.execute("SELECT 1 FROM card WHERE number = ?", (number,)).fetchone()
        return result is not None
