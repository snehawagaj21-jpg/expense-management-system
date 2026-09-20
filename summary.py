import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def show_summary():

    window = tk.Toplevel()
    window.title("Monthly Summary")
    window.geometry("750x550")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Monthly Summary",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    filter_frame = tk.Frame(window)
    filter_frame.pack(pady=10)

    tk.Label(
        filter_frame,
        text="Select Month:",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=0, padx=10)

    month_box = ttk.Combobox(
        filter_frame,
        values=[
            "01 - January",
            "02 - February",
            "03 - March",
            "04 - April",
            "05 - May",
            "06 - June",
            "07 - July",
            "08 - August",
            "09 - September",
            "10 - October",
            "11 - November",
            "12 - December"
        ],
        width=20,
        state="readonly"
    )

    month_box.set("09 - September")
    month_box.grid(row=0, column=1, padx=10)

    summary_frame = tk.Frame(window)
    summary_frame.pack(pady=25)

    income_label = tk.Label(
        summary_frame,
        text="Total Income: ₹ 0.00",
        font=("Arial", 16, "bold")
    )
    income_label.pack(pady=8)

    expense_label = tk.Label(
        summary_frame,
        text="Total Expense: ₹ 0.00",
        font=("Arial", 16, "bold")
    )
    expense_label.pack(pady=8)

    balance_label = tk.Label(
        summary_frame,
        text="Balance: ₹ 0.00",
        font=("Arial", 16, "bold")
    )
    balance_label.pack(pady=8)

    top_category_label = tk.Label(
        summary_frame,
        text="Top Spending Category: -",
        font=("Arial", 16, "bold")
    )
    top_category_label.pack(pady=8)

    alert_label = tk.Label(
        window,
        text="",
        font=("Arial", 14, "bold")
    )
    alert_label.pack(pady=15)

    def calculate_summary():

        selected_month = month_box.get()

        if not selected_month:
            messagebox.showwarning(
                "Select Month",
                "Please select a month."
            )
            return

        month_number = selected_month[:2]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Income'
            AND substr(date, 6, 2) = ?
        """, (month_number,))

        total_income = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
        """, (month_number,))

        total_expense = cursor.fetchone()[0]

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
            LIMIT 1
        """, (month_number,))

        top_category = cursor.fetchone()

        conn.close()

        balance = total_income - total_expense

        income_label.config(
            text=f"Total Income: ₹ {total_income:.2f}"
        )

        expense_label.config(
            text=f"Total Expense: ₹ {total_expense:.2f}"
        )

        balance_label.config(
            text=f"Balance: ₹ {balance:.2f}"
        )

        if top_category:
            top_category_label.config(
                text=f"Top Spending Category: {top_category[0]}"
            )
        else:
            top_category_label.config(
                text="Top Spending Category: -"
            )

        if total_expense > total_income and total_income > 0:

            alert_label.config(
                text="⚠️ Overspending Alert! Expenses are higher than income."
            )

        elif total_expense > 0 and total_income == 0:

            alert_label.config(
                text="⚠️ Expenses recorded but no income found."
            )

        else:

            alert_label.config(
                text="✓ Your spending is within your income."
            )

    tk.Button(
        window,
        text="View Summary",
        width=22,
        height=2,
        font=("Arial", 12, "bold"),
        command=calculate_summary
    ).pack(pady=15)

    calculate_summary()