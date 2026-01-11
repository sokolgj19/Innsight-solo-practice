"""
Flask application factory
"""

from flask import Flask
from flask_cors import CORS
from .config import config
from . import database


def create_app(config_name='development'):
    """
    Create and configure Flask application.
    
    Args:
        config_name: Configuration to use ('development', 'production')
    
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions - Allow all origins for development
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": False,
            "max_age": 3600
        }
    })
    database.init_app(app)
    
    # Register blueprints
    from .routes import analytics, listings
    app.register_blueprint(analytics.bp)
    app.register_blueprint(listings.bp)
    
    # Health check endpoint
    @app.route('/')
    def index():
        return {
            'status': 'ok',
            'message': 'InnSight API is running',
            'version': '1.0.0'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app