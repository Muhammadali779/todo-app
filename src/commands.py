from datetime import datetime

from rich.console import Console
from rich.table import Table

from .storage import (
    create_task,
    get_tasks,
    save_update_data,
    read_database,
    remove_data,
    save_mark_completed,
    
    
)


def add_task():
    name = input("Task name: ").strip().capitalize()
    description = input("Description: ").strip().capitalize()
    category = input("Category: ").strip().title()
    due_date = input("Date (example: 2025-10-11): ")

    due_date = datetime.strptime(due_date, "%Y-%m-%d")
    if due_date < datetime.now():
        print("Date shoulde be greater than or equal to now.")
        return

    create_task(name, description, category, due_date)
    print("✅ Vazifa muvaffaqiyatli qo'shildi!")


def show_tasks():
    tasks = get_tasks()

    console = Console()

    table = Table(title="All Tasks")
    table.add_column("Number")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Due Date")

    for num, task in enumerate(tasks, start=1):
        du_date = task["due_date"].strftime("%d/%m/%Y")
        table.add_row(str(num), task["name"], task["category"], du_date)
    
    console.print(table)

    num = int(input("Task detail: "))
    task = tasks[num - 1]
    
    status = "❌Incompleted"
    if task["status"]:
        status = "✅ Completed"
    du_date = task["due_date"].strftime("%d/%m/%Y")
    created_date = task["created_date"].strftime("%d/%m/%Y, %H:%M:%S")

    print(f"Task name: {task['name']}")
    print(f"Description: {task['description']}")
    print(f"Category: {task['category']}")
    print(f"Status: {status}")
    print(f"Due Date: {du_date}")
    print(f"Created Date: {created_date}")
    
    print()

def update_task():
    data = read_database()

    if not data:
        return "❌ Hech qanday task mavjud emas"

    selected_id = int(input("Qaysi ID dagi taskni yangilaysiz: "))

    for task in data:
        if selected_id == task['id']:
            new_name = input("Task name: ").strip().capitalize()
            new_description = input("Description: ").strip().capitalize()
            new_category = input("Category: ").strip().title()
            new_due_date = input("Date (example: 11/11/2026) ")

            task['name'] = new_name
            task['description'] = new_description
            task['category'] = new_category
            task['due_date'] = new_due_date

            save_update_data(data) 
            return "✅ Task yangilandi"

    return "❌ Bunday IDdagi task topilmadi"


def delete_task():
    data = read_database()

    if not data:
        return "❌ Hech qanday task mavjud emas"
        
    delete_id = int(input("Qaysi ID dagi taskni uchirmoqchisiz: "))
    for task in data:
        if delete_id == task['id']:
            data.remove(task)

            remove_data(data)
            return "✅ Task o`chirildi"
        
    return "❌ Bunday IDdagi task topilmadi"

def mark_completed():
    data = read_database()
    
    if not data:
        return "❌ Hech qanday task mavjud emas"
    
    completed = int(input("Qaysi ID dagi taskni bajarib bo`ldingiz: "))

    for task in data:
        if completed == task['id']:
            task['status'] = True
            save_mark_completed(data)

            return "✅ Task bajarildi"
        
    return "❌ Bunday IDdagi task topilmadi"

