from flask import Blueprint, request
from typing import cast
from models import Grade
from services import GradeService
from utils import success_response, error_response, admin_required

grades_bp = Blueprint('grades', __name__)


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
