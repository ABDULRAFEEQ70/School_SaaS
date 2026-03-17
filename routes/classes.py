from flask import Blueprint, request
from typing import cast
from models import Class
from services import ClassService
from utils import success_response, error_response, admin_required

classes_bp = Blueprint('classes', __name__)


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
