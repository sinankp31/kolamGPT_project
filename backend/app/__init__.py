from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from config import config

# Initialize Flask-Mail extension
mail = Mail()

def create_app(config_name='default'):
    """
    Application factory. This function is responsible for creating and
    configuring the Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from the config object based on the provided name
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Enable Cross-Origin Resource Sharing (CORS). This is essential
    # to allow your React frontend to make requests to this backend.
    CORS(app)

    # Initialize Flask-Mail with the app
    mail.init_app(app)

    # Import and register the API blueprint with the application.
    # We import it here to avoid circular dependency issues.
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app