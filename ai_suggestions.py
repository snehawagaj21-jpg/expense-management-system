import tkinter as tk
import sqlite3


# ============================================================
# THEME
# ============================================================

BG = "#07111F"
CARD = "#0D1B2A"

BLUE = "#1683FF"
BLUE_LIGHT = "#42A5FF"
BLUE_DARK = "#0B5DB7"

WHITE = "#FFFFFF"
LIGHT_TEXT = "#BFD7EA"

BORDER = "#1E4E73"
SHADOW = "#020810"


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

    # Blue depth
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

    # Blue top highlight
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
# PREMIUM BUTTON
# ============================================================

def premium_button(parent, text, command, width=220):

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

    # Main button
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

    # Accent
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

        canvas.itemconfig(
            main,
            fill=BLUE_LIGHT
        )

        canvas.itemconfig(
            depth,
            fill=BLUE
        )

        canvas.itemconfig(
            shine,
            fill=WHITE
        )

        canvas.itemconfig(
            accent,
            fill=WHITE
        )

    def leave(event):

        canvas.itemconfig(
            main,
            fill=BLUE
        )

        canvas.itemconfig(
            depth,
            fill=BLUE_DARK
        )

        canvas.itemconfig(
            shine,
            fill="#7CC4FF"
        )

        canvas.itemconfig(
            accent,
            fill="#8DCEFF"
        )

    canvas.bind(
        "<Enter>",
        enter
    )

    canvas.bind(
        "<Leave>",
        leave
    )

    canvas.bind(
        "<Button-1>",
        lambda event: command()
    )

    canvas.pack()

    return canvas


# ============================================================
# AI SPENDING SUGGESTIONS
# ============================================================

def show_ai_suggestions():

    window = tk.Toplevel()

    window.title(
        "AI Spending Suggestions"
    )

    window.geometry(
        "760x680"
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
        text="AI SPENDING SUGGESTIONS",
        font=("Arial", 23, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        window,
        text="Smart insights based on your spending pattern",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 18)
    )

    # ========================================================
    # DATABASE ANALYSIS
    # ========================================================

    conn = sqlite3.connect(
        "expenses.db"
    )

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

    total_expense = (
        result[0]
        if result[0]
        else 0
    )

    conn.close()

    # ========================================================
    # GENERATE SUGGESTIONS
    # ========================================================

    suggestions = []

    if total_expense == 0:

        suggestions.append(
            "No expenses found yet. Start adding expenses "
            "to get suggestions."
        )

    else:

        if category_data:

            top_category = category_data[0][0]

            top_amount = category_data[0][1]

            suggestions.append(
                f"Your highest spending category is "
                f"{top_category} (₹{top_amount:.2f})."
            )

            percentage = (
                top_amount /
                total_expense
            ) * 100

            if percentage > 40:

                suggestions.append(
                    f"{top_category} uses about "
                    f"{percentage:.1f}% of your total expenses."
                )

                suggestions.append(
                    f"Try reducing your {top_category} "
                    f"expenses to improve your savings."
                )

        if total_expense > 5000:

            suggestions.append(
                "Your total expenses are high. Consider "
                "setting a monthly spending limit."
            )

        elif total_expense > 2000:

            suggestions.append(
                "Keep monitoring your expenses and avoid "
                "unnecessary spending."
            )

        else:

            suggestions.append(
                "Your current spending is under control. "
                "Keep maintaining this habit."
            )

        suggestions.append(
            "Review your expenses regularly to identify "
            "where you can save money."
        )

    # ========================================================
    # TOTAL EXPENSE CARD
    # ========================================================

    expense_card = create_card(
        window,
        650,
        105
    )

    tk.Label(
        expense_card,
        text="TOTAL EXPENSE",
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(20, 3)
    )

    tk.Label(
        expense_card,
        text=f"₹ {total_expense:.2f}",
        font=("Arial", 20, "bold"),
        bg=CARD,
        fg=BLUE_LIGHT
    ).pack()

    # ========================================================
    # SUGGESTIONS CARD
    # ========================================================

    suggestion_card = create_card(
        window,
        650,
        340
    )

    tk.Label(
        suggestion_card,
        text="YOUR PERSONALIZED INSIGHTS",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=WHITE
    ).pack(
        pady=(20, 10)
    )

    suggestion_text = tk.Text(
        suggestion_card,
        width=65,
        height=14,
        font=("Arial", 11),
        wrap="word",
        bg="#081827",
        fg=LIGHT_TEXT,
        insertbackground=WHITE,
        relief="flat",
        bd=0,
        padx=15,
        pady=12
    )

    suggestion_text.pack(
        padx=18,
        pady=5,
        fill="both",
        expand=True
    )

    for suggestion in suggestions:

        suggestion_text.insert(
            tk.END,
            "◆  " + suggestion + "\n\n"
        )

    suggestion_text.config(
        state="disabled"
    )

    # ========================================================
    # REFRESH BUTTON
    # ========================================================

    def refresh_suggestions():

        window.destroy()

        show_ai_suggestions()

    premium_button(
        window,
        "REFRESH INSIGHTS",
        refresh_suggestions,
        220
    )
