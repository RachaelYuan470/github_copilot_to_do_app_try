import json

import pytest

import todo


def reset_state():
    todo.tasks = []
    todo.next_id = 1
    todo.DATA_FILE = "tasks.json"


def test_add_task():
    reset_state()

    todo.add_task("Buy milk")

    assert len(todo.tasks) == 1
    assert todo.tasks[0].id == 1
    assert todo.tasks[0].title == "Buy milk"
    assert todo.tasks[0].done is False
    assert todo.tasks[0].priority == "Medium"


def test_complete_task():
    reset_state()
    todo.add_task("Write report")

    todo.complete_task(1)

    assert todo.tasks[0].done is True


def test_complete_task_persists_to_file(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        json.dumps([
            {"id": 1, "title": "Write report", "done": False, "priority": "Medium"},
        ]),
        encoding="utf-8",
    )

    todo.DATA_FILE = str(file_path)
    todo.load_tasks(str(file_path))
    todo.complete_task(1)

    assert todo.tasks[0].done is True
    assert json.loads(file_path.read_text(encoding="utf-8")) == [
        {"id": 1, "title": "Write report", "done": True, "priority": "Medium"},
    ]


def test_delete_task():
    reset_state()
    todo.add_task("Read book")
    todo.add_task("Call mom")

    todo.delete_task(1)

    assert len(todo.tasks) == 1
    assert todo.tasks[0].id == 2
    assert todo.tasks[0].title == "Call mom"


def test_invalid_task_numbers(capsys):
    reset_state()
    todo.add_task("Test task")

    todo.complete_task(999)
    todo.delete_task(999)

    captured = capsys.readouterr()
    output = captured.out

    assert "Task #999 not found." in output
    assert output.count("Task #999 not found.") == 2


def test_load_tasks_from_file(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        json.dumps([
            {"id": 1, "title": "Read", "done": False, "priority": "High"},
            {"id": 2, "title": "Write", "done": True, "priority": "Low"},
        ]),
        encoding="utf-8",
    )

    todo.DATA_FILE = str(file_path)
    loaded = todo.load_tasks(str(file_path))

    assert len(loaded) == 2
    assert loaded[0].title == "Read"
    assert loaded[0].priority == "High"
    assert loaded[1].done is True
    assert loaded[1].priority == "Low"
    assert todo.next_id == 3


def test_save_tasks_to_file(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    todo.DATA_FILE = str(file_path)
    todo.tasks = [
        todo.Task(id=1, title="Study Python", done=False, priority="High"),
        todo.Task(id=2, title="Exercise", done=True, priority="Low"),
    ]
    todo.next_id = 3

    saved = todo.save_tasks(str(file_path))

    assert saved == [
        {"id": 1, "title": "Study Python", "done": False, "priority": "High"},
        {"id": 2, "title": "Exercise", "done": True, "priority": "Low"},
    ]
    assert json.loads(file_path.read_text(encoding="utf-8")) == saved


def test_missing_or_empty_file_is_handled_gracefully(tmp_path):
    reset_state()
    missing_file = tmp_path / "missing.json"
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("", encoding="utf-8")

    loaded_missing = todo.load_tasks(str(missing_file))
    loaded_empty = todo.load_tasks(str(empty_file))

    assert loaded_missing == []
    assert loaded_empty == []
    assert todo.tasks == []
    assert todo.next_id == 1


def test_load_valid_priorities_from_file(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        json.dumps([
            {"id": 1, "title": "Low task", "done": False, "priority": "Low"},
            {"id": 2, "title": "Medium task", "done": False, "priority": "Medium"},
            {"id": 3, "title": "High task", "done": False, "priority": "High"},
        ]),
        encoding="utf-8",
    )

    loaded = todo.load_tasks(str(file_path))

    assert [task.priority for task in loaded] == ["Low", "Medium", "High"]


def test_load_invalid_priority_defaults_to_medium(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        json.dumps([
            {"id": 1, "title": "Legacy task", "done": False},
            {"id": 2, "title": "Urgent task", "done": False, "priority": "Urgent"},
            {"id": 3, "title": "Null task", "done": False, "priority": None},
        ]),
        encoding="utf-8",
    )

    loaded = todo.load_tasks(str(file_path))

    assert [task.priority for task in loaded] == ["Medium", "Medium", "Medium"]
    assert [task.title for task in loaded] == ["Legacy task", "Urgent task", "Null task"]


def test_load_multiple_tasks_with_mixed_validity(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        json.dumps([
            {"id": 1, "title": "Valid 1", "done": False, "priority": "Low"},
            {"id": 2, "title": "Invalid", "done": False, "priority": "Urgent"},
            {"id": 3, "title": "Valid 2", "done": True, "priority": "High"},
        ]),
        encoding="utf-8",
    )

    loaded = todo.load_tasks(str(file_path))

    assert len(loaded) == 3
    assert loaded[0].priority == "Low"
    assert loaded[1].priority == "Medium"
    assert loaded[2].priority == "High"


def test_save_tasks_never_writes_invalid_priority(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    todo.tasks = [
        todo.Task(id=1, title="One", done=False, priority="Low"),
        todo.Task(id=2, title="Two", done=True, priority="Medium"),
        todo.Task(id=3, title="Three", done=False, priority="High"),
    ]
    todo.next_id = 4

    saved = todo.save_tasks(str(file_path))

    assert all(task["priority"] in todo.VALID_PRIORITIES for task in saved)
    assert all(task["priority"] is not None for task in saved)
    assert saved[0]["priority"] == "Low"
    assert saved[1]["priority"] == "Medium"
    assert saved[2]["priority"] == "High"


@pytest.mark.parametrize("priority", ["Low", "Medium", "High"])
def test_add_task_with_each_priority(priority):
    reset_state()

    todo.add_task("Priority test", priority)

    assert todo.tasks[0].priority == priority


def test_add_task_rejects_empty_title():
    reset_state()

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        todo.add_task("")

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        todo.add_task("   ")

    assert todo.tasks == []


def test_add_task_strips_surrounding_whitespace():
    reset_state()

    todo.add_task("  Finish report  ", "High")

    assert len(todo.tasks) == 1
    assert todo.tasks[0].title == "Finish report"
    assert todo.tasks[0].priority == "High"


def test_add_task_with_invalid_priority_raises_value_error():
    reset_state()

    with pytest.raises(ValueError, match="Invalid priority"):
        todo.add_task("Urgent task", "Urgent")

    assert todo.tasks == []


def test_add_command_with_invalid_priority_does_not_create_task(capsys):
    reset_state()

    result = todo.process_command("add Write tests Critical")

    captured = capsys.readouterr()
    assert result is False
    assert len(todo.tasks) == 0
    assert "Invalid priority" in captured.out
    assert "Critical" not in "".join(task.title for task in todo.tasks)

    todo.process_command("add Review plan High")
    assert len(todo.tasks) == 1
    assert todo.tasks[0].title == "Review plan"
    assert todo.tasks[0].priority == "High"


def test_list_tasks_displays_priority(capsys):
    reset_state()
    todo.tasks = [
        todo.Task(id=1, title="Design app", done=False, priority="High"),
    ]

    todo.list_tasks()

    output = capsys.readouterr().out
    assert "[High]" in output
    assert "Design app" in output


def test_incomplete_command_shows_only_incomplete(capsys):
    reset_state()
    todo.tasks = [
        todo.Task(id=1, title="A", done=False, priority="Low"),
        todo.Task(id=2, title="B", done=True, priority="High"),
        todo.Task(id=3, title="C", done=False, priority="Medium"),
    ]

    todo.process_command("incomplete")

    output = capsys.readouterr().out
    assert "A" in output
    assert "C" in output
    assert "B" not in output


def test_load_old_task_without_priority(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        json.dumps([
            {"id": 1, "title": "Legacy task", "done": False},
        ]),
        encoding="utf-8",
    )

    loaded = todo.load_tasks(str(file_path))

    assert len(loaded) == 1
    assert loaded[0].priority == "Medium"
    assert loaded[0].title == "Legacy task"
