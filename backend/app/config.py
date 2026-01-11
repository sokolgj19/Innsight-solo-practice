"""
Flask application configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = 'innsight_db'
    
    # API
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}