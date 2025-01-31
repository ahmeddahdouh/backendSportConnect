import os
from dotenv import load_dotenv
load_dotenv()



class Config:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'mysecretkey'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'mysecretkey'






