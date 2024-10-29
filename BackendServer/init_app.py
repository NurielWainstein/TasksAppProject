import os
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_compress import Compress
from dotenv import load_dotenv

from BackendServer.apis.tasks import tasks_ns

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Basic configurations using environment variables
    app.config["COMPRESS_LEVEL"] = int(os.getenv("COMPRESS_LEVEL", 6))
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # Max upload size of 64MB

    # Initialize services(allow front functionality)
    Compress(app)
    CORS(app)

    # Initialize and manage the API and register namespaces
    api = Api(
        app,
        version="1.0",
        title="Task API",
        description="A simple Task API",
        doc="/"
    )
    api.add_namespace(tasks_ns, path='/tasks')

    return app

if __name__ == "__main__":
    # Run the Flask application
    application = create_app()
    port = int(os.getenv("APP_PORT", 5000))
    application.run(host="0.0.0.0", port=port, threaded=True)
