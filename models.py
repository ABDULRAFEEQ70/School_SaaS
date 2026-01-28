from flask_sqlalchemy import SQLAlchemy
from flask_tenants import TenantMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Tenant Model for multi-tenancy
class Tenant(TenantMixin, db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    schema_name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tenant {self.name}>"

# User Model
class User(db.Model):
    __tablename__ = 'users'
    USER_TYPE_CHOICES = [
        (1, 'admin'),
        (2, 'teacher'),
        (3, 'student'),
        (4, 'parent'),
        (5, 'staff'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_type = db.Column(db.Integer, default=3)  # Default: student
    phone = db.Column(db.String(15))
    profile_pic = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

# Student Model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    current_class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

    user = db.relationship('User', backref='student_profile')
    current_class = db.relationship('Class', backref='students')
    parents = db.relationship('User', secondary='student_parents', backref='children')

    # Proxy properties to access linked User fields directly from Student
    @property
    def first_name(self):
        return self.user.first_name if self.user else None

    @property
    def last_name(self):
        return self.user.last_name if self.user else None

    @property
    def email(self):
        return self.user.email if self.user else None

# Course Model
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

    def __repr__(self):
        return f"<Course {self.name}>"

# Class Model
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

    course = db.relationship('Course', backref='classes')
    teacher = db.relationship('User', backref='teaching_classes')
    # Optional schedule field
    schedule = db.Column(db.String(255))

# Attendance Model
class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), default='present')  # present, absent, late
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

    student = db.relationship('Student', backref='attendance_records')
    class_record = db.relationship('Class', backref='attendance')

# Grade Model
class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    grade = db.Column(db.Float)
    term = db.Column(db.String(20))  # e.g., "Fall 2023"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

    student = db.relationship('Student', backref='grades')
    course = db.relationship('Course', backref='grades')

    @property
    def value(self):
        return self.grade

# Association table for student-parents relationship
student_parents = db.Table('student_parents',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('parent_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
