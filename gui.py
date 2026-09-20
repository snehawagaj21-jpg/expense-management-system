import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox

from reports import show_reports
from summary import show_summary
from ai_suggestions import show_ai_suggestions
from budget import show_budget
from financial_goals import show_financial_goals


CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Entertainment",
    "Health",
    "Salary",
    "Other"
]


MONTHS = [
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
]


def check_budget_warning(category, new_amount):

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='budgets'
    """)

    table_exists = cursor.fetchone()

    if not table_exists:
        conn.close()
        return True

    cursor.execute("""
        SELECT amount
        FROM budgets
        WHERE category = ?
    """, (category,))

    result = cursor.fetchone()

    if not result:
        conn.close()
        return True

    budget = result[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE transaction_type = 'Expense'
        AND category = ?
    """, (category,))

    current_spending = cursor.fetchone()[0]

    conn.close()

    new_total = current_spending + new_amount

    if new_total > budget:

        exceeded_amount = new_total - budget

        answer = messagebox.askyesno(
            "⚠ Budget Warning",
            f"Your {category} budget will be exceeded!\n\n"
            f"Budget: ₹{budget:.2f}\n"
            f"Current Spending: ₹{current_spending:.2f}\n"
            f"New Expense: ₹{new_amount:.2f}\n"
            f"New Total: ₹{new_total:.2f}\n\n"
            f"Budget Exceeded By: ₹{exceeded_amount:.2f}\n\n"
            f"Do you still want to add this expense?"
        )

        return answer

    elif new_total >= budget * 0.8:

        remaining = budget - new_total

        answer = messagebox.askyesno(
            "⚠ Spending Limit Warning",
            f"You are close to your {category} budget limit!\n\n"
            f"Budget: ₹{budget:.2f}\n"
            f"Current Spending: ₹{current_spending:.2f}\n"
            f"New Expense: ₹{new_amount:.2f}\n"
            f"New Total: ₹{new_total:.2f}\n"
            f"Remaining Budget: ₹{remaining:.2f}\n\n"
            f"Do you want to continue?"
        )

        return answer

    return True


def add_transaction(transaction_type):

    window = tk.Toplevel()
    window.title("Add " + transaction_type)
    window.geometry("400x450")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Add " + transaction_type,
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Amount"
    ).pack()

    amount_entry = tk.Entry(
        window,
        width=30
    )
    amount_entry.pack(pady=5)

    tk.Label(
        window,
        text="Category"
    ).pack()

    category_combo = ttk.Combobox(
        window,
        values=CATEGORIES,
        state="readonly",
        width=27
    )
    category_combo.pack(pady=5)
    category_combo.set(CATEGORIES[0])

    tk.Label(
        window,
        text="Description"
    ).pack()

    description_entry = tk.Entry(
        window,
        width=30
    )
    description_entry.pack(pady=5)

    tk.Label(
        window,
        text="Date (YYYY-MM-DD)"
    ).pack()

    date_entry = tk.Entry(
        window,
        width=30
    )
    date_entry.pack(pady=5)

    def save_transaction():

        amount = amount_entry.get()
        category = category_combo.get()
        description = description_entry.get()
        date = date_entry.get()

        if not amount or not date:

            messagebox.showerror(
                "Error",
                "Amount and Date are required."
            )
            return

        try:

            amount = float(amount)

            if amount <= 0:

                messagebox.showerror(
                    "Error",
                    "Amount must be greater than 0."
                )
                return

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )
            return

        if transaction_type == "Expense":

            allowed = check_budget_warning(
                category,
                amount
            )

            if not allowed:
                return

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (transaction_type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type,
            amount,
            category,
            description,
            date
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            transaction_type + " added successfully!"
        )

        window.destroy()

    tk.Button(
        window,
        text="Save",
        width=15,
        height=2,
        command=save_transaction
    ).pack(pady=20)


def monthly_spending_comparison():

    window = tk.Toplevel()
    window.title("Monthly Spending Comparison")
    window.geometry("600x550")
    window.resizable(False, False)

    tk.Label(
        window,
        text="📈 Monthly Spending Comparison",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    selection_frame = tk.Frame(window)
    selection_frame.pack(pady=10)

    tk.Label(
        selection_frame,
        text="Select Month:",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    month_combo = ttk.Combobox(
        selection_frame,
        values=MONTHS,
        state="readonly",
        width=20
    )

    month_combo.grid(
        row=0,
        column=1,
        padx=5
    )

    month_combo.set(MONTHS[0])

    result_frame = tk.Frame(
        window,
        bd=2,
        relief="groove"
    )

    result_frame.pack(
        padx=30,
        pady=20,
        fill="both",
        expand=True
    )

    current_label = tk.Label(
        result_frame,
        text="Current Month Expense: ₹0.00",
        font=("Arial", 14, "bold")
    )

    current_label.pack(pady=20)

    previous_label = tk.Label(
        result_frame,
        text="Previous Month Expense: ₹0.00",
        font=("Arial", 14, "bold")
    )

    previous_label.pack(pady=10)

    difference_label = tk.Label(
        result_frame,
        text="Difference: ₹0.00",
        font=("Arial", 14, "bold")
    )

    difference_label.pack(pady=10)

    percentage_label = tk.Label(
        result_frame,
        text="Change: 0%",
        font=("Arial", 14, "bold")
    )

    percentage_label.pack(pady=10)

    message_label = tk.Label(
        result_frame,
        text="",
        font=("Arial", 13, "bold"),
        wraplength=450
    )

    message_label.pack(pady=20)

    def compare_months():

        selected_month = month_combo.get()
        current_month = selected_month[:2]

        current_month_number = int(current_month)

        if current_month_number == 1:
            previous_month = 12
        else:
            previous_month = current_month_number - 1

        current_month = f"{current_month_number:02d}"
        previous_month = f"{previous_month:02d}"

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
        """, (current_month,))

        current_expense = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
        """, (previous_month,))

        previous_expense = cursor.fetchone()[0]

        conn.close()

        difference = current_expense - previous_expense

        if previous_expense > 0:

            percentage = (
                difference / previous_expense
            ) * 100

        else:
            percentage = 0

        current_label.config(
            text=f"Current Month Expense: ₹{current_expense:.2f}"
        )

        previous_label.config(
            text=f"Previous Month Expense: ₹{previous_expense:.2f}"
        )

        difference_label.config(
            text=f"Difference: ₹{abs(difference):.2f}"
        )

        if previous_expense == 0 and current_expense > 0:

            percentage_label.config(
                text="Change: New Spending"
            )

            message_label.config(
                text="⚠ You have spending this month, "
                     "but no spending was recorded for "
                     "the previous month."
            )

        elif current_expense > previous_expense:

            percentage_label.config(
                text=f"Spending Increased: {percentage:.2f}%"
            )

            message_label.config(
                text="⚠ Your spending increased compared "
                     "to the previous month. Try to reduce "
                     "unnecessary expenses."
            )

        elif current_expense < previous_expense:

            percentage_label.config(
                text=f"Spending Decreased: {abs(percentage):.2f}%"
            )

            message_label.config(
                text="✅ Great! Your spending decreased "
                     "compared to the previous month."
            )

        else:

            percentage_label.config(
                text="Spending Change: 0%"
            )

            message_label.config(
                text="Your spending is the same as "
                     "the previous month."
            )

    tk.Button(
        window,
        text="Compare",
        width=18,
        height=2,
        font=("Arial", 11, "bold"),
        command=compare_months
    ).pack(pady=15)


def view_transactions():

    window = tk.Toplevel()
    window.title("Transactions")
    window.geometry("950x600")

    search_frame = tk.Frame(window)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search:"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    search_entry = tk.Entry(
        search_frame,
        width=20
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Label(
        search_frame,
        text="Category:"
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    category_filter = ttk.Combobox(
        search_frame,
        values=["All"] + CATEGORIES,
        state="readonly",
        width=15
    )

    category_filter.grid(
        row=0,
        column=3,
        padx=5
    )

    category_filter.set("All")

    tk.Label(
        search_frame,
        text="Month:"
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    months = [
        "All",
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
    ]

    month_filter = ttk.Combobox(
        search_frame,
        values=months,
        state="readonly",
        width=15
    )

    month_filter.grid(
        row=0,
        column=5,
        padx=5
    )

    month_filter.set("All")

    columns = (
        "ID",
        "Type",
        "Amount",
        "Category",
        "Description",
        "Date"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(
            column,
            text=column
        )

    tree.column("ID", width=50)
    tree.column("Type", width=100)
    tree.column("Amount", width=100)
    tree.column("Category", width=120)
    tree.column("Description", width=200)
    tree.column("Date", width=120)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    scrollbar = ttk.Scrollbar(
        window,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def load_transactions(
        search="",
        category="All",
        month="All"
    ):

        for item in tree.get_children():
            tree.delete(item)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        query = """
            SELECT id,
                   transaction_type,
                   amount,
                   category,
                   description,
                   date
            FROM transactions
            WHERE 1=1
        """

        params = []

        if search:

            query += """
                AND (
                    category LIKE ?
                    OR description LIKE ?
                    OR transaction_type LIKE ?
                )
            """

            search_value = "%" + search + "%"

            params.extend([
                search_value,
                search_value,
                search_value
            ])

        if category != "All":

            query += " AND category = ?"
            params.append(category)

        if month != "All":

            month_number = month[:2]

            query += """
                AND substr(date, 6, 2) = ?
            """

            params.append(month_number)

        query += " ORDER BY date DESC"

        cursor.execute(
            query,
            params
        )

        rows = cursor.fetchall()

        for row in rows:

            tree.insert(
                "",
                "end",
                values=row
            )

        conn.close()

    def apply_filter():

        search = search_entry.get()
        category = category_filter.get()
        month = month_filter.get()

        load_transactions(
            search,
            category,
            month
        )

    def clear_filter():

        search_entry.delete(
            0,
            tk.END
        )

        category_filter.set("All")
        month_filter.set("All")

        load_transactions()

    def delete_selected():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a transaction."
            )

            return

        item = tree.item(
            selected[0]
        )

        transaction_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if confirm:

            conn = sqlite3.connect(
                "expenses.db"
            )

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM transactions WHERE id = ?",
                (transaction_id,)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Transaction deleted successfully!"
            )

            apply_filter()

    def update_selected():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a transaction."
            )

            return

        item = tree.item(
            selected[0]
        )

        values = item["values"]

        transaction_id = values[0]

        update_window = tk.Toplevel()

        update_window.title(
            "Update Transaction"
        )

        update_window.geometry(
            "400x450"
        )

        tk.Label(
            update_window,
            text="Update Transaction",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            update_window,
            text="Amount"
        ).pack()

        amount_entry = tk.Entry(
            update_window,
            width=30
        )

        amount_entry.pack(pady=5)

        amount_entry.insert(
            0,
            values[2]
        )

        tk.Label(
            update_window,
            text="Category"
        ).pack()

        category_combo = ttk.Combobox(
            update_window,
            values=CATEGORIES,
            state="readonly",
            width=27
        )

        category_combo.pack(pady=5)

        category_combo.set(
            values[3]
        )

        tk.Label(
            update_window,
            text="Description"
        ).pack()

        description_entry = tk.Entry(
            update_window,
            width=30
        )

        description_entry.pack(pady=5)

        description_entry.insert(
            0,
            values[4]
        )

        tk.Label(
            update_window,
            text="Date (YYYY-MM-DD)"
        ).pack()

        date_entry = tk.Entry(
            update_window,
            width=30
        )

        date_entry.pack(pady=5)

        date_entry.insert(
            0,
            values[5]
        )

        def save_update():

            try:

                amount = float(
                    amount_entry.get()
                )

                if amount <= 0:

                    messagebox.showerror(
                        "Error",
                        "Amount must be greater than 0."
                    )

                    return

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Please enter a valid amount."
                )

                return

            category = category_combo.get()
            description = description_entry.get()
            date = date_entry.get()

            conn = sqlite3.connect(
                "expenses.db"
            )

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE transactions
                SET amount = ?,
                    category = ?,
                    description = ?,
                    date = ?
                WHERE id = ?
            """, (
                amount,
                category,
                description,
                date,
                transaction_id
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Transaction updated successfully!"
            )

            update_window.destroy()

            apply_filter()

        tk.Button(
            update_window,
            text="Save Update",
            width=15,
            height=2,
            command=save_update
        ).pack(pady=20)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Apply Filter",
        width=15,
        command=apply_filter
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Clear Filter",
        width=15,
        command=clear_filter
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update Selected",
        width=15,
        command=update_selected
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete Selected",
        width=15,
        command=delete_selected
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    load_transactions()


def create_dashboard():

    root = tk.Tk()

    root.title(
        "Personal Expense Tracker"
    )

    root.geometry(
        "750x820"
    )

    root.resizable(
        False,
        False
    )

    title = tk.Label(
        root,
        text="Personal Expense Tracker",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)

    summary_frame = tk.Frame(root)
    summary_frame.pack(pady=10)

    income_label = tk.Label(
        summary_frame,
        text="Total Income: ₹0",
        font=("Arial", 14, "bold")
    )

    income_label.grid(
        row=0,
        column=0,
        padx=30,
        pady=10
    )

    expense_label = tk.Label(
        summary_frame,
        text="Total Expense: ₹0",
        font=("Arial", 14, "bold")
    )

    expense_label.grid(
        row=0,
        column=1,
        padx=30,
        pady=10
    )

    balance_label = tk.Label(
        summary_frame,
        text="Balance: ₹0",
        font=("Arial", 14, "bold")
    )

    balance_label.grid(
        row=0,
        column=2,
        padx=30,
        pady=10
    )

    def update_dashboard():

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Income'
        """)

        total_income = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
        """)

        total_expense = cursor.fetchone()[0]

        conn.close()

        balance = (
            total_income -
            total_expense
        )

        income_label.config(
            text=f"Total Income: ₹{total_income:.2f}"
        )

        expense_label.config(
            text=f"Total Expense: ₹{total_expense:.2f}"
        )

        balance_label.config(
            text=f"Balance: ₹{balance:.2f}"
        )

        root.after(
            1000,
            update_dashboard
        )

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Add Income",
        width=20,
        height=2,
        font=("Arial", 12),
        command=lambda: add_transaction("Income")
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="Add Expense",
        width=20,
        height=2,
        font=("Arial", 12),
        command=lambda: add_transaction("Expense")
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="View Transactions",
        width=20,
        height=2,
        font=("Arial", 12),
        command=view_transactions
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="Reports & Charts",
        width=20,
        height=2,
        font=("Arial", 12),
        command=show_reports
    ).grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="Monthly Summary",
        width=20,
        height=2,
        font=("Arial", 12),
        command=show_summary
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="AI Spending Suggestions",
        width=20,
        height=2,
        font=("Arial", 12),
        command=show_ai_suggestions
    ).grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="Budget & Spending Limit",
        width=20,
        height=2,
        font=("Arial", 12),
        command=show_budget
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="📈 Monthly Spending Comparison",
        width=20,
        height=2,
        font=("Arial", 12),
        command=monthly_spending_comparison
    ).grid(
        row=3,
        column=1,
        padx=10,
        pady=10
    )

    tk.Button(
        button_frame,
        text="🎯 Financial Goals",
        width=20,
        height=2,
        font=("Arial", 12),
        command=show_financial_goals
    ).grid(
        row=4,
        column=0,
        columnspan=2,
        padx=10,
        pady=10
    )

    update_dashboard()

    root.mainloop()