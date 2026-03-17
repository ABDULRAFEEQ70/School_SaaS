from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User, Tenant

def success_response(data, status_code=200):
    """Standardized success response"""
    return jsonify({
        'success': True,
        'data': data
    }), status_code

def error_response(message, status_code=400):
    """Standardized error response"""
    return jsonify({
        'success': False,
        'error': message
    }), status_code

def admin_required(fn):
    """Decorator to restrict access to admins"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.user_type != 1:
            return error_response('Admin access required', 403)
        return fn(*args, **kwargs)
    return wrapper

def teacher_required(fn):
    """Decorator to restrict access to teachers and admins"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.user_type not in [1, 2]:
            return error_response('Teacher access required', 403)
        return fn(*args, **kwargs)
    return wrapper

def get_current_tenant():
    """Get the current tenant from the request"""
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        return None
    try:
        return Tenant.query.get(int(tenant_id))
    except (ValueError, TypeError):
        return None

def init_tenants(app):
    """Initialize multi-tenancy (basic implementation)"""
    # This is a basic initialization for multi-tenancy support
    # For production, consider using a dedicated library
    return True
