from flask import Blueprint, request
from typing import cast
from models import Student
from services import StudentService
from utils import success_response, error_response, admin_required

students_bp = Blueprint('students', __name__)


@students_bp.route('/students', methods=['POST'])
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
