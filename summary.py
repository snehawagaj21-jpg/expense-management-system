import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# THEME
# ============================================================

BG = "#07111F"
CARD = "#0D1B2A"
CARD_LIGHT = "#132A40"

BLUE = "#1683FF"
BLUE_LIGHT = "#42A5FF"
BLUE_DARK = "#0B5DB7"

WHITE = "#FFFFFF"
LIGHT_TEXT = "#BFD7EA"

ENTRY_BG = "#10283D"
BORDER = "#1E4E73"

SHADOW = "#020810"


# ============================================================
# PREMIUM BUTTON
# ============================================================

def premium_button(parent, text, command, width=210):

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
            outline=outline
        )

    # Shadow
    cut_shape(
        5, 7,
        width + 5,
        height + 7,
        cut,
        SHADOW
    )

    # Depth
    depth = cut_shape(
        3, 4,
        width + 3,
        height + 4,
        cut,
        BLUE_DARK
    )

    # Main
    main = cut_shape(
        1, 1,
        width,
        height,
        cut,
        BLUE,
        "#56AEFF"
    )

    # Shine
    shine = canvas.create_line(
        cut + 7,
        7,
        width - cut - 7,
        7,
        fill="#7CC4FF",
        width=2
    )

    # Left accent
    accent = canvas.create_line(
        9,
        17,
        9,
        height - 17,
        fill="#8DCEFF",
        width=3
    )

    canvas.create_text(
        width / 2,
        height / 2 + 1,
        text=text,
        fill=WHITE,
        font=("Segoe UI", 10, "bold")
    )

    def enter(event):

        canvas.itemconfig(main, fill=BLUE_LIGHT)
        canvas.itemconfig(depth, fill=BLUE)
        canvas.itemconfig(shine, fill=WHITE)
        canvas.itemconfig(accent, fill=WHITE)

    def leave(event):

        canvas.itemconfig(main, fill=BLUE)
        canvas.itemconfig(depth, fill=BLUE_DARK)
        canvas.itemconfig(shine, fill="#7CC4FF")
        canvas.itemconfig(accent, fill="#8DCEFF")

    canvas.bind("<Enter>", enter)
    canvas.bind("<Leave>", leave)
    canvas.bind("<Button-1>", lambda event: command())

    canvas.pack()

    return canvas


# ============================================================
# 3D CARD
# ============================================================

def create_card(parent, width, height):

    container = tk.Frame(
        parent,
        bg=parent.cget("bg")
    )

    container.pack(
        pady=8
    )

    # Shadow
    shadow = tk.Frame(
        container,
        bg=SHADOW
    )

    shadow.place(
        x=7,
        y=7,
        width=width,
        height=height
    )

    # Depth
    depth = tk.Frame(
        container,
        bg="#0A2740"
    )

    depth.place(
        x=4,
        y=4,
        width=width,
        height=height
    )

    # Main card
    card = tk.Frame(
        container,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.place(
        x=0,
        y=0,
        width=width,
        height=height
    )

    # Blue top line
    tk.Frame(
        card,
        bg=BLUE,
        height=3
    ).place(
        x=0,
        y=0,
        relwidth=1
    )

    container.config(
        width=width + 8,
        height=height + 8
    )

    return card


# ============================================================
# MONTHLY SUMMARY
# ============================================================

def show_summary():

    window = tk.Toplevel()

    window.title(
        "Monthly Summary"
    )

    window.geometry(
        "780x650"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        bg=BG
    )

    # ========================================================
    # TITLE
    # ========================================================

    tk.Label(
        window,
        text="MONTHLY SUMMARY",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        window,
        text="View your monthly income, expenses and spending pattern",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 18)
    )

    # ========================================================
    # MONTH SELECTION CARD
    # ========================================================

    selection_card = create_card(
        window,
        650,
        85
    )

    tk.Label(
        selection_card,
        text="SELECT MONTH",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).place(
        x=35,
        y=28
    )

    month_box = ttk.Combobox(
        selection_card,
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
        width=25,
        state="readonly",
        font=("Arial", 10)
    )

    month_box.place(
        x=170,
        y=24,
        width=250,
        height=32
    )

    month_box.set(
        "09 - September"
    )

    # ========================================================
    # SUMMARY CARD
    # ========================================================

    summary_card = create_card(
        window,
        650,
        300
    )

    income_label = tk.Label(
        summary_card,
        text="TOTAL INCOME\n₹ 0.00",
        font=("Arial", 14, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    income_label.pack(
        pady=(25, 10)
    )

    expense_label = tk.Label(
        summary_card,
        text="TOTAL EXPENSE\n₹ 0.00",
        font=("Arial", 14, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    expense_label.pack(
        pady=10
    )

    balance_label = tk.Label(
        summary_card,
        text="BALANCE\n₹ 0.00",
        font=("Arial", 14, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    )

    balance_label.pack(
        pady=10
    )

    top_category_label = tk.Label(
        summary_card,
        text="TOP SPENDING CATEGORY\n-",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=WHITE
    )

    top_category_label.pack(
        pady=10
    )

    alert_label = tk.Label(
        summary_card,
        text="",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT,
        wraplength=560
    )

    alert_label.pack(
        pady=(8, 5)
    )

    # ========================================================
    # CALCULATE
    # ========================================================

    def calculate_summary():

        selected_month = month_box.get()

        if not selected_month:

            messagebox.showwarning(
                "Select Month",
                "Please select a month."
            )

            return

        month_number = selected_month[:2]

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        # Income
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Income'
            AND substr(date, 6, 2) = ?
        """, (
            month_number,
        ))

        total_income = cursor.fetchone()[0]

        # Expense
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
        """, (
            month_number,
        ))

        total_expense = cursor.fetchone()[0]

        # Top category
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE transaction_type = 'Expense'
            AND substr(date, 6, 2) = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
            LIMIT 1
        """, (
            month_number,
        ))

        top_category = cursor.fetchone()

        conn.close()

        balance = (
            total_income -
            total_expense
        )

        # ----------------------------------------------------
        # UPDATE LABELS
        # ----------------------------------------------------

        income_label.config(
            text=(
                f"TOTAL INCOME\n"
                f"₹ {total_income:.2f}"
            )
        )

        expense_label.config(
            text=(
                f"TOTAL EXPENSE\n"
                f"₹ {total_expense:.2f}"
            )
        )

        balance_label.config(
            text=(
                f"BALANCE\n"
                f"₹ {balance:.2f}"
            )
        )

        if top_category:

            top_category_label.config(
                text=(
                    f"TOP SPENDING CATEGORY\n"
                    f"{top_category[0]}"
                )
            )

        else:

            top_category_label.config(
                text="TOP SPENDING CATEGORY\n-"
            )

        # ----------------------------------------------------
        # ALERT
        # ----------------------------------------------------

        if (
            total_expense > total_income
            and total_income > 0
        ):

            alert_label.config(
                text=(
                    "⚠ Overspending Alert!\n"
                    "Expenses are higher than income."
                ),
                fg=BLUE_LIGHT
            )

        elif (
            total_expense > 0
            and total_income == 0
        ):

            alert_label.config(
                text=(
                    "⚠ Expenses recorded but "
                    "no income found."
                ),
                fg=BLUE_LIGHT
            )

        else:

            alert_label.config(
                text=(
                    "✓ Your spending is within "
                    "your income."
                ),
                fg=LIGHT_TEXT
            )

    # ========================================================
    # VIEW SUMMARY BUTTON
    # ========================================================

    premium_button(
        window,
        "VIEW SUMMARY",
        calculate_summary,
        220
    )

    calculate_summary()
