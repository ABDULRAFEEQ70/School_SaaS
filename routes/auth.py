from flask import Blueprint, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from typing import cast
from models import User
from services import AuthService
from utils import success_response, error_response, admin_required


auth_bp = Blueprint('auth', __name__)


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
    return success_response({'users': [
        {
            'id': u.id,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'user_type': u.user_type
        } for u in users
    ]})


@auth_bp.route('/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    result = AuthService.delete_user(user_id)
    if result:
        return success_response({'message': 'User deleted successfully'})
    return error_response('User not found', 404)
