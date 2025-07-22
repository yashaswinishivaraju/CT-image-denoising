import os
from flask import Flask

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Configure upload folder and secret key (for sessions, if needed later)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
    app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key if using sessions

    # Register routes
    with app.app_context():
        from . import main
        app.register_blueprint(main.bp)

    return app
