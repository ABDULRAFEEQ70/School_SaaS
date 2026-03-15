from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from tasks import celery
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Register blueprints
from routes import (
    auth_bp,
    students_bp,
    courses_bp,
    classes_bp,
    attendance_bp,
    grades_bp,
    tasks_bp,
)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(students_bp, url_prefix='/api/students')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(classes_bp, url_prefix='/api/classes')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(grades_bp, url_prefix='/api/grades')
app.register_blueprint(tasks_bp, url_prefix='/api/tasks')

# Celery setup (optional - only if CELERY_BROKER_URL is configured)
celery = None
if os.getenv('CELERY_BROKER_URL'):
    try:
        from celery_app import make_celery
        celery = make_celery(app)
        print("Celery initialized successfully")
    except Exception as e:
        print(f"WARNING: Celery initialization failed: {e}")
        print("  Running without async task support")
else:
    print("INFO: Celery not configured (CELERY_BROKER_URL not set)")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    from utils import error_response
    return error_response('Resource not found', 404)

@app.errorhandler(500)
def internal_error(error):
    from utils import error_response
    db.session.rollback()
    return error_response('Internal server error', 500)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    from utils import success_response
    return success_response({'status': 'healthy', 'message': 'School SaaS API is running'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables exist on startup
    app.run(debug=True, host='0.0.0.0', port=5000)
