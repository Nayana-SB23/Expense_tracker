Expense-Tracker-Application

A simple desktop Expense Tracker built with Tkinter and SQLite. Opens as a GUI window when you run the script — log daily expenses, set monthly budgets per category, get budget alerts, and view reports.

Features

Add daily expenses: date, category, amount, description
Set monthly budgets per category (YYYY-MM)
Automatic alert when a category's monthly spending exceeds its budget
View total spending for a month and a Spending vs Budget comparison report
Desktop GUI that pops up on run (no terminal menus)
Small, single-file SQLite database created automatically

Tech stack

Python 3.8+ (no external packages required)
GUI: Tkinter (built into Python)
Database: SQLite (file-based DB inside project folder)

Getting started (Run in VSCode / locally)

Install Python. Ensure Python 3.8 or newer is installed. Verify with:
python --version

Clone this repository:
git clone <repository_link>
cd <project_folder>

Open in VSCode:
File → Open Folder... → select the repository folder.

Run the app by opening the VSCode terminal (View → Terminal) and running:
python expense_tracker.py

The GUI window will pop up. No other dependencies or setup required.

How to use

Fill in the Date, Category, Amount, and optional Description; click Add Expense to record a transaction.
To set a monthly budget: enter Month (YYYY-MM), Category, Budget Amount → Save Budget.
To check reports: enter Report Month (YYYY-MM) → click Total Spending or Spending vs Budget.
The application will automatically alert if spending for a category exceeds its assigned budget.

Database details

Database file: expense_tracker.db (created in the same folder when the app runs)
