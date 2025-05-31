import sqlite3
import pandas as pd

DB_NAME = "expenses.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank_name TEXT,
            month TEXT,
            receiver TEXT,
            category TEXT,
            amount REAL
        )
    """
    )
    conn.commit()
    conn.close()


def add_expense(bank_name, month, receiver, category, amount):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO expenses (bank_name, month, receiver, category, amount) VALUES (?, ?, ?, ?, ?)",
        (bank_name, month, receiver, category, amount),
    )
    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df


def delete_expense(entry_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM expenses WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
