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
# CREATE TABLE
# ============================================================

def create_goals_table():

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            saved_amount REAL NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# PREMIUM BUTTON
# ============================================================

def premium_button(parent, text, command, width=180):

    height = 48
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
# FINANCIAL GOALS
# ============================================================

def show_financial_goals():

    create_goals_table()

    window = tk.Toplevel()

    window.title(
        "Financial Goals"
    )

    window.geometry(
        "800x760"
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
        text="FINANCIAL GOALS",
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 3)
    )

    tk.Label(
        window,
        text="Set savings targets and track your progress",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 15)
    )

    # ========================================================
    # INPUT CARD
    # ========================================================

    input_card = create_card(
        window,
        700,
        185
    )

    # Goal name
    tk.Label(
        input_card,
        text="GOAL NAME",
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).place(
        x=30,
        y=25
    )

    goal_entry = tk.Entry(
        input_card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 10)
    )

    goal_entry.place(
        x=30,
        y=52,
        width=260,
        height=32
    )

    # Target amount
    tk.Label(
        input_card,
        text="TARGET AMOUNT",
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).place(
        x=325,
        y=25
    )

    target_entry = tk.Entry(
        input_card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 10)
    )

    target_entry.place(
        x=325,
        y=52,
        width=150,
        height=32
    )

    # Saved amount
    tk.Label(
        input_card,
        text="SAVED AMOUNT",
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=LIGHT_TEXT
    ).place(
        x=495,
        y=25
    )

    saved_entry = tk.Entry(
        input_card,
        bg=ENTRY_BG,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Arial", 10)
    )

    saved_entry.place(
        x=495,
        y=52,
        width=150,
        height=32
    )

    # ========================================================
    # TABLE
    # ========================================================

    table_card = create_card(
        window,
        750,
        345
    )

    columns = (
        "ID",
        "Goal",
        "Target",
        "Saved",
        "Remaining",
        "Progress"
    )

    tree = ttk.Treeview(
        table_card,
        columns=columns,
        show="headings",
        height=10
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

    tree.column(
        "ID",
        width=45,
        anchor="center"
    )

    tree.column(
        "Goal",
        width=190,
        anchor="center"
    )

    tree.column(
        "Target",
        width=110,
        anchor="center"
    )

    tree.column(
        "Saved",
        width=110,
        anchor="center"
    )

    tree.column(
        "Remaining",
        width=120,
        anchor="center"
    )

    tree.column(
        "Progress",
        width=110,
        anchor="center"
    )

    tree.place(
        x=15,
        y=15,
        width=710,
        height=275
    )

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )

    scrollbar.place(
        x=725,
        y=15,
        height=275
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    # ========================================================
    # LOAD GOALS
    # ========================================================

    def load_goals():

        for item in tree.get_children():

            tree.delete(
                item
            )

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id,
                   goal_name,
                   target_amount,
                   saved_amount
            FROM financial_goals
            ORDER BY id DESC
        """)

        goals = cursor.fetchall()

        conn.close()

        for goal in goals:

            goal_id = goal[0]
            goal_name = goal[1]
            target = goal[2]
            saved = goal[3]

            remaining = max(
                target - saved,
                0
            )

            if target > 0:

                progress = min(
                    (saved / target) * 100,
                    100
                )

            else:

                progress = 0

            tree.insert(
                "",
                "end",
                values=(
                    goal_id,
                    goal_name,
                    f"₹{target:.2f}",
                    f"₹{saved:.2f}",
                    f"₹{remaining:.2f}",
                    f"{progress:.1f}%"
                )
            )

    # ========================================================
    # ADD GOAL
    # ========================================================

    def add_goal():

        goal_name = goal_entry.get().strip()

        target = target_entry.get().strip()

        saved = saved_entry.get().strip()

        if not goal_name or not target:

            messagebox.showerror(
                "Error",
                "Goal Name and Target Amount are required."
            )

            return

        if not saved:

            saved = "0"

        try:

            target = float(target)

            saved = float(saved)

            if target <= 0:

                messagebox.showerror(
                    "Error",
                    "Target amount must be greater than 0."
                )

                return

            if saved < 0:

                messagebox.showerror(
                    "Error",
                    "Saved amount cannot be negative."
                )

                return

            if saved > target:

                messagebox.showerror(
                    "Error",
                    "Saved amount cannot be greater than target amount."
                )

                return

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter valid amounts."
            )

            return

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO financial_goals
            (goal_name, target_amount, saved_amount)
            VALUES (?, ?, ?)
        """, (
            goal_name,
            target,
            saved
        ))

        conn.commit()

        conn.close()

        goal_entry.delete(
            0,
            tk.END
        )

        target_entry.delete(
            0,
            tk.END
        )

        saved_entry.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Success",
            "Financial goal added successfully!"
        )

        load_goals()

    # ========================================================
    # UPDATE GOAL
    # ========================================================

    def update_goal():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a goal."
            )

            return

        item = tree.item(
            selected[0]
        )

        goal_id = item["values"][0]

        update_window = tk.Toplevel(
            window
        )

        update_window.title(
            "Update Financial Goal"
        )

        update_window.geometry(
            "480x450"
        )

        update_window.resizable(
            False,
            False
        )

        update_window.configure(
            bg=BG
        )

        tk.Label(
            update_window,
            text="UPDATE FINANCIAL GOAL",
            font=("Arial", 20, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            pady=(25, 15)
        )

        update_card = create_card(
            update_window,
            400,
            270
        )

        # Goal name
        tk.Label(
            update_card,
            text="GOAL NAME",
            font=("Arial", 9, "bold"),
            bg=CARD,
            fg=LIGHT_TEXT
        ).pack(
            pady=(25, 3)
        )

        name_entry = tk.Entry(
            update_card,
            bg=ENTRY_BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 10)
        )

        name_entry.pack(
            ipadx=70,
            ipady=5
        )

        name_entry.insert(
            0,
            item["values"][1]
        )

        # Target
        tk.Label(
            update_card,
            text="TARGET AMOUNT",
            font=("Arial", 9, "bold"),
            bg=CARD,
            fg=LIGHT_TEXT
        ).pack(
            pady=(10, 3)
        )

        target_entry2 = tk.Entry(
            update_card,
            bg=ENTRY_BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 10)
        )

        target_entry2.pack(
            ipadx=70,
            ipady=5
        )

        target_value = str(
            item["values"][2]
        ).replace(
            "₹",
            ""
        )

        target_entry2.insert(
            0,
            target_value
        )

        # Saved
        tk.Label(
            update_card,
            text="SAVED AMOUNT",
            font=("Arial", 9, "bold"),
            bg=CARD,
            fg=LIGHT_TEXT
        ).pack(
            pady=(10, 3)
        )

        saved_entry2 = tk.Entry(
            update_card,
            bg=ENTRY_BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 10)
        )

        saved_entry2.pack(
            ipadx=70,
            ipady=5
        )

        saved_value = str(
            item["values"][3]
        ).replace(
            "₹",
            ""
        )

        saved_entry2.insert(
            0,
            saved_value
        )

        # ====================================================
        # SAVE UPDATE
        # ====================================================

        def save_update():

            name = name_entry.get().strip()

            try:

                target = float(
                    target_entry2.get()
                )

                saved = float(
                    saved_entry2.get()
                )

                if not name:

                    messagebox.showerror(
                        "Error",
                        "Goal name is required."
                    )

                    return

                if target <= 0:

                    messagebox.showerror(
                        "Error",
                        "Target amount must be greater than 0."
                    )

                    return

                if saved < 0 or saved > target:

                    messagebox.showerror(
                        "Error",
                        "Saved amount must be between 0 and target amount."
                    )

                    return

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Please enter valid amounts."
                )

                return

            conn = sqlite3.connect(
                "expenses.db"
            )

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE financial_goals
                SET goal_name = ?,
                    target_amount = ?,
                    saved_amount = ?
                WHERE id = ?
            """, (
                name,
                target,
                saved,
                goal_id
            ))

            conn.commit()

            conn.close()

            update_window.destroy()

            load_goals()

            messagebox.showinfo(
                "Success",
                "Goal updated successfully!"
            )

        premium_button(
            update_card,
            "SAVE UPDATE",
            save_update,
            180
        )

    # ========================================================
    # DELETE GOAL
    # ========================================================

    def delete_goal():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a goal."
            )

            return

        item = tree.item(
            selected[0]
        )

        goal_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this goal?"
        )

        if not confirm:

            return

        conn = sqlite3.connect(
            "expenses.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM financial_goals WHERE id = ?",
            (goal_id,)
        )

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            "Goal deleted successfully!"
        )

        load_goals()

    # ========================================================
    # BUTTONS
    # ========================================================

    button_card = create_card(
        window,
        700,
        85
    )

    premium_button(
        button_card,
        "ADD GOAL",
        add_goal,
        170
    ).place(
        x=35,
        y=15
    )

    premium_button(
        button_card,
        "UPDATE GOAL",
        update_goal,
        170
    ).place(
        x=265,
        y=15
    )

    premium_button(
        button_card,
        "DELETE GOAL",
        delete_goal,
        170
    ).place(
        x=495,
        y=15
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    load_goals()
