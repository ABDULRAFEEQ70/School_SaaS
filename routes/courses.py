from flask import Blueprint, request
from typing import cast
from models import Course
from services import CourseService
from utils import success_response, error_response, admin_required

courses_bp = Blueprint('courses', __name__)


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
