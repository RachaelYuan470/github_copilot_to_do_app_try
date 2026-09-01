import json
import os
from dataclasses import dataclass


DATA_FILE = "tasks.json"
VALID_PRIORITIES = ("Low", "Medium", "High")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: str = "Medium"


tasks = []
next_id = 1


def normalize_priority(value, default="Medium"):
    if value is None:
        return default

    text = str(value).strip()
    if not text:
        return default

    lowered = text.lower()
    for priority in VALID_PRIORITIES:
        if lowered == priority.lower():
            return priority

    return default


def prompt_for_priority():
    while True:
        print("Priority (Low, Medium, High):")
        choice = input("task-priority> ").strip()
        normalized = normalize_priority(choice, default=None)

        if normalized in VALID_PRIORITIES:
            return normalized

        print("Invalid priority. Please choose Low, Medium, or High.")


def is_invalid_priority_candidate(value):
    if value is None:
        return False

    text = str(value).strip()
    if not text:
        return False

    lowered = text.lower()
    if lowered in {"urgent", "critical"}:
        return True

    if text.isdigit():
        return True

    return False


def load_tasks(file_path=None):
    global tasks, next_id, DATA_FILE

    if file_path is None:
        file_path = DATA_FILE
    else:
        DATA_FILE = file_path

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
        priority = normalize_priority(item.get("priority", "Medium"))

        if isinstance(task_id, int) and isinstance(title, str):
            valid_tasks.append(Task(id=task_id, title=title, done=bool(done), priority=priority))
            max_id = max(max_id, task_id)

    tasks = valid_tasks
    next_id = max_id + 1 if valid_tasks else 1
    return tasks


def save_tasks(file_path=None):
    global DATA_FILE

    if file_path is None:
        file_path = DATA_FILE
    else:
        DATA_FILE = file_path

    data = [
        {"id": task.id, "title": task.title, "done": task.done, "priority": task.priority}
        for task in tasks
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")

    return data


def add_task(title, priority="Medium"):
    global next_id

    if title is None:
        raise ValueError("Task title cannot be empty.")

    cleaned_title = str(title).strip()
    if not cleaned_title:
        raise ValueError("Task title cannot be empty.")

    normalized_priority = normalize_priority(priority, default=None)
    if normalized_priority not in VALID_PRIORITIES:
        raise ValueError("Invalid priority. Please choose Low, Medium, or High.")

    task = Task(id=next_id, title=cleaned_title, done=False, priority=normalized_priority)
    tasks.append(task)
    next_id += 1
    save_tasks()
    print(f"Added task #{task.id}: {task.title} [{task.priority}]")


def list_tasks():
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "done" if task.done else "todo"
        print(f"{task.id}. [{status}] [{task.priority}] {task.title}")


def list_incomplete():
    incomplete = [t for t in tasks if not t.done]
    if not incomplete:
        print("No incomplete tasks.")
        return

    for task in incomplete:
        # reuse the same output format as list_tasks but with explicit todo status
        print(f"{task.id}. [todo] [{task.priority}] {task.title}")


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
    print("  add <task> [priority]")
    print("  list")
    print("  incomplete")
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
            if not title:
                print("Task cannot be empty.")
                return False
            priority = prompt_for_priority()
        else:
            content = parts[1].strip()
            words = content.split()
            title = content
            priority = "Medium"

            if len(words) >= 2:
                last_word = words[-1]
                normalized = normalize_priority(last_word, default=None)
                if normalized in VALID_PRIORITIES:
                    title = " ".join(words[:-1]).strip()
                    priority = normalized
                elif is_invalid_priority_candidate(last_word):
                    print("Invalid priority. Please choose Low, Medium, or High.")
                    return False
                else:
                    title = content
                    priority = prompt_for_priority()
            else:
                title = content
                priority = prompt_for_priority()

            if not title:
                print("Task cannot be empty.")
                return False

        try:
            add_task(title, priority)
        except ValueError as exc:
            print(str(exc))
        return False

    if action in ("list", "ls"):
        list_tasks()
        return False

    if action in ("incomplete", "todo", "pending"):
        list_incomplete()
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
