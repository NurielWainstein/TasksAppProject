import sqlite3
from dataclasses import dataclass
import logging
import os

from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
load_dotenv()
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", f"{os.getcwd()}/dbi/tasks.db")

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool


class TaskDatabaseManager:
    def __init__(self, db_path=SQLITE_DB_PATH):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        # Ensure the directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
            logging.info("Database initialized and table created if not exists.")

    def insert_task(self, title, description, completed=False):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                insert_task_query = """
                INSERT INTO tasks (title, description, completed)
                VALUES (?, ?, ?);
                """
                cursor.execute(insert_task_query, (title, description, completed))
                conn.commit()
                task_id = cursor.lastrowid
                logging.info(f"Task '{title}' inserted successfully with ID: {task_id}.")
                return task_id
        except sqlite3.Error as e:
            logging.error(f"Error inserting task: {e}")

    def read_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks;")
            tasks = [Task(*row) for row in cursor.fetchall()]
            logging.info(f"{len(tasks)} tasks retrieved from the database.")
        return tasks

    def query_tasks(self, **kwargs):
        query = "SELECT * FROM tasks"
        conditions = []
        params = []

        for key, value in kwargs.items():
            if key == "id":
                conditions.append(f"id = ?")
                params.append(value)
            else:
                conditions.append(f"{key} LIKE ?")
                params.append(f"%{value}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            tasks = [Task(*row) for row in cursor.fetchall()]
            logging.info(f"Query executed. Found {len(tasks)} tasks matching criteria.")

        return tasks

    def update_task(self, task_id, **kwargs):
        update_fields = []
        params = []

        for key, value in kwargs.items():
            if value is not None:
                update_fields.append(f"{key} = ?")
                params.append(value)

        params.append(task_id)

        if update_fields:
            update_query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(update_query, params)
                conn.commit()
                logging.info(f"Task with ID {task_id} updated successfully.")
        else:
            logging.warning(f"No fields provided for update for task ID {task_id}.")

    def delete_task(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            logging.info(f"Task with ID {task_id} deleted successfully.")


if __name__ == "__main__":
    # Instantiate the database manager with a specific path
    db = TaskDatabaseManager(db_path="tasks.db")
