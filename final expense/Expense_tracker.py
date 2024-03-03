import json
import os
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import defaultdict

# File path for storing data
DATA_FILE = "expense_data.json"

# Default values for name, phone number, records, and monthly target
name = "------"
phone = "------"
records = []
monthly_target = 0
notes = ""  # Store notes separately

def load_data():
    global name, phone, records, monthly_target, notes
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            name = data.get("name", "------")
            phone = data.get("phone", "------")
            records = data.get("records", [])
            monthly_target = data.get("monthly_target", 0)
            notes = data.get("notes", "")

def save_data():
    data = {
        "name": name,
        "phone": phone,
        "records": records,
        "monthly_target": monthly_target,
        "notes": notes
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def on_close():
    save_data()
    root.destroy()

def reset_data():
    global name, phone, records, monthly_target, notes
    name = "------"
    phone = "------"
    records = []
    monthly_target = 0
    notes = ""
    clear_frames()
    save_data()
    messagebox.showinfo("Success", "All data has been reset.")
    # Refresh all frames
    Record()
    Analysis()
    Add_new()
    Reports()
    Account()

def Record():
    clear_frames()
    record_frame = Frame(root, bg="#f0f0f0")
    record_frame.pack(fill="both", expand=True)
    update_record_list(record_frame)

def update_record_list(frame):
    listbox_records = Listbox(frame, width=50, bg="#f0f0f0", fg="#333333", font=("Arial", 12))
    listbox_records.pack(fill="both", expand=True)
    listbox_records.delete(0, END)
    for record in reversed(records):
        listbox_records.insert(END, record)

def Analysis():
    clear_frames()
    analysis_frame = Frame(root, bg="#f0f0f0")
    analysis_frame.pack(fill="both", expand=True)
    if not records:
        messagebox.showwarning("Warning", "No records available for analysis.")
        return

    amounts = [float(record.split(": $")[1]) for record in records]
    total_expense = sum(amounts)
    mean_amount = total_expense / len(amounts)

    total_label_text = f"Total Expense: ${total_expense:.2f}"
    total_label = Label(analysis_frame, text=total_label_text, bg="#f0f0f0", fg="#333333", font=("Arial", 12))
    total_label.pack()
    
    if monthly_target:
        remaining_budget = monthly_target - total_expense
        remaining_budget_text = f"Remaining Budget: ${remaining_budget:.2f}"
    else:
        remaining_budget_text = "Remaining Budget: NAN"
    remaining_budget_label = Label(analysis_frame, text=remaining_budget_text, bg="#f0f0f0", fg="#333333", font=("Arial", 12))
    remaining_budget_label.pack()

    Label(analysis_frame, text=f"Mean: {mean_amount:.2f}", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    perform_analysis(analysis_frame)

def perform_analysis(frame):
    if not records:
        messagebox.showwarning("Warning", "No records available for analysis.")
        return

    category_expenses = defaultdict(float)
    for record in records:
        parts = record.split(": $")
        category = parts[0]
        amount = float(parts[1])
        category_expenses[category] += amount

    categories = list(category_expenses.keys())
    amounts = list(category_expenses.values())

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')
    plt.show()

def Add_new():
    clear_frames()
    add_new_frame = Frame(root, bg="#f0f0f0")
    add_new_frame.pack(fill="both", expand=True)
    Label(add_new_frame, text="Add New Expense", bg="#f0f0f0", fg="#333333", font=("Arial", 16, "bold")).pack()
    Label(add_new_frame, text="Amount:", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    entry_amount = Entry(add_new_frame)
    entry_amount.pack()
    Label(add_new_frame, text="Category:", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    entry_category = Entry(add_new_frame)
    entry_category.pack()
    Button(add_new_frame, text="Add Expense", command=lambda: add_expense(entry_amount.get(), entry_category.get()), bg="#333333", fg="#ffffff", font=("Arial", 12, "bold")).pack()

def add_expense(amount, category):
    if not amount or not category:
        messagebox.showwarning("Warning", "Please enter both amount and category.")
        return
    records.append(f"{category}: ${amount}")
    messagebox.showinfo("Success", "Expense added successfully!")
    Record()

def Reports():
    clear_frames()
    reports_frame = Frame(root, bg="#f0f0f0")
    reports_frame.pack(fill="both", expand=True)
    Label(reports_frame, text="Reports Page", bg="#f0f0f0", fg="#333333", font=("Arial", 16, "bold")).pack()
    Label(reports_frame, text="Monthly Target:", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    entry_target = Entry(reports_frame)
    entry_target.pack()

    # If monthly target is set, display it in the entry widget
    if monthly_target != 0:
        entry_target.insert(END, str(monthly_target))

    Button(reports_frame, text="Set Target", command=lambda: set_target(entry_target.get()), bg="#333333", fg="#ffffff", font=("Arial", 12, "bold")).pack()
    Label(reports_frame, text="Main Expenses Notes:", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    entry_notes = Text(reports_frame, height=5)
    entry_notes.pack()

    # If notes are available, display them in the text widget
    if notes:
        entry_notes.insert(END, notes)

    Button(reports_frame, text="Save Notes", command=lambda: save_notes(entry_notes.get("1.0", "end-1c")), bg="#333333", fg="#ffffff", font=("Arial", 12, "bold")).pack()

def set_target(target):
    global monthly_target
    if not target:
        messagebox.showwarning("Warning", "Please enter a valid target.")
        return
    monthly_target = float(target)
    messagebox.showinfo("Success", f"Monthly target set to ${monthly_target}")

def save_notes(notes_text):
    global notes
    notes = notes_text
    messagebox.showinfo("Success", "Notes saved successfully!")

def Account():
    clear_frames()
    account_frame = Frame(root, bg="#f0f0f0")
    account_frame.pack(fill="both", expand=True)
    Label(account_frame, text="Account Page", bg="#f0f0f0", fg="#333333", font=("Arial", 16, "bold")).pack()
    Label(account_frame, text="Name:", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    entry_name = Entry(account_frame)
    entry_name.insert(END, name)
    entry_name.pack()
    Label(account_frame, text="Phone:", bg="#f0f0f0", fg="#333333", font=("Arial", 12)).pack()
    entry_phone = Entry(account_frame)
    entry_phone.insert(END, phone)
    entry_phone.pack()
    Button(account_frame, text="Save", command=lambda: save_account_info(entry_name.get(), entry_phone.get()), bg="#333333", fg="#ffffff", font=("Arial", 12, "bold")).pack()

def save_account_info(new_name, new_phone):
    global name, phone
    name = new_name
    phone = new_phone
    messagebox.showinfo("Success", "Account information saved successfully!")

def clear_frames():
    for widget in root.winfo_children():
        if isinstance(widget, Frame):
            widget.destroy()

root = Tk()
root.geometry("350x600+50+50")
root.config(bg="#f0f0f0")
root.title("Expense Tracker")

# Load data from file
load_data()

menu_Bar = Menu(root, borderwidth=10, bg="#333333", fg="#ffffff", font=("Arial", 12, "bold"))
menu_Bar.add_command(label="Record", command=Record)
menu_Bar.add_command(label="Analysis", command=Analysis)
menu_Bar.add_command(label="Add_new", command=Add_new)
menu_Bar.add_command(label="Reports", command=Reports)
menu_Bar.add_command(label="Account", command=Account)
menu_Bar.add_command(label="Reset Data", command=reset_data)
menu_Bar.add_command(label="Quit", command=on_close, foreground="red")

root.config(menu=menu_Bar)

# Open Add_new frame by default
Add_new()

# Bind close event to on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
