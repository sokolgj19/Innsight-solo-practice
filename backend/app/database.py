"""
MongoDB database connection for Flask
"""

from pymongo import MongoClient
from flask import current_app, g


def get_db():
    """
    Get database connection.
    Creates a new connection if one doesn't exist for this request.
    """
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client[current_app.config['DB_NAME']]
        g.client = client
    
    return g.db


def close_db(e=None):
    """Close database connection."""
    client = g.pop('client', None)
    
    if client is not None:
        client.close()


def init_app(app):
    """Initialize database with Flask app."""
    app.teardown_appcontext(close_db)