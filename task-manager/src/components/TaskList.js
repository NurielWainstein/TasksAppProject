import React, { useEffect, useState } from 'react';
import './TaskList.css'; // Importing CSS for styles

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [showTasks, setShowTasks] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [completed, setCompleted] = useState(false);
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [queryTitle, setQueryTitle] = useState('');
  const [queryDescription, setQueryDescription] = useState('');
  const [queryCompleted, setQueryCompleted] = useState('');
  const [filteredTasks, setFilteredTasks] = useState([]);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const tasksPerPage = 5;

  const fetchTasks = async () => {
    try {
      const response = await fetch('http://localhost:5000/tasks');
      if (!response.ok) throw new Error('Failed to fetch tasks');
      const data = await response.json();
      setTasks(data);
      setFilteredTasks(data);
      setShowTasks(true);
    } catch (error) {
      setError(error.message);
    }
  };

  const createTask = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/tasks/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, completed }),
      });
      if (!response.ok) throw new Error('Failed to create task');
      const newTask = await response.json();
      setTasks([...tasks, newTask]);
      setFilteredTasks([...tasks, newTask]);
      clearForm();
    } catch (error) {
      setError(error.message);
    }
  };

  const updateTask = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:5000/tasks/${editingTaskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, completed }),
      });
      if (!response.ok) throw new Error('Failed to update task');
      const updatedTasks = tasks.map((task) =>
        task.id === editingTaskId ? { ...task, title, description, completed } : task
      );
      setTasks(updatedTasks);
      setFilteredTasks(updatedTasks);
      clearForm();
    } catch (error) {
      setError(error.message);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`http://localhost:5000/tasks/${taskId}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete task');
      const updatedTasks = tasks.filter((task) => task.id !== taskId);
      setTasks(updatedTasks);
      setFilteredTasks(updatedTasks);
    } catch (error) {
      setError(error.message);
    }
  };

  const clearForm = () => {
    setTitle('');
    setDescription('');
    setCompleted(false);
    setEditingTaskId(null);
    setError(null);
  };

  const queryTasks = () => {
    const results = tasks.filter((task) => {
      const matchesTitle = task.title.toLowerCase().includes(queryTitle.toLowerCase());
      const matchesDescription = task.description.toLowerCase().includes(queryDescription.toLowerCase());
      const matchesCompleted = queryCompleted === '' ? true : (queryCompleted === 'true' ? task.completed : !task.completed);
      return matchesTitle && matchesDescription && matchesCompleted;
    });
    setFilteredTasks(results);
    setCurrentPage(1); // Reset to first page on new query
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Pagination logic
  const indexOfLastTask = currentPage * tasksPerPage;
  const indexOfFirstTask = indexOfLastTask - tasksPerPage;
  const currentTasks = filteredTasks.slice(indexOfFirstTask, indexOfLastTask);

  const nextPage = () => {
    if (currentPage < Math.ceil(filteredTasks.length / tasksPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="task-list-container">
      <h1 className="title">Task Manager</h1>

      {/* Task creation section */}
      <section className="task-creation">
        <h2 className={`subtitle ${editingTaskId ? 'editing-mode' : ''}`}>
          {editingTaskId ? 'Edit Task' : 'Add a New Task'}
        </h2>
        <form className="task-form" onSubmit={editingTaskId ? updateTask : createTask}>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Task Title" required />
          <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Task Description" />
          <label>
            <input type="checkbox" checked={completed} onChange={(e) => setCompleted(e.target.checked)} />
            Completed
          </label>
          <button type="submit" className="submit-button">{editingTaskId ? 'Update Task' : 'Add Task'}</button>
        </form>
        {error && <p className="error-message">Error: {error}</p>}
      </section>

      {/* Search section */}
      <section className="task-search">
        <h2 className="subtitle">Search Tasks</h2>
        <input type="text" value={queryTitle} onChange={(e) => setQueryTitle(e.target.value)} placeholder="Search by Title" />
        <input type="text" value={queryDescription} onChange={(e) => setQueryDescription(e.target.value)} placeholder="Search by Description" />
        <select value={queryCompleted} onChange={(e) => setQueryCompleted(e.target.value)}>
          <option value="">All</option>
          <option value="true">Completed</option>
          <option value="false">Not Completed</option>
        </select>
        <button className="query-button" onClick={queryTasks}>Search</button>
      </section>

      {/* Task list section with pagination */}
      <section className="task-fetching">
        <h2 className="subtitle">Task List</h2>
        <button className="fetch-button" onClick={fetchTasks}>Refresh Tasks</button>
        {showTasks && (
          <>
            <ul className="task-list">
              {currentTasks.map((task) => (
                <li key={task.id} className={`task-item ${task.completed ? 'completed' : 'not-completed'}`}>
                  <div className="task-details">
                    <strong>Title:</strong> {task.title}<br />
                    <strong>Description:</strong> {task.description}<br />
                    <strong>Status:</strong> <span className="status">{task.completed ? '✔️ Completed' : '❌ Not Completed'}</span>
                  </div>
                  <div className="task-actions">
                    <button
                        className="edit-button"
                        onClick={() => {
                          setTitle(task.title);
                          setDescription(task.description);
                          setCompleted(task.completed);
                          setEditingTaskId(task.id);
                          window.scrollTo({top: 0, behavior: 'smooth'}); // Smooth scroll to top
                        }}
                    >
                      Edit
                    </button>
                    <button className="delete-button" onClick={() => deleteTask(task.id)}>Delete</button>
                  </div>
                </li>
              ))}
            </ul>
            <div className="pagination-controls">
              <button onClick={prevPage} disabled={currentPage === 1}>Previous</button>
              <span>Page {currentPage} of {Math.ceil(filteredTasks.length / tasksPerPage)}</span>
              <button onClick={nextPage} disabled={currentPage === Math.ceil(filteredTasks.length / tasksPerPage)}>Next</button>
            </div>
          </>
        )}
      </section>
    </div>
  );
};

export default TaskList;
