import sqlite3
import matplotlib.pyplot as plt


def show_reports():

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # ---------------- EXPENSE BY CATEGORY ----------------

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE transaction_type = 'Expense'
        GROUP BY category
    """)

    category_data = cursor.fetchall()

    # ---------------- INCOME VS EXPENSE ----------------

    cursor.execute("""
        SELECT transaction_type, SUM(amount)
        FROM transactions
        GROUP BY transaction_type
    """)

    income_expense_data = cursor.fetchall()

    conn.close()

    # ---------------- PIE CHART ----------------

    if category_data:

        categories = [row[0] for row in category_data]
        amounts = [row[1] for row in category_data]

        plt.figure(figsize=(7, 6))

        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        plt.title("Expense by Category")

        plt.show()

    else:
        print("No expense data available.")

    # ---------------- BAR CHART ----------------

    if income_expense_data:

        types = [row[0] for row in income_expense_data]
        amounts = [row[1] for row in income_expense_data]

        plt.figure(figsize=(7, 6))

        plt.bar(
            types,
            amounts
        )

        plt.title("Income vs Expense")
        plt.xlabel("Transaction Type")
        plt.ylabel("Amount (₹)")

        plt.show()

    else:
        print("No transaction data available.")