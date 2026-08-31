import json

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


def test_complete_task():
    reset_state()
    todo.add_task("Write report")

    todo.complete_task(1)

    assert todo.tasks[0].done is True


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
            {"id": 1, "title": "Read", "done": False},
            {"id": 2, "title": "Write", "done": True},
        ]),
        encoding="utf-8",
    )

    todo.DATA_FILE = str(file_path)
    loaded = todo.load_tasks(str(file_path))

    assert len(loaded) == 2
    assert loaded[0].title == "Read"
    assert loaded[1].done is True
    assert todo.next_id == 3


def test_save_tasks_to_file(tmp_path):
    reset_state()
    file_path = tmp_path / "tasks.json"
    todo.DATA_FILE = str(file_path)
    todo.tasks = [
        todo.Task(id=1, title="Study Python", done=False),
        todo.Task(id=2, title="Exercise", done=True),
    ]
    todo.next_id = 3

    saved = todo.save_tasks(str(file_path))

    assert saved == [
        {"id": 1, "title": "Study Python", "done": False},
        {"id": 2, "title": "Exercise", "done": True},
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
