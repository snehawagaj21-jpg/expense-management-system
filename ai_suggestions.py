import tkinter as tk
import sqlite3
from tkinter import messagebox


def show_ai_suggestions():

    window = tk.Toplevel()
    window.title("AI Spending Suggestions")
    window.geometry("600x500")
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="AI Spending Suggestions",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=20)

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE transaction_type = 'Expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    category_data = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE transaction_type = 'Expense'
    """)

    result = cursor.fetchone()
    total_expense = result[0] if result[0] else 0

    conn.close()

    suggestions = []

    if total_expense == 0:
        suggestions.append(
            "No expenses found yet. Start adding expenses to get suggestions."
        )
    else:

        if category_data:
            top_category = category_data[0][0]
            top_amount = category_data[0][1]

            suggestions.append(
                f"• Your highest spending category is {top_category} "
                f"(₹{top_amount:.2f})."
            )

            percentage = (top_amount / total_expense) * 100

            if percentage > 40:
                suggestions.append(
                    f"• {top_category} uses about {percentage:.1f}% "
                    f"of your total expenses."
                )

                suggestions.append(
                    f"• Try reducing your {top_category} expenses "
                    f"to improve your savings."
                )

        if total_expense > 5000:
            suggestions.append(
                "• Your total expenses are high. Consider setting "
                "a monthly spending limit."
            )
        elif total_expense > 2000:
            suggestions.append(
                "• Keep monitoring your expenses and avoid "
                "unnecessary spending."
            )
        else:
            suggestions.append(
                "• Your current spending is under control. "
                "Keep maintaining this habit."
            )

        suggestions.append(
            "• Review your expenses regularly to identify "
            "where you can save money."
        )

    suggestion_text = tk.Text(
        window,
        width=65,
        height=18,
        font=("Arial", 12),
        wrap="word"
    )

    suggestion_text.pack(padx=20, pady=10)

    for suggestion in suggestions:
        suggestion_text.insert(tk.END, suggestion + "\n\n")

    suggestion_text.config(state="disabled")