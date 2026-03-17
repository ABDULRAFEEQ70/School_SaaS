from flask import Blueprint, request
from typing import cast
from models import Attendance
from services import AttendanceService
from utils import success_response, error_response, admin_required

attendance_bp = Blueprint('attendance', __name__)


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
