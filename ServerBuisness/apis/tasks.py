import logging
from flask_restx import Namespace, Resource, fields
from flask import request, abort
from ServerBuisness.dbi.TasksDBManager import TaskDatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a namespace for the tasks API
tasks_ns = Namespace('tasks', description='Task-related operations')

db_manager = TaskDatabaseManager()

# Define the task model
task_model = tasks_ns.model('Task', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'title': fields.String(required=True, description='The task title'),
    'description': fields.String(required=False, description='The task description'),
    'completed': fields.Boolean(required=True, description='Task completion status')
})

@tasks_ns.route('/')
class TaskList(Resource):
    @tasks_ns.doc('list_tasks')
    @tasks_ns.marshal_list_with(task_model)
    def get(self):
        """Retrieve a list of all tasks"""
        logger.info("Retrieving list of all tasks.")
        tasks = db_manager.read_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks.")
        return tasks, 200

    @tasks_ns.doc('create_task')
    @tasks_ns.expect(task_model)
    def post(self):
        """Create a new task"""
        data = request.json
        title = data.get('title')
        description = data.get('description', '')
        completed = data.get('completed', False)

        if not title:
            logger.error("Title is required for task creation.")
            abort(400, description="Title is required.")

        task_id = db_manager.insert_task(title, description, completed)
        if task_id is None:
            logger.error("Failed to create task.")
            abort(500, description="Failed to create task.")

        logger.info(f"Task created with ID: {task_id}.")
        return {'id': task_id, 'title': title, 'description': description, 'completed': completed}, 201

@tasks_ns.route('/<int:task_id>')
class TaskResource(Resource):
    @tasks_ns.doc('get_task')
    @tasks_ns.marshal_with(task_model)
    def get(self, task_id):
        """Retrieve a specific task by ID"""
        logger.info(f"Retrieving task with ID: {task_id}.")
        search_args = {"id": task_id}
        matching_tasks = db_manager.query_tasks(**search_args)

        if not matching_tasks:
            logger.warning(f"Task with ID {task_id} not found.")
            abort(404, description=f"Task with ID {task_id} not found.")
        task = matching_tasks[0]
        logger.info(f"Task with ID {task_id} retrieved successfully.")
        return task, 200

    @tasks_ns.doc('update_task')
    @tasks_ns.expect(task_model)
    def put(self, task_id):
        """Update an existing task by ID"""
        data = request.json
        search_args = {"id": task_id}
        task = db_manager.query_tasks(**search_args)

        if task is None:
            logger.warning(f"Task with ID {task_id} not found for update.")
            abort(404, description=f"Task with ID {task_id} not found.")

        db_manager.update_task(task_id, **data)
        logger.info(f"Task with ID {task_id} updated successfully.")
        return {'message': f'Task with ID {task_id} updated successfully.'}, 200

    @tasks_ns.doc('delete_task')
    def delete(self, task_id):
        """Delete a task by ID"""
        logger.info(f"Deleting task with ID: {task_id}.")
        search_args = {"id": task_id}
        task = db_manager.query_tasks(**search_args)

        if task is None:
            logger.warning(f"Task with ID {task_id} not found for deletion.")
            abort(404, description=f"Task with ID {task_id} not found.")

        db_manager.delete_task(task_id)
        logger.info(f"Task with ID {task_id} deleted successfully.")
        return {'message': f'Task with ID {task_id} deleted successfully.'}, 204
