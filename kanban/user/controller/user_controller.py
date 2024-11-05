from flask import Blueprint
from kanban.user.view.user_view import login, get_user, create_user, update_user, delete_user
from kanban.utils import required_fields

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/session', methods=['POST'])
@required_fields('email', 'password')
def login_view():
    return login()

@user_bp.route('/user/<id>', methods=['GET'])
def get_user_view(id):
    return get_user(id)

@user_bp.route('/user', methods=['POST'])
@required_fields('name', 'email', 'password')
def create_user_view():
    return create_user()

@user_bp.route('/user/<id>', methods=['PATCH'])
@required_fields('name', 'password', 'email')
def update_user_view(id):
    return update_user(id)

@user_bp.route('/user/<id>', methods=['DELETE'])
def delete_user_view(id):
    return delete_user(id)