# development.py

import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URI = 'sqlite:///testing.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///production.db'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///production.db'