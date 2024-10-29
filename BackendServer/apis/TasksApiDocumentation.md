
# Tasks API Documentation

## Overview

The Tasks API provides endpoints for managing tasks in a task management application. It allows users to perform CRUD (Create, Read, Update, Delete) operations on tasks. Each task has an ID, title, description, and completion status.

## Logging

The API uses Python's built-in logging module to log events. The logging level is set to `INFO`, allowing both info and error messages to be recorded.

## Namespaces

The API is organized into namespaces using Flask-RESTx. The `tasks` namespace groups all task-related operations.

```python
tasks_ns = Namespace('tasks', description='Task-related operations')
```

## Task Model

The task model defines the structure of a task object. It is used for input validation and response formatting.

```python
task_model = tasks_ns.model('Task', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='The task title'),
    'description': fields.String(required=False, description='The task description'),
    'completed': fields.Boolean(required=True, description='Task completion status')
})
```

## Endpoints

### 1. List Tasks

- **Endpoint**: `/tasks/`
- **Method**: `GET`
- **Description**: Retrieves a list of all tasks.
- **Responses**:
  - **200 OK**: Returns a list of tasks.

#### Example Response

```json
[
    {
        "id": 1,
        "title": "Sample Task 1",
        "description": "This is a sample task.",
        "completed": false
    },
    {
        "id": 2,
        "title": "Sample Task 2",
        "description": "",
        "completed": true
    }
]
```

### 2. Create Task

- **Endpoint**: `/tasks/`
- **Method**: `POST`
- **Description**: Creates a new task.
- **Request Body**:

```json
{
    "title": "New Task",
    "description": "Description of the new task",
    "completed": false
}
```

- **Responses**:
  - **201 Created**: Returns the created task.
  - **400 Bad Request**: If the title is missing.
  - **500 Internal Server Error**: If task creation fails.

#### Example Response

```json
{
    "id": 3,
    "title": "New Task",
    "description": "Description of the new task",
    "completed": false
}
```

### 3. Get Task by ID

- **Endpoint**: `/tasks/<int:task_id>`
- **Method**: `GET`
- **Description**: Retrieves a specific task by its ID.
- **Responses**:
  - **200 OK**: Returns the requested task.
  - **404 Not Found**: If the task with the specified ID does not exist.

#### Example Response

```json
{
    "id": 1,
    "title": "Sample Task 1",
    "description": "This is a sample task.",
    "completed": false
}
```

### 4. Update Task

- **Endpoint**: `/tasks/<int:task_id>`
- **Method**: `PUT`
- **Description**: Updates an existing task by its ID.
- **Request Body**:

```json
{
    "title": "Updated Task Title",
    "description": "Updated description",
    "completed": true
}
```

- **Responses**:
  - **200 OK**: Returns a success message.
  - **404 Not Found**: If the task with the specified ID does not exist.

#### Example Response

```json
{
    "message": "Task with ID 1 updated successfully."
}
```

### 5. Delete Task

- **Endpoint**: `/tasks/<int:task_id>`
- **Method**: `DELETE`
- **Description**: Deletes a task by its ID.
- **Responses**:
  - **204 No Content**: If the deletion is successful.
  - **404 Not Found**: If the task with the specified ID does not exist.

#### Example Response

```json
{
    "message": "Task with ID 1 deleted successfully."
}
```

## Error Handling

- **400 Bad Request**: Occurs when required fields are missing during task creation.
- **404 Not Found**: Occurs when attempting to retrieve, update, or delete a task that does not exist.
- **500 Internal Server Error**: Occurs when there is a failure in the task management operations (e.g., task creation).

## Logging

Logging is utilized throughout the API to track actions and errors:
- `INFO`: For successful operations (e.g., retrieving or creating tasks).
- `ERROR`: For failed operations (e.g., missing title during task creation).
- `WARNING`: For cases where a requested resource is not found.

## Conclusion

This documentation provides an overview of the Tasks API's functionality, detailing how to interact with it effectively. For more information, refer to the code or explore the API endpoints using tools like Postman or curl.
