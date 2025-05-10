import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    # Construct database URL from environment variables or use DATABASE_URL if provided
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    
    SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "mysecretkey"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "mysecretkey"
    ENV = os.getenv("FLASK_ENV", "development")

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"

class TestingConfig(Config):
    TESTING = True
    ENV = "testing"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
