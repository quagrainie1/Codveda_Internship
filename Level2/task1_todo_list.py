"""
Codveda Internship — Level 2, Task 1
To-Do List Application
-----------------------
Command-line task manager with JSON persistence.
Supports add, view, complete, delete, and clear operations.
"""

import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


# ─────────────────────────────────────────
#  Persistence helpers
# ─────────────────────────────────────────

def load_tasks() -> list[dict]:
    """Load tasks from JSON file. Returns an empty list if file is missing."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("  ⚠  Could not read tasks file. Starting fresh.")
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Persist the task list to JSON."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────
#  Core operations
# ─────────────────────────────────────────

def add_task(tasks: list[dict], title: str) -> dict:
    """Create and append a new task. Returns the new task."""
    task = {
        "id":        max((t["id"] for t in tasks), default=0) + 1,
        "title":     title.strip(),
        "done":      False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "done_at":   None,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def delete_task(tasks: list[dict], task_id: int) -> dict:
    """Remove a task by ID.

    Raises:
        ValueError: If the ID does not exist.
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks)
            return removed
    raise ValueError(f"No task found with ID {task_id}.")


def complete_task(tasks: list[dict], task_id: int) -> dict:
    """Mark a task as done.

    Raises:
        ValueError: If the ID does not exist or task is already done.
    """
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                raise ValueError(f"Task #{task_id} is already marked as done.")
            task["done"] = True
            task["done_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            return task
    raise ValueError(f"No task found with ID {task_id}.")


def clear_completed(tasks: list[dict]) -> int:
    """Remove all completed tasks. Returns count removed."""
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    return before - len(tasks)


# ─────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────

STATUS_ICON = {True: "✔", False: "○"}
STATUS_LABEL = {True: "Done  ", False: "Pending"}


def display_tasks(tasks: list[dict], filter_mode: str = "all") -> None:
    """Print the task list, optionally filtered."""
    if filter_mode == "pending":
        visible = [t for t in tasks if not t["done"]]
        heading = "PENDING TASKS"
    elif filter_mode == "done":
        visible = [t for t in tasks if t["done"]]
        heading = "COMPLETED TASKS"
    else:
        visible = tasks
        heading = "ALL TASKS"

    print(f"\n  {'─'*52}")
    print(f"  {heading}  ({len(visible)} task{'s' if len(visible) != 1 else ''})")
    print(f"  {'─'*52}")

    if not visible:
        print("  (no tasks to display)")
    else:
        for t in visible:
            icon = STATUS_ICON[t["done"]]
            title = t["title"]
            created = t["created_at"]
            done_info = f"  ✔ {t['done_at']}" if t["done"] else ""
            print(f"  [{icon}] #{t['id']:<4} {title}")
            print(f"           Added: {created}{done_info}")

    pending = sum(1 for t in tasks if not t["done"])
    done    = sum(1 for t in tasks if t["done"])
    print(f"  {'─'*52}")
    print(f"  Total: {len(tasks)}  |  Pending: {pending}  |  Done: {done}")


def display_menu() -> None:
    print("\n" + "=" * 45)
    print("         TO-DO LIST APPLICATION")
    print("=" * 45)
    print("  [1] Add a task")
    print("  [2] View all tasks")
    print("  [3] View pending tasks")
    print("  [4] View completed tasks")
    print("  [5] Mark task as done")
    print("  [6] Delete a task")
    print("  [7] Clear all completed tasks")
    print("  [0] Exit")
    print("=" * 45)


def get_task_id(prompt: str) -> int:
    """Prompt until the user enters a valid positive integer."""
    while True:
        try:
            val = int(input(prompt).strip())
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("  ✗ Please enter a valid task ID (positive integer).")


# ─────────────────────────────────────────
#  Main loop
# ─────────────────────────────────────────

def main() -> None:
    tasks = load_tasks()
    print(f"\n  Loaded {len(tasks)} task(s) from '{TASKS_FILE}'.")

    while True:
        display_menu()
        choice = input("  Your choice: ").strip()

        # ── Add ──
        if choice == "1":
            title = input("\n  Task title: ").strip()
            if not title:
                print("  ✗ Title cannot be empty.")
                continue
            task = add_task(tasks, title)
            print(f"  ✔ Task #{task['id']} added: \"{task['title']}\"")

        # ── View all ──
        elif choice == "2":
            display_tasks(tasks, "all")

        # ── View pending ──
        elif choice == "3":
            display_tasks(tasks, "pending")

        # ── View completed ──
        elif choice == "4":
            display_tasks(tasks, "done")

        # ── Mark done ──
        elif choice == "5":
            display_tasks(tasks, "pending")
            task_id = get_task_id("\n  Enter task ID to mark as done: ")
            try:
                task = complete_task(tasks, task_id)
                print(f"  ✔ Task #{task['id']} marked as done: \"{task['title']}\"")
            except ValueError as e:
                print(f"  ✗ {e}")

        # ── Delete ──
        elif choice == "6":
            display_tasks(tasks, "all")
            task_id = get_task_id("\n  Enter task ID to delete: ")
            confirm = input(f"  Are you sure you want to delete task #{task_id}? (y/n): ").strip().lower()
            if confirm != "y":
                print("  Deletion cancelled.")
                continue
            try:
                task = delete_task(tasks, task_id)
                print(f"  ✔ Task #{task['id']} deleted: \"{task['title']}\"")
            except ValueError as e:
                print(f"  ✗ {e}")

        # ── Clear completed ──
        elif choice == "7":
            removed = clear_completed(tasks)
            if removed:
                print(f"  ✔ Removed {removed} completed task(s).")
            else:
                print("  ℹ  No completed tasks to remove.")

        # ── Exit ──
        elif choice == "0":
            print(f"\n  Tasks saved to '{TASKS_FILE}'. Goodbye!\n")
            break

        else:
            print("  ✗ Invalid choice. Please select 0–7.")


if __name__ == "__main__":
    main()
