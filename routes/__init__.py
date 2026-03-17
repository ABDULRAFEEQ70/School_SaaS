"""Package initializer for route blueprints."""
# import and re-export blueprints so the top-level `routes` module behaves
# much like the previous single-file module.

from .auth import auth_bp
from .students import students_bp
from .courses import courses_bp
from .classes import classes_bp
from .attendance import attendance_bp
from .grades import grades_bp
from .tasks import tasks_bp

__all__ = [
    'auth_bp',
    'students_bp',
    'courses_bp',
    'classes_bp',
    'attendance_bp',
    'grades_bp',
    'tasks_bp',
]
