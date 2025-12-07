# 📘 Smart Study Planner with Productivity Analytics

A simple and effective **Tkinter-based Study Planner** that helps
students manage tasks, track study hours, and visualize productivity
trends using charts.\
This project uses **JSON for data storage**, **Tkinter for GUI**, and
**Matplotlib for graphs**.

------------------------------------------------------------------------

## 🚀 Features

### ✅ Task Management

-   Add study tasks with estimated hours\
-   Mark tasks as completed\
-   Delete tasks\
-   Automatically saves and loads data from `study_data.json`

### 📊 Productivity & Analytics

-   Real-time statistics:
    -   Total tasks\
    -   Completed vs Pending\
    -   Total study hours\
    -   Completion rate\
-   Pie charts showing:
    -   Task completion distribution\
    -   Study hour distribution\
-   Line + Bar graphs showing:
    -   Daily task completion trend\
    -   Hours added per day

### 💾 Data Persistence

-   All tasks stored locally in **JSON**\
-   No database required\
-   Automatically loads saved data on startup

------------------------------------------------------------------------

## 🧰 Technologies Used

  Component                  Library
  -------------------------- ------------
  Graphical User Interface   Tkinter
  Data Visualization         Matplotlib
  Data Storage               JSON
  Date & Time Handling       datetime
  File Management            OS module

------------------------------------------------------------------------

## 📂 Project Structure

    📁 Smart Study Planner
    │
    ├── study_data.json          # Auto-generated data file  
    ├── main.py                  # Main Tkinter application  
    └── README.md                # Documentation  

------------------------------------------------------------------------

## ▶️ How to Run the Project

### **1️⃣ Install Python**

Make sure Python 3.8+ is installed.

### **2️⃣ Install Required Libraries**

Run this command:

``` bash
pip install matplotlib
```

### **3️⃣ Execute the Script**

Run the Python file:

``` bash
python main.py
```

------------------------------------------------------------------------

## 🖥️ How It Works

### ➕ Add Task

-   Enter task name\
-   Enter estimated hours\
-   Click **Add Task**\
-   Task appears in the task table

### ✔ Mark as Complete

-   Select a task\
-   Click **Mark as Completed**

### 🗑 Delete Task

-   Select a task\
-   Click **Delete Task**

### 📈 View Charts

-   *Task Chart* → Shows completion & hours distribution\
-   *Productivity Trend* → Shows performance by date

------------------------------------------------------------------------

## 📊 Visualization Samples

### **Task Completion Pie Chart**

-   Completed vs Pending tasks\
-   Shows hours distribution

### **Productivity Trend Chart**

-   Line graph → Tasks completed per day\
-   Bar graph → Hours added per day

------------------------------------------------------------------------

## 🛠 Future Enhancements

-   Add due dates & reminders\
-   Export reports as PDF\
-   Dark mode UI\
-   Add subject/category filters\
-   Weekly & monthly analytics dashboard

------------------------------------------------------------------------

## 👨‍💻 Author

**Smart Study Planner with Productivity Analytics**\
Made using Python, Tkinter & Matplotlib.
