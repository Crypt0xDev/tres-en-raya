# production.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///production.db'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Add any other production-specific configurations here

# You can add more classes for different configurations if needed
