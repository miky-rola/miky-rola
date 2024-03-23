print("\nWelcome to Miky To Do List\n".ljust(40, "="))


def display_menu():
    print("1. Add Task")
    print("2. Remove Task ")
    print("3. Mark Task as Complete")
    print("4. View Tasks")
    print("(blank to exit program)")

def add_task(tasks):
    task_name = input("Enter the task name: ")
    tasks[task_name] = False
    if len(task_name) > 1:
        task_name == []
    print(f"Task '{task_name}' added successfully!😊")

def mark_complete(tasks):
    task_name = input("Enter the task name to mark as complete: ")
    if task_name in tasks:
        tasks[task_name] = True
        print(f"Task '{task_name}' marked as complete!🏆")
    else:
        print(f"Task '{task_name}' not found.")

def remove_task(tasks):
    task_name = input("Enter the task name to remove: ")
    if task_name in tasks:
        del tasks[task_name]
        print(f"Task '{task_name}' removed successfully!😑")
    else:
        print(f"Task '{task_name}' not found.")

def view_tasks(tasks):
    print("\nCurrent Tasks:")
    for task, complete in tasks.items():
        if complete:
            status = "Complete 😉"
        else:
            status = "Incomplete 😒"
        print(f"{task}: {status}")
    print()

def main():
    tasks = {}

    while True:
        display_menu()

        user_choice = input("Enter your choice (1-4): ")

        if user_choice == "1":
            add_task(tasks)
        elif user_choice == "2":
            remove_task(tasks)
        elif user_choice == "3":
            mark_complete(tasks)
        elif user_choice == "4":
            view_tasks(tasks)
        elif user_choice == "":
            print("Exiting the To-Do List application.... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
