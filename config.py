import os


class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'mysecretkey'

