import os

# Load .env files when available (optional dependency)
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()


class Config:
    """
    Flask configuration class that reads from environment variables.
    Sensible defaults are provided for local development.
    """
    
    # Core Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 
        'sqlite:///data.db'  # SQLite for local development
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT (JSON Web Tokens)
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY', 
        os.getenv('SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    )
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour

    # CORS (Cross-Origin Resource Sharing)
    CORS_HEADERS = 'Content-Type'
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:3000,http://localhost:5000,http://localhost:8000'
    )

    # Celery Configuration (async task queue - optional)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'UTC'


# Convenience module-level variables for external use
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-mini')

