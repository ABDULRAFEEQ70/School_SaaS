from celery import Celery
from config import Config

# Create Celery instance (the core object; configuration may be expanded later)
celery = Celery(
    'school_saas',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=['tasks']
)

# Base configuration; will be merged with Flask config when bound
celery.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Optional: Configure Celery Beat for periodic tasks
celery.conf.beat_schedule = {
    # Example periodic task - runs every 10 minutes
    # 'check-system-health': {
    #     'task': 'tasks.check_system_health',
    #     'schedule': 600.0,  # 10 minutes
    # },
}


def make_celery(flask_app):
    """Create a new Celery object attached to the Flask app's context.

    This helper copies configuration from the application and ensures tasks
    execute within the application context so that they can access extensions
    such as the database.
    """
    celery.conf.update(flask_app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# Import tasks to register them
import tasks