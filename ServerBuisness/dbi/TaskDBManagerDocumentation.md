
# Task Database Manager Documentation

## Overview

The `TaskDatabaseManager` class provides a way to interact with a SQLite database for managing tasks. It supports operations for inserting, reading, querying, updating, and deleting tasks.

## Dependencies

- `sqlite3`: For SQLite database operations.
- `dataclasses`: To define the Task data structure.
- `logging`: For logging operations and errors.
- `os`: For handling file paths.
- `dotenv`: For loading environment variables from a `.env` file.

## Environment Variables

The database path can be configured using an environment variable:
- **SQLITE_DB_PATH**: The path to the SQLite database file. If not set, it defaults to `./dbi/tasks.db`.

## Task Data Class

The `Task` data class represents the structure of a task object.

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
```
## TaskDatabaseManager Class

### Initialization

The `TaskDatabaseManager` class is initialized with an optional `db_path` argument. It automatically initializes the database and creates the `tasks` table if it does not exist.

```python
class TaskDatabaseManager:
    def __init__(self, db_path=SQLITE_DB_PATH):
        self.db_path = db_path
        self.init_db()
```

### Methods

#### 1. `init_db()`

- **Description**: Initializes the database and creates the `tasks` table if it does not exist.
- **Logging**: Logs the initialization status.

#### 2. `insert_task(title, description, completed=False)`

- **Description**: Inserts a new task into the database.
- **Parameters**:
  - `title`: The title of the task (required).
  - `description`: The description of the task (optional).
  - `completed`: The completion status of the task (default is `False`).
- **Returns**: The ID of the inserted task.
- **Logging**: Logs success or error messages during insertion.

#### 3. `read_tasks()`

- **Description**: Retrieves all tasks from the database.
- **Returns**: A list of `Task` objects.
- **Logging**: Logs the number of tasks retrieved.

#### 4. `query_tasks(**kwargs)`

- **Description**: Retrieves tasks based on specified criteria.
- **Parameters**: Accepts keyword arguments that correspond to task fields (e.g., `id`, `title`, `description`).
- **Returns**: A list of `Task` objects matching the criteria.
- **Logging**: Logs the number of tasks found.

#### 5. `update_task(task_id, **kwargs)`

- **Description**: Updates an existing task based on its ID.
- **Parameters**:
  - `task_id`: The ID of the task to update (required).
  - `kwargs`: The fields to update and their new values.
- **Logging**: Logs the update status or warnings if no fields are provided.

#### 6. `delete_task(task_id)`

- **Description**: Deletes a task from the database based on its ID.
- **Parameters**: `task_id`: The ID of the task to delete (required).
- **Logging**: Logs the deletion status.

## Example Usage

To use the `TaskDatabaseManager`, you can instantiate it and call its methods:

```python
if __name__ == "__main__":
    db = TaskDatabaseManager(db_path="tasks.db")
    # Example: Insert a task
    task_id = db.insert_task(title="Sample Task", description="This is a sample task.", completed=False)
    # Example: Read all tasks
    tasks = db.read_tasks()
    print(tasks)
```

## Conclusion

This documentation provides a comprehensive overview of the `TaskDatabaseManager` class and its methods for managing tasks in a SQLite database. For further information, refer to the source code or the relevant Python documentation.
