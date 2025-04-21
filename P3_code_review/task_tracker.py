#!/usr/bin/env python3
"""
Task Tracker Application

A simple console application for tracking tasks.
"""
import json
import os
from datetime import datetime
import time

# Global variables
TASKS_FILE = "tasks.json"
tasks = {}

def load_tasks():
    """Load tasks from the JSON file."""
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                tasks = json.load(f)
        except json.JSONDecodeError:
            print("Warning: Tasks file is corrupted.")
            tasks = {}
    else:
        # Create an empty JSON file if it doesn't exist
        save_tasks()

def save_tasks():
    """Save tasks to the JSON file."""
    try: 
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f)
    except IOError as e:
        print(f"Error saving tasks: {e}")            

def generate_task_id():
    """Generate a new unique task ID."""
    existing_ids = [int(task_id) for task_id in tasks.keys()]
    return str(max(existing_ids) + 1 if existing_ids else 1)

def is_valid_date(date_str):
    try:
        due_date = datetime.strptime(date_str, "%Y-%m-%d")
        if due_date < datetime.today():
            print("Error: Due date must be in the future.")
            return False
        return True
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return False

def add_task():
    """Add a new task."""
    print("\n=== Add New Task ===")
    
    title = input("Enter task title: ")
    if not title:
        print("Error: Title cannot be empty.")
        return
    
    description = input("Enter task description: ")
  
    due_date = input("Enter due date (YYYY-MM-DD): ")
    if not is_valid_date(due_date):
        return    

    
    task_id = str(generate_task_id())
    tasks[task_id] = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "incomplete",
        "created_date": datetime.today().strftime("%Y-%m-%d")
    }
    
    
    save_tasks()
    print(f"Task {task_id} added successfully!")

def view_all_tasks():
    """View all tasks."""
    print("\n=== All Tasks ===")
    
    if not tasks:
        print("No tasks found.")
        return
    
    # Set column widths
    print("{:<5} {:<25} {:<12} {:<10}".format("ID", "Title", "Due Date", "Status"))
    print("-" * 60)
    for task_id, task in tasks.items():
        print("{:<5} {:<25} {:<12} {:<10}".format(
            task_id,
            task["title"][:24],  # Truncate long titles
            task["due_date"],
            task["status"]
        ))

def view_task():
    """View details of a specific task."""
    print("\n=== View Task ===")
    
    task_id = input("Enter task ID: ")
    
    if not task_id.isdigit():
        print("Invalid input. Task ID must be a number.")
        return

    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    task = tasks[task_id]
    print(f"ID: {task_id}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Status: {task['status']}")

def update_task():
    """Update an existing task."""
    print("\n=== Update Task ===")
    
    task_id = input("Enter task ID: ")
    
    if not task_id.isdigit():
        print("Invalid input. Task ID must be a number.")
        return
    
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    task = tasks[task_id]
    
    print("Leave field empty to keep current value.")
    print(f"Current Title: {task['title']}")
    new_title = input("New Title: ")
    
    print(f"Current Description: {task['description']}")
    new_description = input("New Description: ")
    
    print(f"Current Due Date: {task['due_date']}")
    new_due_date = input("New Due Date (YYYY-MM-DD): ")
    
    # Update task with new values, keeping old values if input is empty
    if new_title:
        task['title'] = new_title
    if new_description:
        task['description'] = new_description
    if new_due_date:
        if not is_valid_date(new_due_date):
            return        
        task['due_date'] = new_due_date
    
    save_tasks()
    print(f"Task {task_id} updated successfully!")

def mark_task_complete():
    """Mark a task as complete."""
    print("\n=== Mark Task as Complete ===")
    task_id = input("Enter task ID: ")
    
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return

    tasks[task_id]['status'] = 'complete'
    save_tasks()
    print(f"Task {task_id} marked as complete.")

def delete_task():
    """Delete a task."""
    print("\n=== Delete Task ===")
    
    task_id = input("Enter task ID: ")
    
    if task_id not in tasks:
        print(f"Task {task_id} not found.")
        return
    
    confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()
    
    if confirm == 'y':
        del tasks[task_id]
        save_tasks()
        print(f"Task {task_id} deleted successfully!")
    else:
        print("Deletion cancelled.")

def display_menu():
    """Display the main menu."""
    print("\n=== Task Tracker ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Task")
    print("4. Update Task")
    print("5. Mark Task as Complete")
    print("6. Delete Task")
    print("7. Exit")

def main():
    """Main application function."""
    load_tasks()
    
    while True:
        display_menu()
        
        choice = input("Enter your choice (1-7): ")
        
        if not choice.isdigit():
            print("Invalid input. Choice must be a number.")
            continue       
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_task()
        elif choice == "4":
            update_task()
        elif choice == "5":
            mark_task_complete()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting Task Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 