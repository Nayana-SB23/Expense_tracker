import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

DB = "expense_tracker.db"



def initialize_database():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            category TEXT,
            budget_amount REAL,
            UNIQUE(month, category)
        )
    """)

    conn.commit()
    conn.close()



def add_expense_entry():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount")
        return

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()

    
    year_month = date[:7]
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE category=? AND substr(date,1,7)=?", 
                   (category, year_month))
    total_spent = cursor.fetchone()[0] or 0

    cursor.execute("SELECT budget_amount FROM budgets WHERE category=? AND month=?", 
                   (category, year_month))
    row = cursor.fetchone()
    conn.close()

    if row:
        budget = row[0]
        if total_spent > budget:
            messagebox.showwarning("Budget Alert", f"Budget exceeded for {category}.\nSpent: {total_spent}, Budget: {budget}")
        else:
            remaining = budget - total_spent
            messagebox.showinfo("Expense Added", f"Expense added successfully!\nRemaining budget: {remaining}")
    else:
        messagebox.showinfo("Expense Added", "Expense added successfully, but no budget set for this category.")


def set_budget_entry():
    month = budget_month_entry.get()
    category = budget_category_entry.get()
    budget_amount = budget_amount_entry.get()

    if not month:
        month = datetime.today().strftime("%Y-%m")

    try:
        float(budget_amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid budget amount")
        return

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO budgets (month, category, budget_amount)
        VALUES (?, ?, ?)
        ON CONFLICT(month, category)
        DO UPDATE SET budget_amount=excluded.budget_amount
    """, (month, category, budget_amount))

    conn.commit()
    conn.close()

    messagebox.showinfo("Budget Set", "Budget successfully saved!")


def view_total_spending():
    month = report_month_entry.get()

    if not month:
        month = datetime.today().strftime("%Y-%m")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE substr(date,1,7)=?", (month,))
    total_spent = cursor.fetchone()[0] or 0
    conn.close()

    messagebox.showinfo("Total Spending", f"Total spending for {month}: ₹{total_spent}")


def view_spending_comparison():
    month = report_month_entry.get()

    if not month:
        month = datetime.today().strftime("%Y-%m")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE substr(date,1,7)=?
        GROUP BY category
    """, (month,))
    expenses_data = cursor.fetchall()

    result = "Category     Spent    Budget    Difference\n\n"

    for category, spent in expenses_data:
        cursor.execute("SELECT budget_amount FROM budgets WHERE category=? AND month=?", 
                       (category, month))
        budget_row = cursor.fetchone()
        budget = budget_row[0] if budget_row else None

        if budget:
            difference = budget - spent
            result += f"{category:<12} {spent:<8} {budget:<8} {difference:<8}\n"
        else:
            result += f"{category:<12} {spent:<8} No Budget Set\n"

    conn.close()

    messagebox.showinfo("Spending vs Budget", result)



initialize_database()

app = tk.Tk()
app.title("Expense Tracker")
app.geometry("600x600")
app.resizable(False, False)
app.configure(bg="#f0f0f0")



tab_control = ttk.Notebook(app)
tab_control.pack(padx=10, pady=10, fill="both", expand=True)


tab_expense = tk.Frame(tab_control, bg="#f0f0f0")
tab_control.add(tab_expense, text="Add Expense")

expense_frame = tk.Frame(tab_expense, bg="#f0f0f0")
expense_frame.pack(padx=10, pady=10)

tk.Label(expense_frame, text="Date (YYYY-MM-DD):", bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
date_entry = tk.Entry(expense_frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(expense_frame, text="Category:", bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
category_entry = tk.Entry(expense_frame)
category_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(expense_frame, text="Amount:", bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
amount_entry = tk.Entry(expense_frame)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(expense_frame, text="Description:", bg="#f0f0f0").grid(row=3, column=0, sticky="e", padx=5, pady=5)
description_entry = tk.Entry(expense_frame)
description_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(expense_frame, text="Add Expense", command=add_expense_entry, bg="#4CAF50", fg="white").grid(row=4, columnspan=2, pady=10)


tab_budget = tk.Frame(tab_control, bg="#f0f0f0")
tab_control.add(tab_budget, text="Set Budget")

budget_frame = tk.Frame(tab_budget, bg="#f0f0f0")
budget_frame.pack(padx=10, pady=10)

tk.Label(budget_frame, text="Month (YYYY-MM):", bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
budget_month_entry = tk.Entry(budget_frame)
budget_month_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(budget_frame, text="Category:", bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
budget_category_entry = tk.Entry(budget_frame)
budget_category_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(budget_frame, text="Budget Amount:", bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
budget_amount_entry = tk.Entry(budget_frame)
budget_amount_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(budget_frame, text="Save Budget", command=set_budget_entry, bg="#4CAF50", fg="white").grid(row=3, columnspan=2, pady=10)


tab_report = tk.Frame(tab_control, bg="#f0f0f0")
tab_control.add(tab_report, text="Reports")

report_frame = tk.Frame(tab_report, bg="#f0f0f0")
report_frame.pack(padx=10, pady=10)

tk.Label(report_frame, text="Month (YYYY-MM):", bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
report_month_entry = tk.Entry(report_frame)
report_month_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(report_frame, text="Total Spending", command=view_total_spending, bg="#4CAF50", fg="white").grid(row=1, columnspan=2, pady=5)
tk.Button(report_frame, text="Spending vs Budget", command=view_spending_comparison, bg="#4CAF50", fg="white").grid(row=2, columnspan=2, pady=5)

app.mainloop()