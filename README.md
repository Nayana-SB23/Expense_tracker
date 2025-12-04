## **Features**

1. **Add daily expenses**: date, category, amount, description
2. **Set monthly budgets per category** (YYYY-MM)
3. **Automatic alert** when a category's monthly spending exceeds its budget
4. **View total spending** for a month and a **Spending vs Budget** comparison report
5. Desktop **GUI** that pops up on run (no terminal menus)
6. Small, **single-file SQLite database** created automatically

## **Tech Stack**

- **Python 3.8+** (no external packages required)
- **GUI**: Tkinter (built into Python)
- **Database**: SQLite (file-based DB inside project folder)

## **Getting Started (Run in VSCode / Locally)**

1. **Install Python**: Ensure Python 3.8 or newer is installed. Verify with:
   bash
   python --version
`

2. **Clone this repository**:

   bash
   git clone <repository_link>
   cd <project_folder>
   

3. **Open in VSCode**:

   * File → Open Folder → select the repository folder.

4. **Run the app** by opening the **VSCode terminal** and running:

   bash
   python expense_tracker.py
   

   * The **GUI window** will pop up. No other dependencies or setup required.

## **How to Use**

1. **Fill in the Date, Category, Amount**, and optional **Description**; click **Add Expense** to record a transaction.
2. To **set a monthly budget**: enter **Month (YYYY-MM)**, **Category**, **Budget Amount** → **Save Budget**.
3. To check **reports**: enter **Report Month (YYYY-MM)** → click **Total Spending** or **Spending vs Budget**.
4. The application will **automatically alert** if spending for a category exceeds its assigned budget.

## **Database Details**

* **Database file**: `expense_tracker.db`
