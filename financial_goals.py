import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


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


def show_financial_goals():

    create_goals_table()

    window = tk.Toplevel()
    window.title("Financial Goals")
    window.geometry("750x600")
    window.resizable(False, False)

    tk.Label(
        window,
        text="🎯 Financial Goals",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    tk.Label(
        input_frame,
        text="Goal Name:"
    ).grid(row=0, column=0, padx=5, pady=5)

    goal_entry = tk.Entry(
        input_frame,
        width=25
    )
    goal_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(
        input_frame,
        text="Target Amount:"
    ).grid(row=1, column=0, padx=5, pady=5)

    target_entry = tk.Entry(
        input_frame,
        width=25
    )
    target_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(
        input_frame,
        text="Saved Amount:"
    ).grid(row=2, column=0, padx=5, pady=5)

    saved_entry = tk.Entry(
        input_frame,
        width=25
    )
    saved_entry.grid(row=2, column=1, padx=5, pady=5)

    columns = (
        "ID",
        "Goal",
        "Target",
        "Saved",
        "Remaining",
        "Progress"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=10
    )

    for column in columns:
        tree.heading(column, text=column)

    tree.column("ID", width=40)
    tree.column("Goal", width=180)
    tree.column("Target", width=100)
    tree.column("Saved", width=100)
    tree.column("Remaining", width=110)
    tree.column("Progress", width=100)

    tree.pack(
        padx=20,
        pady=15
    )

    def load_goals():

        for item in tree.get_children():
            tree.delete(item)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, goal_name, target_amount, saved_amount
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

            remaining = max(target - saved, 0)

            if target > 0:
                progress = min((saved / target) * 100, 100)
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

        conn = sqlite3.connect("expenses.db")
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

        goal_entry.delete(0, tk.END)
        target_entry.delete(0, tk.END)
        saved_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Financial goal added successfully!"
        )

        load_goals()

    def update_goal():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a goal."
            )
            return

        item = tree.item(selected[0])
        goal_id = item["values"][0]

        update_window = tk.Toplevel()
        update_window.title("Update Financial Goal")
        update_window.geometry("400x350")
        update_window.resizable(False, False)

        tk.Label(
            update_window,
            text="Update Goal",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            update_window,
            text="Goal Name"
        ).pack()

        name_entry = tk.Entry(
            update_window,
            width=30
        )
        name_entry.pack(pady=5)

        name_entry.insert(
            0,
            item["values"][1]
        )

        tk.Label(
            update_window,
            text="Target Amount"
        ).pack()

        target_entry2 = tk.Entry(
            update_window,
            width=30
        )
        target_entry2.pack(pady=5)

        target_value = str(
            item["values"][2]
        ).replace("₹", "")

        target_entry2.insert(
            0,
            target_value
        )

        tk.Label(
            update_window,
            text="Saved Amount"
        ).pack()

        saved_entry2 = tk.Entry(
            update_window,
            width=30
        )
        saved_entry2.pack(pady=5)

        saved_value = str(
            item["values"][3]
        ).replace("₹", "")

        saved_entry2.insert(
            0,
            saved_value
        )

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

            conn = sqlite3.connect("expenses.db")
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

        tk.Button(
            update_window,
            text="Save Update",
            width=15,
            height=2,
            command=save_update
        ).pack(pady=20)

    def delete_goal():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a goal."
            )
            return

        item = tree.item(selected[0])
        goal_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this goal?"
        )

        if not confirm:
            return

        conn = sqlite3.connect("expenses.db")
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

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Goal",
        width=15,
        command=add_goal
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update Goal",
        width=15,
        command=update_goal
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete Goal",
        width=15,
        command=delete_goal
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    load_goals()