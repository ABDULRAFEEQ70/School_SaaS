from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config


from models import db

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)


from routes import (
    auth_bp, students_bp, courses_bp,
    classes_bp, attendance_bp, grades_bp
)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(students_bp, url_prefix='/api/students')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(classes_bp, url_prefix='/api/classes')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(grades_bp, url_prefix='/api/grades')

# Celery setup
from celery import Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if __name__ == '__main__':
    app.run(debug=True)
