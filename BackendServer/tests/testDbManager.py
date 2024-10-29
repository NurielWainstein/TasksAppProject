import pytest
import tempfile
from BackendServer.dbi.TasksDBManager import TaskDatabaseManager

@pytest.fixture
def task_db():
    """Fixture that provides a TaskDatabaseManager with a temporary SQLite database."""
    # Create a temporary file for the SQLite database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as temp_db:
        db = TaskDatabaseManager(db_path=temp_db.name)  # Use the temporary database
        db.init_db()  # Initialize the database
        yield db  # Provide the database to the test
        # Cleanup happens automatically, as the temporary file is deleted when closed

def test_insert_task(task_db):
    task_db.insert_task("Test Task", "This is a test task description.")
    tasks = task_db.read_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "This is a test task description."
    assert not tasks[0].completed


def test_read_tasks_empty(task_db):
    tasks = task_db.read_tasks()
    assert len(tasks) == 0


def test_update_task(task_db):
    task_db.insert_task("Update Task", "This task will be updated.")
    tasks = task_db.read_tasks()
    task_id = tasks[0].id

    task_db.update_task(task_id, title="Updated Task", description="Updated description", completed=True)

    updated_tasks = task_db.read_tasks()
    assert updated_tasks[0].title == "Updated Task"
    assert updated_tasks[0].description == "Updated description"
    assert updated_tasks[0].completed


def test_delete_task(task_db):
    task_db.insert_task("Delete Task", "This task will be deleted.")
    tasks = task_db.read_tasks()
    task_id = tasks[0].id

    task_db.delete_task(task_id)
    final_tasks = task_db.read_tasks()
    assert len(final_tasks) == 0


# def test_update_non_existent_task(task_db):
#     # Trying to update a non-existent task should not throw an error
#     task_db.update_task(999, title="Non-existent Task", description="Should not raise an error.")
#
#
# def test_delete_non_existent_task(task_db):
#     # Trying to delete a non-existent task should not throw an error
#     task_db.delete_task(999)  # No error should be raised


if __name__ == "__main__":
    pytest.main()
