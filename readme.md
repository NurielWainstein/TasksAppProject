# Project Overview

This README provides general explanations and clarifications about the project setup, 
both for the backend and frontend components.

The App provides an easy to use task managment application and api.

## General Setup
0. **Set up venv**
    you can use this tutorial: https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env

1. **Install Python Dependencies**
   - Run the following command to install all necessary packages:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up Frontend Dependencies**
   - Navigate to the `task-manager` directory (the frontend app) and run:
     ```bash
     npm install
     ```
   - This command installs the required JavaScript packages.

3. **Optional Configure Source Directory**
   - Mark the parent folder (`tasksapp`) as the source directory to avoid import issues.

4. **Optional Environment Configuration**
   - Add the environment path to your environment variables:
     ```
     ;ENV_FILE=.env
     ```

## Backend Setup

- To start the backend server, run:
  ```bash
  python init_app.py
  ```
- This will create a server that runs the API and provides access to Swagger documentation for API endpoints.

## Frontend Setup

- Navigate to the React frontend app using:
  ```bash
  cd task-manager
  ```
- Start the frontend application with:
  ```bash
  npm start
  ```

## Important Note

- Ensure both the backend and frontend servers are running simultaneously for proper functionality.