import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from datetime import datetime
import os

# Create the main window
root = tk.Tk()
root.title("Daily Income Tracker")

# Initialize data list and CSV file name
data = []
csv_file = "income_data.csv"

# Load existing data from the CSV file if it exists
if os.path.exists(csv_file):
    data = pd.read_csv(csv_file).to_dict('records')

# Function to load data into the Listbox
def load_data():
    for entry in data:
        listbox.insert(tk.END, f"Date: {entry['Date']}, Income: {entry['Income']}")

# Define a function to add daily income
def add_income(date_entry, income_entry):
    date = date_entry.get()
    income = income_entry.get()
    
    if not date or not income:
        messagebox.showwarning("Input Error", "Please enter both date and income.")
        return
    
    try:
        # Convert income to float
        income = float(income)
        # Append data to list
        new_entry = {"Date": date, "Income": income}
        data.append(new_entry)
        
        # Append data to the CSV file
        df = pd.DataFrame([new_entry])
        df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
        
        # Add entry to the Listbox
        listbox.insert(tk.END, f"Date: {date}, Income: {income}")
        messagebox.showinfo("Success", "Income added successfully.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid income amount.")
    
    # Clear the entry fields
    date_entry.delete(0, tk.END)
    income_entry.delete(0, tk.END)

# Define a function to generate monthly report
def generate_report():
    if not data:
        messagebox.showwarning("Data Error", "No data to generate report.")
        return
    
    # Convert data list to DataFrame
    df = pd.DataFrame(data)
    
    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set 'Date' as the index
    df.set_index('Date', inplace=True)
    
    # Resample the data by month and sum the incomes
    monthly_report = df.resample('M').sum()
    
    # Reset the index to have the 'Date' column back
    monthly_report.reset_index(inplace=True)
    
    # Rename the columns for better readability
    monthly_report.columns = ['Month', 'Total Income']
    
    # Generate the file name based on the current date
    file_name = f"Monthly_Report_{datetime.now().strftime('%Y_%m_%d')}.xlsx"
    
    # Save the report to an Excel file
    monthly_report.to_excel(file_name, index=False)
    
    messagebox.showinfo("Success", f"Monthly report generated: {file_name}")

# Create a Notebook widget for tabs
notebook = ttk.Notebook(root)
notebook.pack()

# Create frames for each tab
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add tabs to the Notebook
notebook.add(tab1, text='Income Tab 1')
notebook.add(tab2, text='Income Tab 2')

# Create the GUI elements for Tab 1
date_label1 = tk.Label(tab1, text="Date (YYYY-MM-DD):")
date_label1.pack()
date_entry1 = tk.Entry(tab1)
date_entry1.pack()

income_label1 = tk.Label(tab1, text="Income:")
income_label1.pack()
income_entry1 = tk.Entry(tab1)
income_entry1.pack()

add_button1 = tk.Button(tab1, text="Add Income", command=lambda: add_income(date_entry1, income_entry1))
add_button1.pack()

# Create the GUI elements for Tab 2
date_label2 = tk.Label(tab2, text="Date (YYYY-MM-DD):")
date_label2.pack()
date_entry2 = tk.Entry(tab2)
date_entry2.pack()

income_label2 = tk.Label(tab2, text="Income:")
income_label2.pack()
income_entry2 = tk.Entry(tab2)
income_entry2.pack()

add_button2 = tk.Button(tab2, text="Add Income", command=lambda: add_income(date_entry2, income_entry2))
add_button2.pack()

# Add a Listbox to display the daily incomes
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack()

report_button = tk.Button(root, text="Generate Monthly Report", command=generate_report)
report_button.pack()

# Load data into the Listbox
load_data()

# Run the main loop
root.mainloop()
