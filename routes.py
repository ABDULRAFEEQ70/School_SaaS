from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from typing import cast, Any
from models import User, Student, Course, Class, Attendance, Grade
from services import (
    AuthService, StudentService, CourseService,
    ClassService, AttendanceService, GradeService
)
from utils import (
    success_response, error_response,
    admin_required, teacher_required
)
import os
try:
    import openai
except Exception:
    openai: Any = None
from config import OPENAI_API_KEY, OPENAI_MODEL
try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv():
        return None

# Load environment variables from .env file
load_dotenv()

# Create blueprints
auth_bp = Blueprint('auth', __name__)
students_bp = Blueprint('students', __name__)
courses_bp = Blueprint('courses', __name__)
classes_bp = Blueprint('classes', __name__)
attendance_bp = Blueprint('attendance', __name__)
grades_bp = Blueprint('grades', __name__)

openai.api_key = OPENAI_API_KEY

def call_model(messages):
    model = OPENAI_MODEL
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    return resp

# Auth Routes
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = AuthService.register_user(data)
    if isinstance(user, tuple):  # If it's an error response
        return user
    user = cast(User, user)
    return success_response({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type
        }
    }, 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return error_response('Email and password are required', 400)
    user = AuthService.authenticate_user(email, password)
    if not user:
        return error_response('Invalid credentials', 401)
    access_token = create_access_token(identity=user.id)
    return success_response({
        'message': 'User logged in successfully',
        'access_token': access_token
    })

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # Get JWT ID
    AuthService.blacklist_token(jti)
    return success_response({'message': 'User logged out successfully'})


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return success_response({
        'message': 'Token refreshed successfully',
        'access_token': access_token
    })

@auth_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    users = AuthService.get_all_users()
    return success_response({
        'users': [{
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type
        } for user in users]
    })

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = AuthService.get_user_by_id(user_id)
    if not user:
        return error_response('User not found', 404)
    user = cast(User, user)
    return success_response({
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type
        }
    })

@auth_bp.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = AuthService.update_user(current_user_id, data)
    if isinstance(user, tuple):  # If it's an error response
        return user
    user = cast(User, user)
    return success_response({
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type
        }
    })

@auth_bp.route('/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    result = AuthService.delete_user(user_id)
    if result:
        return success_response({'message': 'User deleted successfully'})
    return error_response('User not found', 404)

@auth_bp.route('/students', methods=['POST'])
@admin_required
def create_student():
    data = request.get_json()
    student = StudentService.create_student(data)
    if isinstance(student, tuple):  # If it's an error response
        return student
    student = cast(Student, student)
    return success_response({
        'message': 'Student created successfully',
        'student': {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': getattr(student, 'last_name', None),
            'email': student.email
        }
    }, 201)

@students_bp.route('/students', methods=['GET'])
@admin_required
def get_all_students():
    students = StudentService.get_all_students()
    return success_response({
        'students': [{
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email
        } for student in students]
    })

@students_bp.route('/student/<int:student_id>', methods=['GET'])
@admin_required
def get_student(student_id):
    student = StudentService.get_student_by_id(student_id)
    if not student:
        return error_response('Student not found', 404)
    student = cast(Student, student)
    return success_response({
        'student': {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email
        }
    })

@students_bp.route('/student', methods=['PUT'])
@admin_required
def update_student():
    data = request.get_json() or {}
    student_id = data.get('id') or data.get('student_id')
    if not student_id:
        return error_response('student_id is required', 400)
    student = StudentService.update_student(student_id, data)
    if isinstance(student, tuple):  # If it's an error response
        return student
    student = cast(Student, student)
    return success_response({
        'message': 'Student updated successfully',
        'student': {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email
        }
    })

@students_bp.route('/student/<int:student_id>', methods=['DELETE'])
@admin_required
def delete_student(student_id):
    result = StudentService.delete_student(student_id)
    if result:
        return success_response({'message': 'Student deleted successfully'})
    return error_response('Student not found', 404)

@courses_bp.route('/courses', methods=['POST'])
@admin_required
def create_course():
    data = request.get_json()
    course = CourseService.create_course(data)
    if isinstance(course, tuple):  # If it's an error response
        return course
    course = cast(Course, course)
    return success_response({
        'message': 'Course created successfully',
        'course': {
            'id': course.id,
            'name': course.name,
            'description': course.description
        }
    }, 201)

@courses_bp.route('/courses', methods=['GET'])
@admin_required
def get_all_courses():
    courses = CourseService.get_all_courses()
    return success_response({
        'courses': [{
            'id': course.id,
            'name': course.name,
            'description': course.description
        } for course in courses]
    })

@courses_bp.route('/course/<int:course_id>', methods=['GET'])
@admin_required
def get_course(course_id):
    course = CourseService.get_course_by_id(course_id)
    if not course:
        return error_response('Course not found', 404)
    course = cast(Course, course)
    return success_response({
        'course': {
            'id': course.id,
            'name': course.name,
            'description': course.description
        }
    })

@courses_bp.route('/course', methods=['PUT'])
@admin_required
def update_course():
    data = request.get_json()
    course = CourseService.update_course(data)
    if isinstance(course, tuple):  # If it's an error response
        return course
    course = cast(Course, course)
    return success_response({
        'message': 'Course updated successfully',
        'course': {
            'id': course.id,
            'name': course.name,
            'description': course.description
        }
    })

@courses_bp.route('/course/<int:course_id>', methods=['DELETE'])
@admin_required
def delete_course(course_id):
    result = CourseService.delete_course(course_id)
    if result:
        return success_response({'message': 'Course deleted successfully'})
    return error_response('Course not found', 404)

@classes_bp.route('/classes', methods=['POST'])
@admin_required
def create_class():
    data = request.get_json()
    class_ = ClassService.create_class(data)
    if isinstance(class_, tuple):  # If it's an error response
        return class_
    class_ = cast(Class, class_)
    return success_response({
        'message': 'Class created successfully',
        'class': {
            'id': class_.id,
            'course_id': class_.course_id,
            'teacher_id': class_.teacher_id,
            'schedule': class_.schedule
        }
    }, 201)

@classes_bp.route('/classes', methods=['GET'])
@admin_required
def get_all_classes():
    classes = ClassService.get_all_classes()
    return success_response({
        'classes': [{
            'id': class_.id,
            'course_id': class_.course_id,
            'teacher_id': class_.teacher_id,
            'schedule': class_.schedule
        } for class_ in classes]
    })

@classes_bp.route('/class/<int:class_id>', methods=['GET'])
@admin_required
def get_class(class_id):
    class_ = ClassService.get_class_by_id(class_id)
    if not class_:
        return error_response('Class not found', 404)
    class_ = cast(Class, class_)
    return success_response({
        'class': {
            'id': class_.id,
            'course_id': class_.course_id,
            'teacher_id': class_.teacher_id,
            'schedule': class_.schedule
        }
    })

@classes_bp.route('/class', methods=['PUT'])
@admin_required
def update_class():
    data = request.get_json()
    class_ = ClassService.update_class(data)
    if isinstance(class_, tuple):  # If it's an error response
        return class_
    class_ = cast(Class, class_)
    return success_response({
        'message': 'Class updated successfully',
        'class': {
            'id': class_.id,
            'course_id': class_.course_id,
            'teacher_id': class_.teacher_id,
            'schedule': class_.schedule
        }
    })

@classes_bp.route('/class/<int:class_id>', methods=['DELETE'])
@admin_required
def delete_class(class_id):
    result = ClassService.delete_class(class_id)
    if result:
        return success_response({'message': 'Class deleted successfully'})
    return error_response('Class not found', 404)

@attendance_bp.route('/attendance', methods=['POST'])
@admin_required
def create_attendance():
    data = request.get_json()
    attendance = AttendanceService.create_attendance(data)
    if isinstance(attendance, tuple):  # If it's an error response
        return attendance
    attendance = cast(Attendance, attendance)
    return success_response({
        'message': 'Attendance record created successfully',
        'attendance': {
            'id': attendance.id,
            'class_id': attendance.class_id,
            'student_id': attendance.student_id,
            'status': attendance.status
        }
    }, 201)

@attendance_bp.route('/attendance', methods=['GET'])
@admin_required
def get_all_attendance():
    attendance_records = AttendanceService.get_all_attendance()
    return success_response({
        'attendance': [{
            'id': attendance.id,
            'class_id': attendance.class_id,
            'student_id': attendance.student_id,
            'status': attendance.status
        } for attendance in attendance_records]
    })

@attendance_bp.route('/attendance/<int:attendance_id>', methods=['GET'])
@admin_required
def get_attendance(attendance_id):
    attendance = AttendanceService.get_attendance_by_id(attendance_id)
    if not attendance:
        return error_response('Attendance record not found', 404)
    attendance = cast(Attendance, attendance)
    return success_response({
        'attendance': {
            'id': attendance.id,
            'class_id': attendance.class_id,
            'student_id': attendance.student_id,
            'status': attendance.status
        }
    })

@attendance_bp.route('/attendance', methods=['PUT'])
@admin_required
def update_attendance():
    data = request.get_json()
    attendance = AttendanceService.update_attendance(data)
    if isinstance(attendance, tuple):  # If it's an error response
        return attendance
    attendance = cast(Attendance, attendance)
    return success_response({
        'message': 'Attendance record updated successfully',
        'attendance': {
            'id': attendance.id,
            'class_id': attendance.class_id,
            'student_id': attendance.student_id,
            'status': attendance.status
        }
    })

@attendance_bp.route('/attendance/<int:attendance_id>', methods=['DELETE'])
@admin_required
def delete_attendance(attendance_id):
    result = AttendanceService.delete_attendance(attendance_id)
    if result:
        return success_response({'message': 'Attendance record deleted successfully'})
    return error_response('Attendance record not found', 404)

@grades_bp.route('/grades', methods=['POST'])
@admin_required
def create_grade():
    data = request.get_json()
    grade = GradeService.create_grade(data)
    if isinstance(grade, tuple):  # If it's an error response
        return grade
    grade = cast(Grade, grade)
    return success_response({
        'message': 'Grade record created successfully',
        'grade': {
            'id': grade.id,
            'student_id': grade.student_id,
            'course_id': grade.course_id,
            'value': grade.value
        }
    }, 201)

@grades_bp.route('/grades', methods=['GET'])
@admin_required
def get_all_grades():
    grades = GradeService.get_all_grades()
    return success_response({
        'grades': [{
            'id': grade.id,
            'student_id': grade.student_id,
            'course_id': grade.course_id,
            'value': grade.value
        } for grade in grades]
    })

@grades_bp.route('/grade/<int:grade_id>', methods=['GET'])
@admin_required
def get_grade(grade_id):
    grade = GradeService.get_grade_by_id(grade_id)
    if not grade:
        return error_response('Grade record not found', 404)
    grade = cast(Grade, grade)
    return success_response({
        'grade': {
            'id': grade.id,
            'student_id': grade.student_id,
            'course_id': grade.course_id,
            'value': grade.value
        }
    })

@grades_bp.route('/grade', methods=['PUT'])
@admin_required
def update_grade():
    data = request.get_json()
    grade = GradeService.update_grade(data)
    if isinstance(grade, tuple):  # If it's an error response
        return grade
    grade = cast(Grade, grade)
    return success_response({
        'message': 'Grade record updated successfully',
        'grade': {
            'id': grade.id,
            'student_id': grade.student_id,
            'course_id': grade.course_id,
            'value': grade.value
        }
    })

@grades_bp.route('/grade/<int:grade_id>', methods=['DELETE'])
@admin_required
def delete_grade(grade_id):
    result = GradeService.delete_grade(grade_id)
    if result:
        return success_response({'message': 'Grade record deleted successfully'})
    return error_response('Grade record not found', 404)
