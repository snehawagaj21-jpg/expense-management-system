import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from datetime import date

from reports import show_reports
from summary import show_summary
from ai_suggestions import show_ai_suggestions
from budget import show_budget
from financial_goals import show_financial_goals


# ============================================================
# THEME / COLORS
# ============================================================

BG = "#07111F"
CARD = "#0D1B2A"
CARD_LIGHT = "#132A40"

BLUE = "#1683FF"
BLUE_LIGHT = "#42A5FF"
BLUE_DARK = "#0B5DB7"

WHITE = "#FFFFFF"
LIGHT_TEXT = "#BFD7EA"
GRAY = "#78909C"

ENTRY_BG = "#10283D"
BORDER = "#1E4E73"

SHADOW = "#020810"
SHADOW_LIGHT = "#061A2C"


# ============================================================
# CONSTANTS
# ============================================================

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


# ============================================================
# 3D BLUE BUTTON
# ============================================================

# ============================================================
# PREMIUM CUT-CORNER BLUE BUTTON
# ============================================================

def blue_button(parent, text, x, y, width, command):

    height = 50
    cut = 10

    canvas = tk.Canvas(
        parent,
        width=width + 12,
        height=height + 12,
        bg=parent.cget("bg"),
        highlightthickness=0,
        bd=0
    )

    canvas.place(
        x=x,
        y=y
    )

    # --------------------------------------------------------
    # CUT-CORNER SHAPE
    # --------------------------------------------------------

    def cut_shape(x1, y1, x2, y2, c, fill, outline=""):

        points = [
            x1 + c, y1,
            x2 - c, y1,
            x2, y1 + c,
            x2, y2 - c,
            x2 - c, y2,
            x1 + c, y2,
            x1, y2 - c,
            x1, y1 + c
        ]

        return canvas.create_polygon(
            points,
            fill=fill,
            outline=outline,
            width=1
        )

    # --------------------------------------------------------
    # DEEP SHADOW
    # --------------------------------------------------------

    shadow = cut_shape(
        5, 7,
        width + 5,
        height + 7,
        cut,
        SHADOW
    )

    # --------------------------------------------------------
    # BLUE 3D DEPTH
    # --------------------------------------------------------

    depth = cut_shape(
        3, 4,
        width + 3,
        height + 4,
        cut,
        BLUE_DARK
    )

    # --------------------------------------------------------
    # OUTER BORDER
    # --------------------------------------------------------

    border = cut_shape(
        1, 1,
        width + 1,
        height + 1,
        cut,
        "#0A4F91",
        "#2C8FEF"
    )

    # --------------------------------------------------------
    # MAIN BUTTON
    # --------------------------------------------------------

    main = cut_shape(
        2, 2,
        width - 1,
        height - 1,
        cut - 2,
        BLUE,
        "#56AEFF"
    )

    # --------------------------------------------------------
    # DARK INNER PANEL
    # --------------------------------------------------------

    inner = cut_shape(
        7, 7,
        width - 7,
        height - 7,
        cut - 3,
        "#1174D8",
        ""
    )

    # --------------------------------------------------------
    # TOP LIGHT SHINE
    # --------------------------------------------------------

    shine = canvas.create_line(
        cut + 7,
        7,
        width - cut - 7,
        7,
        fill="#7CC4FF",
        width=2
    )

    # --------------------------------------------------------
    # LEFT ACCENT
    # --------------------------------------------------------

    accent = canvas.create_line(
        9,
        17,
        9,
        height - 17,
        fill="#8DCEFF",
        width=3
    )

    # --------------------------------------------------------
    # BUTTON TEXT
    # --------------------------------------------------------

    label = canvas.create_text(
        width / 2,
        height / 2 + 1,
        text=text,
        fill=WHITE,
        font=("Segoe UI", 10, "bold")
    )

    # --------------------------------------------------------
    # HOVER EFFECT
    # --------------------------------------------------------

    def on_enter(event):

        canvas.itemconfig(
            main,
            fill=BLUE_LIGHT
        )

        canvas.itemconfig(
            inner,
            fill="#238BE8"
        )

        canvas.itemconfig(
            border,
            fill="#116CC4"
        )

        canvas.itemconfig(
            shine,
            fill=WHITE
        )

        canvas.itemconfig(
            accent,
            fill=WHITE
        )

    def on_leave(event):

        canvas.itemconfig(
            main,
            fill=BLUE
        )

        canvas.itemconfig(
            inner,
            fill="#1174D8"
        )

        canvas.itemconfig(
            border,
            fill="#0A4F91"
        )

        canvas.itemconfig(
            shine,
            fill="#7CC4FF"
        )

        canvas.itemconfig(
            accent,
            fill="#8DCEFF"
        )

    # --------------------------------------------------------
    # CLICK
    # --------------------------------------------------------

    def on_click(event):
        command()

    canvas.bind(
        "<Enter>",
        on_enter
    )

    canvas.bind(
        "<Leave>",
        on_leave
    )

    canvas.bind(
        "<Button-1>",
        on_click
    )

    return canvas
# ============================================================
# 3D CARD
# ============================================================

def create_card(parent, x, y, width, height):

    # --------------------------------------------------------
    # BIG DARK SHADOW
    # --------------------------------------------------------

    shadow = tk.Frame(
        parent,
        bg=SHADOW
    )

    shadow.place(
        x=x + 8,
        y=y + 8,
        width=width,
        height=height
    )

    # --------------------------------------------------------
    # BLUE DEPTH LAYER
    # --------------------------------------------------------

    depth = tk.Frame(
        parent,
        bg="#0A2740"
    )

    depth.place(
        x=x + 4,
        y=y + 4,
        width=width,
        height=height
    )

    # --------------------------------------------------------
    # MAIN CARD
    # --------------------------------------------------------

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.place(
        x=x,
        y=y,
        width=width,
        height=height
    )

    # --------------------------------------------------------
    # TOP BLUE HIGHLIGHT
    # --------------------------------------------------------

    highlight = tk.Frame(
        card,
        bg=BLUE_DARK
    )

    highlight.place(
        x=0,
        y=0,
        relwidth=1,
        height=3
    )

    return card


# ============================================================
# BUDGET WARNING
# ============================================================

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
            "Budget Warning",

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
            "Spending Limit Warning",

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


# ============================================================
# ADD TRANSACTION
# ============================================================

def add_transaction(transaction_type):

    window = tk.Toplevel()

    window.title(
        "Add " + transaction_type
    )

    window.geometry(
        "520x670"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        bg=BG
    )

    # --------------------------------------------------------
    # 3D CARD
    # --------------------------------------------------------

    shadow = tk.Frame(
        window,
        bg=SHADOW
    )

    shadow.place(
        x=30,
        y=30,
        width=460,
        height=590
    )

    depth = tk.Frame(
        window,
        bg="#0A2740"
    )

    depth.place(
        x=24,
        y=24,
        width=460,
        height=590
    )

    card = tk.Frame(
        window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.place(
        x=18,
        y=18,
        width=460,
        height=590
    )

    # --------------------------------------------------------
    # BLUE TOP LINE
    # --------------------------------------------------------

    tk.Frame(
        card,
        bg=BLUE,
        height=4
    ).place(
        x=0,
        y=0,
        relwidth=1
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    tk.Label(
        card,
        text="ADD " + transaction_type.upper(),
        font=("Arial", 21, "bold"),
        bg=CARD,
        fg=WHITE
    ).pack(
        pady=(28, 5)
    )

    tk.Label(
        card,
        text="Enter your transaction details",
        font=("Arial", 10),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 22)
    )

    # --------------------------------------------------------
    # AMOUNT
    # --------------------------------------------------------

    tk.Label(
        card,
        text="Amount",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=45
    )

    amount_entry = tk.Entry(
        card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 11)
    )

    amount_entry.pack(
        padx=45,
        fill="x",
        ipady=10,
        pady=(5, 15)
    )

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    tk.Label(
        card,
        text="Category",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=45
    )

    category_combo = ttk.Combobox(
        card,
        values=CATEGORIES,
        state="readonly",
        font=("Arial", 10)
    )

    category_combo.pack(
        padx=45,
        fill="x",
        ipady=6,
        pady=(5, 15)
    )

    category_combo.set(
        CATEGORIES[0]
    )

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    tk.Label(
        card,
        text="Description",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=45
    )

    description_entry = tk.Entry(
        card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 11)
    )

    description_entry.pack(
        padx=45,
        fill="x",
        ipady=10,
        pady=(5, 15)
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    tk.Label(
        card,
        text="Date (YYYY-MM-DD)",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=45
    )

    date_entry = tk.Entry(
        card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 11)
    )

    date_entry.pack(
        padx=45,
        fill="x",
        ipady=10,
        pady=(5, 22)
    )

    date_entry.insert(
        0,
        str(date.today())
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save_transaction():

        amount = amount_entry.get().strip()

        category = category_combo.get()

        description = description_entry.get().strip()

        transaction_date = date_entry.get().strip()

        if not amount:

            messagebox.showerror(
                "Error",
                "Please enter amount."
            )

            return

        if not transaction_date:

            messagebox.showerror(
                "Error",
                "Please enter date."
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

        try:

            date.fromisoformat(
                transaction_date
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Date must be in YYYY-MM-DD format."
            )

            return

        if transaction_type == "Expense":

            allowed = check_budget_warning(
                category,
                amount
            )

            if not allowed:

                return

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (
                transaction_type,
                amount,
                category,
                description,
                date
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type,
            amount,
            category,
            description,
            transaction_date
        ))

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            transaction_type +
            " added successfully!"
        )

        window.destroy()

    # --------------------------------------------------------
    # 3D SAVE BUTTON
    # --------------------------------------------------------

    save_shadow = tk.Frame(
        card,
        bg=SHADOW
    )

    save_shadow.pack(
        padx=47,
        fill="x"
    )

    save_button = tk.Button(
        card,
        text="SAVE TRANSACTION",
        command=save_transaction,
        bg=BLUE,
        fg=WHITE,
        activebackground=BLUE_LIGHT,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        font=("Arial", 11, "bold"),
        cursor="hand2"
    )

    save_button.pack(
        padx=45,
        fill="x",
        ipady=11
    )

    def save_enter(event):

        save_button.configure(
            bg=BLUE_LIGHT
        )

    def save_leave(event):

        save_button.configure(
            bg=BLUE
        )

    save_button.bind(
        "<Enter>",
        save_enter
    )

    save_button.bind(
        "<Leave>",
        save_leave
    )


# ============================================================
# MONTHLY SPENDING COMPARISON
# ============================================================

def monthly_spending_comparison():

    window = tk.Toplevel()

    window.title(
        "Monthly Spending Comparison"
    )

    window.geometry(
        "680x620"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        bg=BG
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    tk.Label(
        window,
        text="MONTHLY SPENDING COMPARISON",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        window,
        text="Compare your spending with the previous month",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 20)
    )

    # --------------------------------------------------------
    # SELECTION CARD
    # --------------------------------------------------------

    selection_card = create_card(
        window,
        40,
        100,
        600,
        105
    )

    tk.Label(
        selection_card,
        text="SELECT MONTH",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        side="left",
        padx=(35, 15)
    )

    month_combo = ttk.Combobox(
        selection_card,
        values=MONTHS,
        state="readonly",
        width=22,
        font=("Arial", 10)
    )

    month_combo.pack(
        side="left"
    )

    month_combo.set(
        MONTHS[0]
    )

    # --------------------------------------------------------
    # RESULT CARD
    # --------------------------------------------------------

    result_card = create_card(
        window,
        40,
        225,
        600,
        285
    )

    current_label = tk.Label(
        result_card,
        text="Current Month Expense: ₹0.00",
        font=("Arial", 13, "bold"),
        bg=CARD,
        fg=WHITE
    )

    current_label.pack(
        pady=(30, 15)
    )

    previous_label = tk.Label(
        result_card,
        text="Previous Month Expense: ₹0.00",
        font=("Arial", 13, "bold"),
        bg=CARD,
        fg=WHITE
    )

    previous_label.pack(
        pady=15
    )

    difference_label = tk.Label(
        result_card,
        text="Difference: ₹0.00",
        font=("Arial", 13, "bold"),
        bg=CARD,
        fg=WHITE
    )

    difference_label.pack(
        pady=15
    )

    percentage_label = tk.Label(
        result_card,
        text="Change: 0%",
        font=("Arial", 13, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    percentage_label.pack(
        pady=15
    )

    message_label = tk.Label(
        result_card,
        text="Select a month and click Compare.",
        font=("Arial", 10),
        bg=CARD,
        fg=LIGHT_TEXT,
        wraplength=470
    )

    message_label.pack(
        pady=10
    )

    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    def compare_months():

        selected_month = month_combo.get()

        if not selected_month:

            return

        current_number = int(
            selected_month[:2]
        )

        if current_number == 1:

            previous_number = 12

        else:

            previous_number = (
                current_number - 1
            )

        current_month = (
            f"{current_number:02d}"
        )

        previous_month = (
            f"{previous_number:02d}"
        )

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
        """, (
            current_month,
        ))

        current_expense = (
            cursor.fetchone()[0]
        )

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
        """, (
            previous_month,
        ))

        previous_expense = (
            cursor.fetchone()[0]
        )

        conn.close()

        difference = (
            current_expense -
            previous_expense
        )

        if previous_expense > 0:

            percentage = (
                difference /
                previous_expense
            ) * 100

        else:

            percentage = 0

        current_label.config(
            text=(
                f"Current Month Expense: "
                f"₹{current_expense:.2f}"
            )
        )

        previous_label.config(
            text=(
                f"Previous Month Expense: "
                f"₹{previous_expense:.2f}"
            )
        )

        difference_label.config(
            text=(
                f"Difference: "
                f"₹{abs(difference):.2f}"
            )
        )

        if previous_expense == 0 and current_expense > 0:

            percentage_label.config(
                text="Change: New Spending"
            )

            message_label.config(
                text=(
                    "Spending was recorded this month, "
                    "but no spending was recorded "
                    "for the previous month."
                )
            )

        elif current_expense > previous_expense:

            percentage_label.config(
                text=(
                    f"Spending Increased: "
                    f"{percentage:.2f}%"
                )
            )

            message_label.config(
                text=(
                    "Your spending increased "
                    "compared to the previous month."
                )
            )

        elif current_expense < previous_expense:

            percentage_label.config(
                text=(
                    f"Spending Decreased: "
                    f"{abs(percentage):.2f}%"
                )
            )

            message_label.config(
                text=(
                    "Your spending decreased "
                    "compared to the previous month."
                )
            )

        else:

            percentage_label.config(
                text="Spending Change: 0%"
            )

            message_label.config(
                text=(
                    "Your spending is the same "
                    "as the previous month."
                )
            )

    blue_button(
        window,
        "COMPARE",
        235,
        535,
        210,
        compare_months
    )


# ============================================================
# VIEW TRANSACTIONS
# ============================================================

def view_transactions():

    window = tk.Toplevel()

    window.title(
        "View Transactions"
    )

    window.geometry(
        "1100x700"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        bg=BG
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    tk.Label(
        window,
        text="TRANSACTION HISTORY",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        window,
        text="Search, filter, update or delete transactions",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 15)
    )

    # --------------------------------------------------------
    # FILTER CARD
    # --------------------------------------------------------

    filter_card = create_card(
        window,
        30,
        90,
        1040,
        100
    )

    tk.Label(
        filter_card,
        text="Search",
        bg=CARD,
        fg=LIGHT_TEXT,
        font=("Arial", 9, "bold")
    ).place(
        x=25,
        y=18
    )

    search_entry = tk.Entry(
        filter_card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 10)
    )

    search_entry.place(
        x=25,
        y=45,
        width=220,
        height=30
    )

    tk.Label(
        filter_card,
        text="Category",
        bg=CARD,
        fg=LIGHT_TEXT,
        font=("Arial", 9, "bold")
    ).place(
        x=275,
        y=18
    )

    category_filter = ttk.Combobox(
        filter_card,
        values=["All"] + CATEGORIES,
        state="readonly",
        font=("Arial", 9)
    )

    category_filter.place(
        x=275,
        y=45,
        width=170,
        height=30
    )

    category_filter.set(
        "All"
    )

    tk.Label(
        filter_card,
        text="Month",
        bg=CARD,
        fg=LIGHT_TEXT,
        font=("Arial", 9, "bold")
    ).place(
        x=465,
        y=18
    )

    month_filter = ttk.Combobox(
        filter_card,
        values=["All"] + MONTHS,
        state="readonly",
        font=("Arial", 9)
    )

    month_filter.place(
        x=465,
        y=45,
        width=170,
        height=30
    )

    month_filter.set(
        "All"
    )

    # --------------------------------------------------------
    # TABLE CARD
    # --------------------------------------------------------

    table_card = create_card(
        window,
        30,
        205,
        1040,
        355
    )

    columns = (
        "ID",
        "Type",
        "Amount",
        "Category",
        "Description",
        "Date"
    )

    tree = ttk.Treeview(
        table_card,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

    tree.column(
        "ID",
        width=50,
        anchor="center"
    )

    tree.column(
        "Type",
        width=110,
        anchor="center"
    )

    tree.column(
        "Amount",
        width=120,
        anchor="center"
    )

    tree.column(
        "Category",
        width=140,
        anchor="center"
    )

    tree.column(
        "Description",
        width=330,
        anchor="w"
    )

    tree.column(
        "Date",
        width=140,
        anchor="center"
    )

    tree.place(
        x=15,
        y=15,
        width=980,
        height=320
    )

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )

    scrollbar.place(
        x=995,
        y=15,
        height=320
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    def load_transactions(
        search="",
        category="All",
        month="All"
    ):

        for item in tree.get_children():

            tree.delete(
                item
            )

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        query = """
            SELECT
                id,
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

            search_value = (
                "%" +
                search +
                "%"
            )

            params.extend([
                search_value,
                search_value,
                search_value
            ])

        if category != "All":

            query += """
                AND category = ?
            """

            params.append(
                category
            )

        if month != "All":

            month_number = month[:2]

            query += """
                AND substr(date, 6, 2) = ?
            """

            params.append(
                month_number
            )

        query += """
            ORDER BY date DESC, id DESC
        """

        cursor.execute(
            query,
            params
        )

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    f"₹{row[2]:.2f}",
                    row[3],
                    row[4],
                    row[5]
                )
            )

    # --------------------------------------------------------
    # APPLY FILTER
    # --------------------------------------------------------

    def apply_filter():

        load_transactions(
            search_entry.get().strip(),
            category_filter.get(),
            month_filter.get()
        )

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    def clear_filter():

        search_entry.delete(
            0,
            tk.END
        )

        category_filter.set(
            "All"
        )

        month_filter.set(
            "All"
        )

        load_transactions()

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    def delete_selected():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a transaction first."
            )

            return

        item = tree.item(
            selected[0]
        )

        transaction_id = (
            item["values"][0]
        )

        answer = messagebox.askyesno(
            "Delete Transaction",
            "Are you sure you want to delete this transaction?"
        )

        if not answer:

            return

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        conn.commit()

        conn.close()

        load_transactions(
            search_entry.get().strip(),
            category_filter.get(),
            month_filter.get()
        )

        messagebox.showinfo(
            "Deleted",
            "Transaction deleted successfully."
        )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update_selected():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a transaction first."
            )

            return

        item = tree.item(
            selected[0]
        )

        values = item["values"]

        transaction_id = values[0]

        old_amount = str(
            values[2]
        ).replace(
            "₹",
            ""
        )

        old_category = values[3]

        old_description = values[4]

        old_date = values[5]

        update_window = tk.Toplevel()

        update_window.title(
            "Update Transaction"
        )

        update_window.geometry(
            "520x650"
        )

        update_window.resizable(
            False,
            False
        )

        update_window.configure(
            bg=BG
        )

        # 3D card
        shadow = tk.Frame(
            update_window,
            bg=SHADOW
        )

        shadow.place(
            x=28,
            y=28,
            width=460,
            height=590
        )

        depth = tk.Frame(
            update_window,
            bg="#0A2740"
        )

        depth.place(
            x=22,
            y=22,
            width=460,
            height=590
        )

        card = tk.Frame(
            update_window,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=2
        )

        card.place(
            x=16,
            y=16,
            width=460,
            height=590
        )

        tk.Frame(
            card,
            bg=BLUE,
            height=4
        ).place(
            x=0,
            y=0,
            relwidth=1
        )

        tk.Label(
            card,
            text="UPDATE TRANSACTION",
            font=("Arial", 19, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(
            pady=(28, 25)
        )

        # Amount
        tk.Label(
            card,
            text="Amount",
            bg=CARD,
            fg=LIGHT_TEXT,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=45
        )

        amount_entry = tk.Entry(
            card,
            bg=ENTRY_BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 11)
        )

        amount_entry.pack(
            padx=45,
            fill="x",
            ipady=9,
            pady=(5, 15)
        )

        amount_entry.insert(
            0,
            old_amount
        )

        # Category
        tk.Label(
            card,
            text="Category",
            bg=CARD,
            fg=LIGHT_TEXT,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=45
        )

        category_combo = ttk.Combobox(
            card,
            values=CATEGORIES,
            state="readonly"
        )

        category_combo.pack(
            padx=45,
            fill="x",
            ipady=5,
            pady=(5, 15)
        )

        category_combo.set(
            old_category
        )

        # Description
        tk.Label(
            card,
            text="Description",
            bg=CARD,
            fg=LIGHT_TEXT,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=45
        )

        description_entry = tk.Entry(
            card,
            bg=ENTRY_BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 11)
        )

        description_entry.pack(
            padx=45,
            fill="x",
            ipady=9,
            pady=(5, 15)
        )

        description_entry.insert(
            0,
            old_description
        )

        # Date
        tk.Label(
            card,
            text="Date (YYYY-MM-DD)",
            bg=CARD,
            fg=LIGHT_TEXT,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=45
        )

        date_entry = tk.Entry(
            card,
            bg=ENTRY_BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 11)
        )

        date_entry.pack(
            padx=45,
            fill="x",
            ipady=9,
            pady=(5, 25)
        )

        date_entry.insert(
            0,
            old_date
        )

        # ----------------------------------------------------
        # SAVE UPDATE
        # ----------------------------------------------------

        def save_update():

            try:

                new_amount = float(
                    amount_entry.get()
                )

                if new_amount <= 0:

                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Please enter a valid amount."
                )

                return

            new_category = (
                category_combo.get()
            )

            new_description = (
                description_entry.get()
            )

            new_date = (
                date_entry.get().strip()
            )

            try:

                date.fromisoformat(
                    new_date
                )

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Date must be in YYYY-MM-DD format."
                )

                return

            conn = sqlite3.connect(
                "expenses.db"
            )

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE transactions
                SET
                    amount = ?,
                    category = ?,
                    description = ?,
                    date = ?
                WHERE id = ?
            """, (
                new_amount,
                new_category,
                new_description,
                new_date,
                transaction_id
            ))

            conn.commit()

            conn.close()

            update_window.destroy()

            load_transactions(
                search_entry.get().strip(),
                category_filter.get(),
                month_filter.get()
            )

            messagebox.showinfo(
                "Success",
                "Transaction updated successfully."
            )

        # ----------------------------------------------------
        # 3D SAVE BUTTON
        # ----------------------------------------------------

        update_shadow = tk.Frame(
            card,
            bg=SHADOW
        )

        update_shadow.pack(
            padx=47,
            fill="x"
        )

        update_button = tk.Button(
            card,
            text="SAVE CHANGES",
            command=save_update,
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2"
        )

        update_button.pack(
            padx=45,
            fill="x",
            ipady=10
        )

        update_button.bind(
            "<Enter>",
            lambda e: update_button.configure(
                bg=BLUE_LIGHT
            )
        )

        update_button.bind(
            "<Leave>",
            lambda e: update_button.configure(
                bg=BLUE
            )
        )

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    blue_button(
        window,
        "APPLY FILTER",
        45,
        580,
        170,
        apply_filter
    )

    blue_button(
        window,
        "CLEAR",
        235,
        580,
        130,
        clear_filter
    )

    blue_button(
        window,
        "UPDATE",
        380,
        580,
        130,
        update_selected
    )

    blue_button(
        window,
        "DELETE",
        525,
        580,
        130,
        delete_selected
    )

    blue_button(
        window,
        "REFRESH",
        670,
        580,
        130,
        lambda: load_transactions()
    )

    load_transactions()


# ============================================================
# DASHBOARD
# ============================================================

def create_dashboard():

    root = tk.Tk()

    root.title(
        "Personal Expense Tracker"
    )

    root.geometry(
        "1000x760"
    )

    root.resizable(
        False,
        False
    )

    root.configure(
        bg=BG
    )

    # ========================================================
    # TITLE
    # ========================================================

    tk.Label(
        root,
        text="PERSONAL EXPENSE TRACKER",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        root,
        text="Manage your income, expenses and financial goals",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 20)
    )

    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    income_card = create_card(
        root,
        50,
        95,
        280,
        105
    )

    tk.Label(
        income_card,
        text="TOTAL INCOME",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(20, 5)
    )

    income_label = tk.Label(
        income_card,
        text="₹0.00",
        font=("Arial", 21, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    income_label.pack()

    expense_card = create_card(
        root,
        360,
        95,
        280,
        105
    )

    tk.Label(
        expense_card,
        text="TOTAL EXPENSE",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(20, 5)
    )

    expense_label = tk.Label(
        expense_card,
        text="₹0.00",
        font=("Arial", 21, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    expense_label.pack()

    balance_card = create_card(
        root,
        670,
        95,
        280,
        105
    )

    tk.Label(
        balance_card,
        text="CURRENT BALANCE",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(20, 5)
    )

    balance_label = tk.Label(
        balance_card,
        text="₹0.00",
        font=("Arial", 21, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    balance_label.pack()

    # ========================================================
    # QUICK ACTIONS CARD
    # ========================================================

    button_card = create_card(
        root,
        50,
        230,
        900,
        485
    )

    tk.Label(
        button_card,
        text="QUICK ACTIONS",
        font=("Arial", 14, "bold"),
        bg=CARD,
        fg=WHITE
    ).pack(
        pady=(20, 10)
    )

    tk.Label(
        button_card,
        text="Choose an option",
        font=("Arial", 9),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 20)
    )

    # --------------------------------------------------------
    # ROW 1
    # --------------------------------------------------------

    blue_button(
        button_card,
        "ADD INCOME",
        70,
        85,
        350,
        lambda: add_transaction("Income")
    )

    blue_button(
        button_card,
        "ADD EXPENSE",
        480,
        85,
        350,
        lambda: add_transaction("Expense")
    )

    # --------------------------------------------------------
    # ROW 2
    # --------------------------------------------------------

    blue_button(
        button_card,
        "VIEW TRANSACTIONS",
        70,
        145,
        350,
        view_transactions
    )

    blue_button(
        button_card,
        "REPORTS & CHARTS",
        480,
        145,
        350,
        show_reports
    )

    # --------------------------------------------------------
    # ROW 3
    # --------------------------------------------------------

    blue_button(
        button_card,
        "MONTHLY SUMMARY",
        70,
        205,
        350,
        show_summary
    )

    blue_button(
        button_card,
        "AI SPENDING SUGGESTIONS",
        480,
        205,
        350,
        show_ai_suggestions
    )

    # --------------------------------------------------------
    # ROW 4
    # --------------------------------------------------------

    blue_button(
        button_card,
        "BUDGET & SPENDING LIMIT",
        70,
        265,
        350,
        show_budget
    )

    blue_button(
        button_card,
        "MONTHLY COMPARISON",
        480,
        265,
        350,
        monthly_spending_comparison
    )

    # --------------------------------------------------------
    # ROW 5
    # --------------------------------------------------------

    blue_button(
        button_card,
        "FINANCIAL GOALS",
        70,
        325,
        350,
        show_financial_goals
    )

    # ========================================================
    # DASHBOARD UPDATE
    # ========================================================

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

        total_income = (
            cursor.fetchone()[0]
        )

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
        """)

        total_expense = (
            cursor.fetchone()[0]
        )

        conn.close()

        balance = (
            total_income -
            total_expense
        )

        income_label.config(
            text=f"₹{total_income:.2f}"
        )

        expense_label.config(
            text=f"₹{total_expense:.2f}"
        )

        balance_label.config(
            text=f"₹{balance:.2f}"
        )

        root.after(
            1000,
            update_dashboard
        )

    update_dashboard()

    root.mainloop()
