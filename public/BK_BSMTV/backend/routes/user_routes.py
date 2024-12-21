from flask import Blueprint, jsonify, request
from backend.services.user_service import UserService

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    return jsonify(users), 200

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = UserService.create_user(data)
    return jsonify(user), 201

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    updated_user = UserService.update_user(user_id, data)
    if updated_user:
        return jsonify(updated_user), 200
    return jsonify({'message': 'User not found'}), 404

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted'}), 204
    return jsonify({'message': 'User not found'}), 404