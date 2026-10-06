import csv
import pandas as pd
import requests
from datetime import datetime
import os

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

tasks = []

class Task:

    def __init__(self, title, priority, due_date, category, status="Pending"):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.status = status

def load_tasks():

    try:

        with open("tasks.csv", "r") as file:

            reader = csv.reader(file)

            for row in reader:

                if row:

                    task = Task(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4]
                    )

                    tasks.append(task)

    except FileNotFoundError:

        open("tasks.csv", "w").close()

def save_tasks():

    with open("tasks.csv", "w", newline="") as file:

        writer = csv.writer(file)

        for task in tasks:

            writer.writerow([
                task.title,
                task.priority,
                task.due_date,
                task.category,
                task.status
            ])

def add_task():

    title = input("Enter task title: ")
    priority = input("Enter priority (High/Medium/Low): ")
    due_date = input("Enter due date (DD-MM-YYYY): ")
    category = input("Enter category: ")

    task = Task(title, priority, due_date, category)

    tasks.append(task)

    save_tasks()

    print("Task Added Successfully")

def update_task():

    view_tasks()

    if len(tasks) == 0:
        return

    try:

        task_num = int(input("Enter task number to update: "))

        if 1 <= task_num <= len(tasks):

            print("\nWhat do you want to update?")
            print("1. Title")
            print("2. Priority")
            print("3. Due Date")
            print("4. Category")
            print("5. Status")

            update_choice = input("Enter your choice: ")

            if update_choice == "1":

                new_title = input("Enter new title: ")

                tasks[task_num - 1].title = new_title

            elif update_choice == "2":

                new_priority = input(
                    "Enter new priority: "
                )

                tasks[task_num - 1].priority = new_priority

            elif update_choice == "3":

                new_due_date = input(
                    "Enter new due date: "
                )

                tasks[task_num - 1].due_date = new_due_date

            elif update_choice == "4":

                new_category = input(
                    "Enter new category: "
                )

                tasks[task_num - 1].category = new_category

            elif update_choice == "5":

                new_status = input(
                    "Enter new status: "
                )

                tasks[task_num - 1].status = new_status

            else:

                print("Invalid Choice")
                return

            save_tasks()

            print("Task Updated Successfully")

        else:

            print("Invalid Task Number")

    except ValueError:

        print("Enter Numbers Only")
        
def view_tasks():

    if len(tasks) == 0:

        print("No Tasks Available")

    else:

        print("\n--- TASK LIST ---")

        print(
            f"{'No':<5}"
            f"{'Title':<35}"
            f"{'Priority':<15}"
            f"{'Due Date':<15}"
            f"{'Category':<15}"
            f"{'Status':<15}"
        )

        print("-" * 85)

        for i in range(len(tasks)):

            print(
                f"{i + 1:<5}"
                f"{tasks[i].title:<35}"
                f"{tasks[i].priority:<15}"
                f"{tasks[i].due_date:<15}"
                f"{tasks[i].category:<15}"
                f"{tasks[i].status:<15}"
            )

def complete_task():

    view_tasks()

    if len(tasks) == 0:
        return

    try:

        task_num = int(input("Enter task number to complete: "))

        if 1 <= task_num <= len(tasks):

            tasks[task_num - 1].status = "Completed"

            save_tasks()

            print("Task Completed Successfully")

        else:

            print("Invalid Task Number")

    except ValueError:

        print("Enter Numbers Only")

def delete_task():

    view_tasks()

    if len(tasks) == 0:
        return

    try:

        task_num = int(input("Enter task number to delete: "))

        if 1 <= task_num <= len(tasks):

            removed = tasks.pop(task_num - 1)

            save_tasks()

            print(f"{removed.title} Deleted Successfully")

        else:

            print("Invalid Task Number")

    except ValueError:

        print("Enter Numbers Only")

def search_task():

    keyword = input("Enter task name to search: ").lower()

    found = False

    for task in tasks:

        if keyword in task.title.lower():

            print(
                f"{task.title} | "
                f"{task.priority} | "
                f"{task.due_date} | "
                f"{task.category} | "
                f"{task.status}"
            )

            found = True

    if not found:

        print("No Matching Task Found")

def check_overdue_tasks():

    today = datetime.today()

    print("\n--- OVERDUE TASKS ---")

    found = False

    for task in tasks:

        try:

            due = datetime.strptime(
                task.due_date,
                "%d-%m-%Y"
            )

            if due < today and task.status == "Pending":

                print(f"{task.title} is OVERDUE")

                found = True

        except ValueError:

            print(
                f"Invalid date format for task: {task.title}"
            )

    if not found:

        print("No Overdue Tasks")

def generate_report():

    if len(tasks) == 0:

        print("No Tasks Available")
        return

    data = []

    for task in tasks:

        data.append({
            "Task": task.title,
            "Priority": task.priority,
            "Due Date": task.due_date,
            "Category": task.category,
            "Status": task.status
        })

    df = pd.DataFrame(data)

    total_tasks = len(df)

    completed_tasks = len(df[df["Status"] == "Completed"])

    pending_tasks = len(df[df["Status"] == "Pending"])

    high_priority = len(df[df["Priority"] == "High"])

    productivity_score = (
        completed_tasks / total_tasks
    ) * 100

    print("\n--- PRODUCTIVITY REPORT ---")

    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Pending Tasks: {pending_tasks}")
    print(f"High Priority Tasks: {high_priority}")
    print(f"Productivity Score: {productivity_score:.2f}%")

def call_ai(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=data
        )

        result = response.json()

        if "choices" in result:

            return result["choices"][0]["message"]["content"]

        else:

            print("\nAI Error")
            print(result)

            return None

    except Exception as error:

        print("\nRequest Failed")
        print(error)

        return None

def ai_productivity_advice():

    pending_tasks = []

    for task in tasks:

        if task.status == "Pending":

            pending_tasks.append(task.title)

    if len(pending_tasks) == 0:

        print("No Pending Tasks")
        return

    prompt = f"""
    These are my pending tasks:
    {pending_tasks}

    Give short productivity advice.
    """

    advice = call_ai(prompt)

    if advice:

        print("\n--- AI PRODUCTIVITY ADVICE ---")
        print(advice)

def ai_task_prioritization():

    task_titles = []

    for task in tasks:

        task_titles.append(task.title)

    prompt = f"""
    These are my tasks:
    {task_titles}

    Arrange them from highest priority to lowest priority.
    """

    priorities = call_ai(prompt)

    if priorities:

        print("\n--- AI TASK PRIORITIZATION ---")
        print(priorities)

def ai_daily_planner():

    available_hours = input("Enter available hours today: ")

    pending_tasks = []

    for task in tasks:

        if task.status == "Pending":

            pending_tasks.append(task.title)

    prompt = f"""
    I have {available_hours} hours available today.

    These are my pending tasks:
    {pending_tasks}

    Create a smart daily plan.
    """

    plan = call_ai(prompt)

    if plan:

        print("\n--- AI DAILY PLAN ---")
        print(plan)

def ai_task_summary():

    all_tasks = []

    for task in tasks:

        all_tasks.append(
            f"{task.title} - {task.status}"
        )

    prompt = f"""
    Summarize these tasks briefly:
    {all_tasks}
    """

    summary = call_ai(prompt)

    if summary:

        print("\n--- AI TASK SUMMARY ---")
        print(summary)

load_tasks()

while True:

    print("\n--- AI TASK TRACKER ---")

    print("1. Add Task")
    print("2.Update Task")
    print("3. View Tasks")
    print("4. Complete Task")
    print("5. Delete Task")
    print("6. Search Task")
    print("7. Check Overdue Tasks")
    print("8. Generate Report")
    print("9. AI Productivity Advice")
    print("10. AI Task Prioritization")
    print("11. AI Daily Planner")
    print("12. AI Task Summary")
    print("13. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        add_task()

    elif choice == "2":

        update_task()

    elif choice == "3":

        view_tasks()

    elif choice == "4":

        complete_task()

    elif choice == "5":

        delete_task()

    elif choice == "6":

        search_task()

    elif choice == "7":

        check_overdue_tasks()

    elif choice == "8":

        generate_report()

    elif choice == "9":

        ai_productivity_advice()

    elif choice == "10":

        ai_task_prioritization()

    elif choice == "11":

        ai_daily_planner()

    elif choice == "12":

        ai_task_summary()

    elif choice == "13":

        print("Exiting Program")
        break

    else:

        print("Invalid Choice")