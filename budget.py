import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Entertainment",
    "Health",
    "Other"
]


def show_budget():

    window = tk.Toplevel()
    window.title("Budget & Spending Limit")
    window.geometry("650x550")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Budget & Spending Limit",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    form_frame = tk.Frame(window)
    form_frame.pack(pady=10)

    tk.Label(
        form_frame,
        text="Category:",
        font=("Arial", 12)
    ).grid(row=0, column=0, padx=10, pady=10)

    category_combo = ttk.Combobox(
        form_frame,
        values=CATEGORIES,
        state="readonly",
        width=20
    )
    category_combo.grid(row=0, column=1, padx=10, pady=10)
    category_combo.set("Food")

    tk.Label(
        form_frame,
        text="Budget Amount:",
        font=("Arial", 12)
    ).grid(row=1, column=0, padx=10, pady=10)

    amount_entry = tk.Entry(
        form_frame,
        width=23
    )
    amount_entry.grid(row=1, column=1, padx=10, pady=10)

    def save_budget():

        category = category_combo.get()
        amount = amount_entry.get()

        if not amount:
            messagebox.showerror(
                "Error",
                "Please enter budget amount."
            )
            return

        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid positive amount."
            )
            return

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL
            )
        """)

        cursor.execute("""
            INSERT OR REPLACE INTO budgets
            (category, amount)
            VALUES (?, ?)
        """, (category, amount))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            f"Budget for {category} saved successfully!"
        )

        amount_entry.delete(0, tk.END)

        load_budgets()

    tk.Button(
        form_frame,
        text="Save Budget",
        width=18,
        height=2,
        command=save_budget
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=15
    )

    tk.Label(
        window,
        text="Current Budgets",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    columns = (
        "Category",
        "Budget",
        "Spent",
        "Remaining",
        "Status"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=10
    )

    for column in columns:
        tree.heading(column, text=column)

    tree.column("Category", width=120)
    tree.column("Budget", width=100)
    tree.column("Spent", width=100)
    tree.column("Remaining", width=110)
    tree.column("Status", width=120)

    tree.pack(
        padx=20,
        pady=10
    )

    def load_budgets():

        for item in tree.get_children():
            tree.delete(item)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL
            )
        """)

        cursor.execute("""
            SELECT category, amount
            FROM budgets
            ORDER BY category
        """)

        budgets = cursor.fetchall()

        for category, budget in budgets:

            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE transaction_type = 'Expense'
                AND category = ?
            """, (category,))

            spent = cursor.fetchone()[0]

            remaining = budget - spent

            if spent > budget:
                status = "OVER BUDGET"
            elif spent >= budget * 0.8:
                status = "Near Limit"
            else:
                status = "Within Budget"

            tree.insert(
                "",
                "end",
                values=(
                    category,
                    f"₹{budget:.2f}",
                    f"₹{spent:.2f}",
                    f"₹{remaining:.2f}",
                    status
                )
            )

        conn.commit()
        conn.close()

    load_budgets()