import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


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

ENTRY_BG = "#10283D"
BORDER = "#1E4E73"

SHADOW = "#020810"


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
    "Other"
]


# ============================================================
# PREMIUM BUTTON
# ============================================================

def premium_button(parent, text, command, width=190):

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

    # Top shine
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

    # Top blue highlight
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
# BUDGET & SPENDING LIMIT
# ============================================================

def show_budget():

    window = tk.Toplevel()

    window.title(
        "Budget & Spending Limit"
    )

    window.geometry(
        "760x700"
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
        text="BUDGET & SPENDING LIMIT",
        font=("Arial", 23, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        window,
        text="Set spending limits and monitor your expenses",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 15)
    )

    # ========================================================
    # INPUT CARD
    # ========================================================

    form_card = create_card(
        window,
        650,
        155
    )

    # Category
    tk.Label(
        form_card,
        text="CATEGORY",
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).place(
        x=35,
        y=28
    )

    category_combo = ttk.Combobox(
        form_card,
        values=CATEGORIES,
        state="readonly",
        font=("Arial", 10)
    )

    category_combo.place(
        x=35,
        y=55,
        width=230,
        height=32
    )

    category_combo.set(
        "Food"
    )

    # Budget amount
    tk.Label(
        form_card,
        text="BUDGET AMOUNT",
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).place(
        x=295,
        y=28
    )

    amount_entry = tk.Entry(
        form_card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 11)
    )

    amount_entry.place(
        x=295,
        y=55,
        width=230,
        height=32
    )

    # ========================================================
    # SAVE
    # ========================================================

    def save_budget():

        category = category_combo.get()

        amount = amount_entry.get().strip()

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

        conn = sqlite3.connect(
            "expenses.db"
        )

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
        """, (
            category,
            amount
        ))

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            f"Budget for {category} saved successfully!"
        )

        amount_entry.delete(
            0,
            tk.END
        )

        load_budgets()

    premium_button(
        form_card,
        "SAVE BUDGET",
        save_budget,
        190
    ).place(
        x=450,
        y=92
    )

    # ========================================================
    # CURRENT BUDGETS
    # ========================================================

    tk.Label(
        window,
        text="CURRENT BUDGETS",
        font=("Arial", 15, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(12, 5)
    )

    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = create_card(
        window,
        700,
        330
    )

    columns = (
        "Category",
        "Budget",
        "Spent",
        "Remaining",
        "Status"
    )

    tree = ttk.Treeview(
        table_card,
        columns=columns,
        show="headings",
        height=11
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

    tree.column(
        "Category",
        width=130,
        anchor="center"
    )

    tree.column(
        "Budget",
        width=120,
        anchor="center"
    )

    tree.column(
        "Spent",
        width=120,
        anchor="center"
    )

    tree.column(
        "Remaining",
        width=130,
        anchor="center"
    )

    tree.column(
        "Status",
        width=150,
        anchor="center"
    )

    tree.place(
        x=15,
        y=15,
        width=660,
        height=280
    )

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )

    scrollbar.place(
        x=675,
        y=15,
        height=280
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    # ========================================================
    # LOAD BUDGETS
    # ========================================================

    def load_budgets():

        for item in tree.get_children():

            tree.delete(
                item
            )

        conn = sqlite3.connect(
            "expenses.db"
        )

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
            """, (
                category,
            ))

            spent = cursor.fetchone()[0]

            remaining = (
                budget -
                spent
            )

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

        conn.close()

    load_budgets()
