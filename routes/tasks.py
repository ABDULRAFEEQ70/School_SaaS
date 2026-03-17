from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from utils import success_response, error_response


# The tasks blueprint only deals with queuing and checking Celery jobs.
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/test-email', methods=['POST'])
@jwt_required()
def test_email_task():
    """Queue a test email notification task."""
    from tasks import send_email_notification
    from app import celery

    if not celery:
        return error_response('Celery not configured', 503)

    data = request.get_json() or {}
    recipient = data.get('recipient', 'test@example.com')
    subject = data.get('subject', 'Test Email')
    body = data.get('body', 'This is a test email sent via Celery!')

    result = send_email_notification.delay(recipient, subject, body)
    return success_response({
        'message': 'Email task queued successfully',
        'task_id': result.id,
        'recipient': recipient
    })


@tasks_bp.route('/task-status/<task_id>', methods=['GET'])
@jwt_required()
def get_task_status(task_id):
    """Return the state and result of a previously queued task."""
    from app import celery
    if not celery:
        return error_response('Celery not configured', 503)

    result = celery.AsyncResult(task_id)
    response = {
        'task_id': task_id,
        'status': result.status,
        'current': result.info if result.state == 'PROGRESS' else None
    }
    if result.ready():
        response['result'] = result.result
    return success_response(response)


@tasks_bp.route('/test-report', methods=['POST'])
@jwt_required()
def test_report_task():
    """Queue a report generation task."""
    from tasks import generate_report
    from app import celery

    if not celery:
        return error_response('Celery not configured', 503)

    data = request.get_json() or {}
    report_type = data.get('report_type', 'summary')
    parameters = data.get('parameters', {})

    result = generate_report.delay(report_type, parameters)
    return success_response({
        'message': 'Report generation task queued successfully',
        'task_id': result.id,
        'report_type': report_type
    })