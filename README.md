# To-Do List Application

A simple and user-friendly To-Do List application built with Flask, SQLAlchemy, Flask-Login, and Flask-WTF, designed to help users manage their tasks effectively.

## Description

This To-Do List application allows users to register, log in, and manage their tasks by adding, updating, and deleting tasks. Tasks can be categorized as "To Do", "Doing", and "Done". The application ensures a seamless user experience with a clean and responsive design.

## Features

- User registration and authentication
- Task creation with details such as title, description, due date, and priority
- Categorize tasks into "To Do", "Doing", and "Done"
- Update task status
- Delete tasks
- Responsive design using Bootstrap

## Installation

### Prerequisites

Ensure you have the following installed on your local machine:

- Python 3.7+
- `pip` (Python package installer)
- `virtualenv` (optional but recommended)

### Clone the Repository

```bash
git clone https://github.com/yourusername/todo-list-app.git
cd todo-list-app
```

### Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```
### Set Up the Database

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```
### Run the Application

```bash
flask run
Open your web browser and navigate to http://127.0.0.1:5000.
```
## Usage

### User Registration

1. Visit the home page.
2. Click on "Register".
3. Fill out the registration form and submit.

### User Login

1. Click on "Login".
2. Enter your registered email and password.

### Managing Tasks

- **Add a Task:** Click on the "Add Task" button, fill out the form, and submit.
- **Update Task Status:** Use the provided buttons to move tasks between "To Do", "Doing", and "Done".
- **Delete a Task:** Click on the "Remove" button to delete a task.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository.**
2. **Create your feature branch**

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Commit your changes**

    ```bash
    git commit -am 'Add some feature'
    ```

4. **Push to the branch**

    ```bash
    git push origin feature/your-feature-name
    ```

5. **Create a new Pull Request.**

## Contact

If you have any questions or suggestions, feel free to reach out:

- **Email:** [darshni211196@gmail.com](mailto:darshni211196@gmail.com)
- **GitHub:** [https://github.com/Darshnipatel21](https://github.com/Darshnipatel21)
