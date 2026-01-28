import os
from dotenv import load_dotenv

# Load .env files when available
load_dotenv()


class Config:
    # Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY', 'change-me'))
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # seconds

    # CORS
    CORS_HEADERS = 'Content-Type'

    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')


# Convenience module-level variables for simple imports
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-5-mini')

