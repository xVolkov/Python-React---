# Python Flask RESTful Task Scheduler with User Authentication

## Developer: xVolkov
## Date: 11/03/2023

### Application Description

The Task Manager is a web-based application that allows users to manage their tasks efficiently. The application incorporates multiple functionalities, such as user authentication, task persistence, and user-specific tasks management. It ensures data privacy, allowing only the user to access and manage their tasks securely. Users can create, retrieve, update, and delete tasks, as well as retrieve all their tasks at once. The backend infrastructure is built using the Python Flask framework and follows the RESTful service model (REST APIs).

### Features

- **User Authentication**: Secure registration and login for users.
- **Task Management**: Create, retrieve, update, and delete tasks.
- **User-Specific Tasks**: Ensure that only the user can access and manage their own tasks.
- **Task Persistence**: Tasks and user data are persisted in JSON files.

### Instructions to Run the Application

1. Ensure that `tasks.json` and `users.json` are both within the same directory as the source code (`app.py` & `appUI.py`).
2. Run `app.py` in CMD or an IDE of your choice to start the REST application with all its core features.
3. Run `appUI.py` in CMD or an IDE of your choice to simulate a user-interface for accessing the application's functions.
4. Login or register an account.
5. Follow the instructions displayed on your terminal.

### Running the Application

#### Step 1: Set Up Environment
Make sure you have Python and Flask installed. You can install Flask using pip:
```sh
pip install Flask
```

#### Step 2: Run the Backend Server
```sh
python app.py
```
The backend server will start running on http://localhost:5000.

#### Step 3: Run the User Interface Simulation
Open another terminal and run:
```sh
python appUI.py
```

### API Endpoints
- #### User Registration: 'POST /register'
  - Request Body: {"username": "user", "password": "pass"}
  - Response: {"message": "User user registered successfully."}
- #### User Login: 'POST /login'
  - Request Body: {"username": "user", "password": "pass"}
  - Response: {"user_id": 1, "message": "Login successful."}
- #### Add Task: POST /tasks
Request Body: {"description": "Task", "priority": "high", "due_date": "MM/DD/YYYY", "user_id": 1}
Response: {"message": "Task successfully added. Task ID is '1'"}
- #### List Tasks: GET /tasks
Request Parameters: user_id
Response: List of user-specific tasks
- #### Get Task: GET /tasks/<int:task_id>
Request Parameters: user_id
Response: Task details
- #### Update Task: PUT /tasks/<int:task_id>
Request Parameters: user_id
Request Body: {"description": "Updated Task", "priority": "medium", "due_date": "MM/DD/YYYY"}
Response: {"message": "Task with ID '1' updated successfully."}
- #### Delete Task: DELETE /tasks/<int:task_id>
Request Parameters: user_id
Response: {"message": "Task 1 deleted successfully."}

### Sample User Interface Commands
1. Register: Register a new user.
2. Login: Login with an existing user account.
3. Add a Task: Create a new task.
4. Get a Task: Retrieve a specific task by its ID.
5. Update a Task: Update the details of an existing task.
6. Delete a Task: Delete a task by its ID.
7. List all Tasks: Retrieve all tasks for the logged-in user.
8. Exit: Terminate the program.

### Files
* app.py: The main application file containing the Flask RESTful API.
* appUI.py: A simulation of a user interface to interact with the RESTful API.
