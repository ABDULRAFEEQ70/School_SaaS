from flask import jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User, Tenant
from flask_tenants import current_tenant

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
    return current_tenant._get_current_object() if current_tenant else None

def init_tenants(app):
    """Initialize multi-tenancy"""
    from flask_tenants import TenantManager
    tenant_manager = TenantManager(app)

    @tenant_manager.tenant_resolver
    def tenant_resolver(request):
        tenant_schema = request.headers.get('X-Tenant-ID')
        if not tenant_schema:
            return None
        return Tenant.query.filter_by(schema_name=tenant_schema).first()

    return tenant_manager
