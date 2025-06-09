TASKS_FILE = "tasks.txt"

def load_tasks():
  """Loads tasks from the tasks file."""
  try:
    with open(TASKS_FILE, "r") as f:
      tasks = [line.strip() for line in f.readlines()]
    return tasks
  except FileNotFoundError:
    return []
  except (IOError, OSError) as e:
    print(f"Error: Could not read tasks from {TASKS_FILE}. {e}")
    return []

def save_tasks(tasks):
  """Saves tasks to the tasks file."""
  try:
    with open(TASKS_FILE, "w") as f:
      for task in tasks:
        f.write(task + "\n")
  except (IOError, OSError) as e:
    print(f"Error: Could not save tasks to {TASKS_FILE}. {e}")

def add_task(task_description):
  """Adds a task to the list."""
  tasks = load_tasks()
  tasks.append(task_description)
  save_tasks(tasks)
  print("Task added.")

def view_tasks():
  """Views all tasks in the list."""
  tasks = load_tasks()
  if not tasks:
    print("No tasks in the list.")
  else:
    for i, task in enumerate(tasks):
      print(f"{i+1}. {task}")

def update_task(task_index, new_description):
  """Updates a task in the list."""
  tasks = load_tasks()
  try:
    # Assuming task_index is already an int from main()
    if 1 <= task_index <= len(tasks):
      tasks[task_index - 1] = new_description
      save_tasks(tasks)
      print("Task updated.")
    else:
      print("Error: Invalid task number.")
  except IndexError: # Should not happen if task_index is validated in main
      print("Error: Invalid task number.")


def mark_task_done(task_index):
  """Marks a task as done."""
  tasks = load_tasks()
  try:
    # Assuming task_index is already an int from main()
    if 1 <= task_index <= len(tasks):
      task_to_mark = tasks[task_index - 1]
      if task_to_mark.startswith("[DONE] "):
        print("Task is already marked as done.")
      else:
        tasks[task_index - 1] = "[DONE] " + task_to_mark
        save_tasks(tasks)
        print("Task marked as done.")
    else:
      print("Error: Invalid task number.")
  except IndexError: # Should not happen if task_index is validated in main
      print("Error: Invalid task number.")

def delete_task(task_index):
  """Deletes a task from the list."""
  tasks = load_tasks()
  try:
    # Assuming task_index is already an int from main()
    if 1 <= task_index <= len(tasks):
      tasks.pop(task_index - 1)
      save_tasks(tasks)
      print("Task deleted.")
    else:
      print("Error: Invalid task number.")
  except IndexError: # Should not happen if task_index is validated in main
      print("Error: Invalid task number.")

def main():
  """Runs the command-line interface for the to-do application."""
  while True:
    print("\nTo-Do List Application")
    print("1. Add task")
    print("2. View tasks")
    print("3. Update task")
    print("4. Mark task as done")
    print("5. Delete task")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
      description = input("Enter task description: ")
      add_task(description)
    elif choice == "2":
      view_tasks()
    elif choice == "3":
      try:
        task_num = int(input("Enter task number to update: "))
        new_description = input("Enter new task description: ")
        update_task(task_num, new_description)
      except ValueError:
        print("Error: Invalid task number. Please enter a number.")
    elif choice == "4":
      try:
        task_num = int(input("Enter task number to mark as done: "))
        mark_task_done(task_num)
      except ValueError:
        print("Error: Invalid task number. Please enter a number.")
    elif choice == "5":
      try:
        task_num = int(input("Enter task number to delete: "))
        delete_task(task_num)
      except ValueError:
        print("Error: Invalid task number. Please enter a number.")
    elif choice == "6":
      print("Exiting application.")
      break
    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()
