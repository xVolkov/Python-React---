import requests

# Base URL of the Flask service
base_url = "http://localhost:5000"
user_id = None  # Store the user's ID after login or registration

print("\n##########################################################################")
print("\n            << Welcome to the Flask RESTful Task Manager! >>")
print("\n##########################################################################")

def welcome_msg():
    while True:
        
        print("\nSelect one of the following options (1/2):")
        print("1. Register")
        print("2. Login")
        selection = input()
        
        if selection == '1': 
            register_user()
            break;
        elif selection == '2':  
            login_user()
            break;
        else:
            print("Wrong input, type 1 to Register, or 2 to Login.")

def print_instructions():
    print("\nYou can use the following commands:")
    print("1. Add a Task")
    print("2. Get a Task")
    print("3. Update a Task")
    print("4. Delete a Task")
    print("5. List all Tasks")
    print("6. Exit the program")

def register_user():
    print("Register a User:")
    username = input("Username: ")
    password = input("Password: ")

    user_data = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{base_url}/register", json=user_data)
    print(f"\n>> Register - Response:", response.status_code)
    print(response.json())

def login_user():
    global user_id  # Access the user_id variable
    print("Login:")
    username = input("Username: ")
    password = input("Password: ")

    user_data = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{base_url}/login", json=user_data)
    if response.status_code == 200:
        user_id = response.json()['user_id']
        print(f"\n>> Login - Response:", response.status_code)
        print(response.json())
    else:
        print(f"\n>> Login - Response:", response.status_code)
        print(response.json())

def add_task():
    if user_id is None:
        print("You must login or register first.")
        return

    print("Add a Task:")
    description = input("Description: ")
    priority = input("Priority (high/medium/low) - OPTIONAL: ")
    due_date = input("Due Date (MM/DD/YYYY) - OPTIONAL: ")

    task_data = {
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "user_id": user_id
    }

    response = requests.post(f"{base_url}/tasks", json=task_data)
    print(f"\n>> ADD a Task - Response:", response.status_code)
    print(response.json())

def get_task():
    if user_id is None:
        print("You must login or register first.")
        return

    print("Get a Task:")
    task_id = input("Task ID: ")

    response = requests.get(f"{base_url}/tasks/{task_id}?user_id={user_id}")
    if response.status_code == 200:
        print(f"\n>> GET Task {task_id} - Response:", response.status_code)
        print(response.json())
    else:
        print(f"\n>> GET Task {task_id} - Response:", response.status_code)
        print(response.json())

def update_task():
    if user_id is None:
        print("You must login or register first.")
        return

    print("Update a Task:")
    task_id = input("Task ID: ")
    description = input("New Description (or press Enter to keep the same): ")
    priority = input("New Priority (or press Enter to keep the same): ")
    due_date = input("New Due Date (MM/DD/YYYY) (or press Enter to keep the same): ")

    task_data = {}
    if description:
        task_data["description"] = description
    if priority:
        task_data["priority"] = priority
    if due_date:
        task_data["due_date"] = due_date

    response = requests.put(f"{base_url}/tasks/{task_id}?user_id={user_id}", json=task_data)
    print(f"\n>> UPDATE Task {task_id} - Response:", response.status_code)
    print(response.json())

def delete_task():
    if user_id is None:
        print("You must login or register first.")
        return

    print("Delete a Task:")
    task_id = input("Task ID: ")

    response = requests.delete(f"{base_url}/tasks/{task_id}?user_id={user_id}")
    print(f"\n>> DELETE Task {task_id} - Response:", response.status_code)
    print(response.json())

def list_tasks():
    if user_id is None:
        print("You must login or register first.")
        return

    response = requests.get(f"{base_url}/tasks?user_id={user_id}")
    if response.status_code == 200:
        print("\n>> List of Tasks:")
        tasks = response.json()
        for task in tasks:
            print(task)
    else:
        print(f"\n>> List Tasks - Response:", response.status_code)
        print(response.json())

######## RUNNING THE CODE #########

welcome_msg() # Prints welcome message to have the user either login or register

while True:
    print_instructions()
    choice = input("\nEnter your choice (1/2/3/4/5/6): ")

    if choice == "1":
        add_task()
    elif choice == "2":
        get_task()
    elif choice == "3":
        update_task()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        list_tasks()
    elif choice == "6":
        print("Connection terminated. Goodbye!")
        break
    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")