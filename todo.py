import json
import os
from dataclasses import dataclass


DATA_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


tasks = []
next_id = 1


def load_tasks(file_path=None):
    global tasks, next_id

    if file_path is None:
        file_path = DATA_FILE

    if not os.path.exists(file_path):
        tasks = []
        next_id = 1
        return tasks

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = file.read().strip()
    except OSError:
        tasks = []
        next_id = 1
        return tasks

    if not raw_data:
        tasks = []
        next_id = 1
        return tasks

    try:
        loaded = json.loads(raw_data)
    except json.JSONDecodeError:
        tasks = []
        next_id = 1
        return tasks

    if not isinstance(loaded, list):
        tasks = []
        next_id = 1
        return tasks

    valid_tasks = []
    max_id = 0

    for item in loaded:
        if not isinstance(item, dict):
            continue

        task_id = item.get("id")
        title = item.get("title")
        done = item.get("done", False)

        if isinstance(task_id, int) and isinstance(title, str):
            valid_tasks.append(Task(id=task_id, title=title, done=bool(done)))
            max_id = max(max_id, task_id)

    tasks = valid_tasks
    next_id = max_id + 1 if valid_tasks else 1
    return tasks


def save_tasks(file_path=None):
    if file_path is None:
        file_path = DATA_FILE

    data = [
        {"id": task.id, "title": task.title, "done": task.done}
        for task in tasks
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")

    return data


def add_task(title):
    global next_id

    task = Task(id=next_id, title=title.strip(), done=False)
    tasks.append(task)
    next_id += 1
    save_tasks()
    print(f"Added task #{task.id}: {task.title}")


def list_tasks():
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "done" if task.done else "todo"
        print(f"{task.id}. [{status}] {task.title}")


def complete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            if task.done:
                print(f"Task #{task.id} is already complete.")
            else:
                task.done = True
                save_tasks()
                print(f"Completed task #{task.id}: {task.title}")
            return

    print(f"Task #{task_id} not found.")


def delete_task(task_id):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            removed_task = tasks.pop(index)
            save_tasks()
            print(f"Deleted task #{removed_task.id}: {removed_task.title}")
            return

    print(f"Task #{task_id} not found.")


def show_help():
    print("Commands:")
    print("  add <task>")
    print("  list")
    print("  complete <task_id>")
    print("  delete <task_id>")
    print("  help")
    print("  exit")


def process_command(command_line):
    command = command_line.strip()

    if not command:
        return False

    parts = command.split(maxsplit=1)
    action = parts[0].lower()

    if action == "add":
        if len(parts) < 2 or not parts[1].strip():
            title = input("Enter task: ").strip()
        else:
            title = parts[1].strip()

        if not title:
            print("Task cannot be empty.")
            return False

        add_task(title)
        return False

    if action in ("list", "ls"):
        list_tasks()
        return False

    if action in ("complete", "done"):
        if len(parts) < 2:
            print("Usage: complete <task_id>")
            return False

        try:
            task_id = int(parts[1])
            complete_task(task_id)
        except ValueError:
            print("Task ID must be a number.")
        return False

    if action == "delete":
        if len(parts) < 2:
            print("Usage: delete <task_id>")
            return False

        try:
            task_id = int(parts[1])
            delete_task(task_id)
        except ValueError:
            print("Task ID must be a number.")
        return False

    if action in ("help", "?"):
        show_help()
        return False

    if action in ("exit", "quit"):
        print("Goodbye!")
        return True

    print("Unknown command. Type 'help' for a list of commands.")
    return False


def main():
    load_tasks()
    print("Task Manager")
    show_help()

    while True:
        try:
            command = input("task> ")
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if process_command(command):
            break


if __name__ == "__main__":
    main()
