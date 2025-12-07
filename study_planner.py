import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"tasks": []}
    return {"tasks": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_task(task_name, estimated_hours, data):
    task = {"id": len(data["tasks"]) + 1, "name": task_name, "estimated_hours": float(estimated_hours),
            "completed": False, "created_date": datetime.now().strftime("%Y-%m-%d"), "completed_date": None}
    data["tasks"].append(task)
    save_data(data)
    return data

def mark_task_complete(task_id, data):
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["completed"] = True
            task["completed_date"] = datetime.now().strftime("%Y-%m-%d")
            break
    save_data(data)
    return data

def delete_task(task_id, data):
    data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
    save_data(data)
    return data

def calculate_statistics(data):
    total_tasks = len(data["tasks"])
    completed_tasks = sum(1 for task in data["tasks"] if task["completed"])
    pending_tasks = total_tasks - completed_tasks
    total_estimated_hours = sum(task["estimated_hours"] for task in data["tasks"])
    completed_hours = sum(task["estimated_hours"] for task in data["tasks"] if task["completed"])
    pending_hours = total_estimated_hours - completed_hours
    return {"total_tasks": total_tasks, "completed_tasks": completed_tasks, "pending_tasks": pending_tasks,
            "total_hours": total_estimated_hours, "completed_hours": completed_hours, "pending_hours": pending_hours}

def get_productivity_by_date(data):
    date_data = {}
    for task in data["tasks"]:
        date = task["created_date"]
        if date not in date_data:
            date_data[date] = {"completed": 0, "total": 0, "hours": 0}
        date_data[date]["total"] += 1
        date_data[date]["hours"] += task["estimated_hours"]
        if task["completed"]:
            date_data[date]["completed"] += 1
    sorted_dates = sorted(date_data.keys())
    return sorted_dates, [date_data[date] for date in sorted_dates]

def refresh_task_list():
    for item in task_tree.get_children():
        task_tree.delete(item)
    data = load_data()
    for task in data["tasks"]:
        status = "✓ Completed" if task["completed"] else "○ Pending"
        task_tree.insert("", "end", values=(task["id"], task["name"], f"{task['estimated_hours']} hrs", status, task["created_date"]))

def refresh_statistics():
    data = load_data()
    stats = calculate_statistics(data)
    stats_text.config(state="normal")
    stats_text.delete(1.0, tk.END)
    completion_rate = (stats['completed_tasks']/stats['total_tasks']*100) if stats['total_tasks'] > 0 else 0
    stats_text.insert(1.0, f"""📊 STUDY STATISTICS

Total Tasks: {stats['total_tasks']}
Completed: {stats['completed_tasks']} ✓
Pending: {stats['pending_tasks']} ○

Total Estimated Time: {stats['total_hours']:.1f} hours
Completed Time: {stats['completed_hours']:.1f} hours
Pending Time: {stats['pending_hours']:.1f} hours

Completion Rate: {completion_rate:.1f}%
""")
    stats_text.config(state="disabled")

def on_add_task():
    task_name = task_name_entry.get().strip()
    estimated_hours = hours_entry.get().strip()
    if not task_name:
        messagebox.showerror("Error", "Please enter a task name!")
        return
    try:
        hours = float(estimated_hours)
        if hours <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of hours (greater than 0)!")
        return
    data = load_data()
    add_task(task_name, hours, data)
    task_name_entry.delete(0, tk.END)
    hours_entry.delete(0, tk.END)
    refresh_task_list()
    refresh_statistics()
    messagebox.showinfo("Success", "Task added successfully!")

def on_complete_task():
    selected = task_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a task to mark as complete!")
        return
    item = task_tree.item(selected[0])
    task_id = int(item['values'][0])
    data = load_data()
    mark_task_complete(task_id, data)
    refresh_task_list()
    refresh_statistics()
    messagebox.showinfo("Success", "Task marked as completed!")

def on_delete_task():
    selected = task_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a task to delete!")
        return
    if not messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
        return
    item = task_tree.item(selected[0])
    task_id = int(item['values'][0])
    data = load_data()
    delete_task(task_id, data)
    refresh_task_list()
    refresh_statistics()
    messagebox.showinfo("Success", "Task deleted successfully!")

def show_task_chart():
    data = load_data()
    stats = calculate_statistics(data)
    if stats["total_tasks"] == 0:
        messagebox.showinfo("Info", "No tasks to display. Please add some tasks first!")
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    labels = ['Completed', 'Pending']
    sizes = [stats["completed_tasks"], stats["pending_tasks"]]
    colors = ['#4CAF50', '#FF9800']
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Tasks: Completed vs Pending')
    hours_sizes = [stats["completed_hours"], stats["pending_hours"]]
    ax2.pie(hours_sizes, labels=['Completed Hours', 'Pending Hours'], colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Study Hours: Completed vs Pending')
    plt.tight_layout()
    plt.show()

def show_productivity_trend():
    data = load_data()
    if len(data["tasks"]) == 0:
        messagebox.showinfo("Info", "No tasks to display. Please add some tasks first!")
        return
    dates, date_data = get_productivity_by_date(data)
    if len(dates) == 0:
        messagebox.showinfo("Info", "No data to display!")
        return
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    completed_counts = [d["completed"] for d in date_data]
    total_counts = [d["total"] for d in date_data]
    ax1.plot(dates, completed_counts, marker='o', label='Completed Tasks', color='#4CAF50', linewidth=2)
    ax1.plot(dates, total_counts, marker='s', label='Total Tasks', color='#2196F3', linewidth=2)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Tasks')
    ax1.set_title('Task Completion Trend Over Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    hours_data = [d["hours"] for d in date_data]
    ax2.bar(dates, hours_data, color='#FF9800', alpha=0.7)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Estimated Hours')
    ax2.set_title('Study Hours Added Over Time')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()





























































































































































































































































































root = tk.Tk()
root.title("Smart Study Planner")
root.geometry("900x700")
root.configure(bg='#87CEEB')
title_label = tk.Label(root, text="📚 Smart Study Planner", font=("Arial", 20, "bold"), bg='#87CEEB')
title_label.pack(pady=10)
main_frame = tk.Frame(root, bg='#87CEEB')
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
left_panel = tk.Frame(main_frame, bg='#E3F2FD', relief=tk.RAISED, bd=2)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
add_task_frame = tk.LabelFrame(left_panel, text="Add New Task", font=("Arial", 12, "bold"), bg='#FFF9C4', padx=10, pady=10)
add_task_frame.pack(fill=tk.X, padx=10, pady=10)
tk.Label(add_task_frame, text="Task Name:", bg='#FFF9C4', fg='#1976D2', font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
task_name_entry = tk.Entry(add_task_frame, width=30, font=("Arial", 10), bg='#FFFFFF')
task_name_entry.grid(row=0, column=1, pady=5, padx=5)
tk.Label(add_task_frame, text="Estimated Hours:", bg='#FFF9C4', fg='#1976D2', font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
hours_entry = tk.Entry(add_task_frame, width=30, font=("Arial", 10), bg='#FFFFFF')
hours_entry.grid(row=1, column=1, pady=5, padx=5)
add_button = tk.Button(add_task_frame, text="Add Task", command=on_add_task, bg='#4CAF50', fg='white', font=("Arial", 10, "bold"), padx=20)
add_button.grid(row=2, column=0, columnspan=2, pady=10)
list_frame = tk.LabelFrame(left_panel, text="Task List", font=("Arial", 12, "bold"), bg='#F3E5F5', padx=10, pady=10)
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
columns = ("ID", "Task Name", "Hours", "Status", "Date")
task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
for col in columns:
    task_tree.heading(col, text=col)
    task_tree.column(col, width=120)
task_tree.pack(fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=task_tree.yview)
task_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
button_frame = tk.Frame(list_frame, bg='#F3E5F5')
button_frame.pack(pady=5)
complete_button = tk.Button(button_frame, text="Mark Complete", command=on_complete_task, bg='#2196F3', fg='white', font=("Arial", 10, "bold"), width=15)
complete_button.pack(side=tk.LEFT, padx=5)
delete_button = tk.Button(button_frame, text="Delete Task", command=on_delete_task, bg='#f44336', fg='white', font=("Arial", 10, "bold"), width=15)
delete_button.pack(side=tk.LEFT, padx=5)
right_panel = tk.Frame(main_frame, bg='#E8F5E9', relief=tk.RAISED, bd=2)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
stats_frame = tk.LabelFrame(right_panel, text="Statistics", font=("Arial", 12, "bold"), bg='#FFE0B2', padx=10, pady=10)
stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
stats_text = tk.Text(stats_frame, height=15, width=30, font=("Arial", 10), state="disabled", bg='#FFFDE7', fg='#1A237E')
stats_text.pack(fill=tk.BOTH, expand=True)
charts_frame = tk.LabelFrame(right_panel, text="Visualizations", font=("Arial", 12, "bold"), bg='#E1BEE7', padx=10, pady=10)
charts_frame.pack(fill=tk.X, padx=10, pady=10)
chart1_button = tk.Button(charts_frame, text="Show Task Chart", command=show_task_chart, bg='#FF9800', fg='white', font=("Arial", 10, "bold"), width=20)
chart1_button.pack(pady=5)
chart2_button = tk.Button(charts_frame, text="Show Productivity Trend", command=show_productivity_trend, bg='#9C27B0', fg='white', font=("Arial", 10, "bold"), width=20)
chart2_button.pack(pady=5)
refresh_task_list()
refresh_statistics()
root.mainloop()
