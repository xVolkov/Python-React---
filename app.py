from flask import Flask, request, jsonify
import datetime
import json
import os

app = Flask(__name__)
tasks_filename = 'tasks.json'
users_filename = 'users.json'

# Load tasks from the JSON file or create an empty list if the file doesn't exist or is empty
if os.path.exists(tasks_filename) and os.path.getsize(tasks_filename) > 0:
    with open(tasks_filename, 'r') as f:
        tasks = json.load(f)
else:
    tasks = []

# Load users from the JSON file or create an empty list if the file doesn't exist or is empty
if os.path.exists(users_filename) and os.path.getsize(users_filename) > 0:
    with open(users_filename, 'r') as f:
        users = json.load(f)
else:
    users = []

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user_id = len(users) + 1  # Generating a unique user ID

    user = {
        "user_id": user_id,
        "username": username,
        "password": password,
    }
    users.append(user)

    with open(users_filename, 'w') as f:
        json.dump(users, f, indent=4)

    return jsonify({"message": f"User {username} registered successfully."}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if user:
        return jsonify({"user_id": user['user_id'], "message": "Login successful."}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    user_id = data.get('user_id')

    # Check if the user exists
    if not next((u for u in users if u['user_id'] == user_id), None):
        return jsonify({"message": "Invalid user ID."}), 401

    # Set "Not set" as the default value if priority or due_date is blank
    priority = data.get('priority', "Not set")
    due_date = data.get('due_date', "Not set")

    # Check if priority or due_date are empty strings and set them to "Not set"
    if not priority.strip():
        priority = "Not set"
    if not due_date.strip():
        due_date = "Not set"

    task = {
        "task_id": len(tasks) + 1,  # Generating a unique task ID
        "user_id": user_id,
        "description": data['description'],
        "priority": priority,
        "due_date": due_date,
    }
    tasks.append(task)

    with open(tasks_filename, 'w') as f:
        json.dump(tasks, f, indent=4)

    return jsonify({"message": f"Task successfully added. Task ID is '{task['task_id']}'"}), 201

@app.route('/tasks', methods=['GET'])  # New route to list all tasks
def list_tasks():
    user_id = int(request.args.get('user_id'))

    # Filter tasks by user_id
    user_tasks = [task for task in tasks if task['user_id'] == user_id]
    return jsonify(user_tasks), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    user_id = int(request.args.get('user_id'))

    # Check if the user has access to the task
    task = next((t for t in tasks if t['task_id'] == task_id and t['user_id'] == user_id), None)
    if task:
        return jsonify(task), 200
    else:
        return jsonify({"message": f"Task with ID '{task_id}' not found or access denied."}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    user_id = int(request.args.get('user_id'))

    # Check if the user has access to the task
    task = next((t for t in tasks if t['task_id'] == task_id and t['user_id'] == user_id), None)
    if task:
        data = request.get_json()
        if 'description' in data:
            task["description"] = data['description']
        if 'priority' in data:
            task["priority"] = data['priority']
        if 'due_date' in data:
            due_date = data['due_date']
            if not is_valid_due_date(due_date):
                return jsonify({"message": "Invalid due date. Please enter a valid due date (MM/DD/YYYY)."}), 400
            task["due_date"] = due_date

        with open(tasks_filename, 'w') as f:
            json.dump(tasks, f, indent=4)

        return jsonify({"message": f"Task with ID '{task_id}' updated successfully."}), 200
    else:
        return jsonify({"message": f"Task with ID '{task_id}' not found or access denied."}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = int(request.args.get('user_id'))

    # Check if the user has access to the task
    task = next((t for t in tasks if t['task_id'] == task_id and t['user_id'] == user_id), None)
    if task:
        tasks.remove(task)

        with open(tasks_filename, 'w') as f:
            json.dump(tasks, f, indent=4)

        return jsonify({"message": f"Task {task_id} deleted successfully."}), 200
    else:
        return jsonify({"message": f"Task {task_id} not found or access denied."}), 404

def is_valid_due_date(date_str):
    try:
        due_date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        return due_date >= datetime.datetime.now()
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(debug=True)