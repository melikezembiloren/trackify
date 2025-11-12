from flask import Blueprint, request, jsonify, render_template
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('auth.html')

@auth_bp.route('/login/user', methods=['POST'])

def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    return AuthService.auth_with_username(username, password)


@auth_bp.route('/login/line', methods=['POST'])
def authWithLine():
    data = request.get_json()
    linename = data.get('linename')
    password = data.get('password')


    return AuthService.auth_with_line_name(linename, password)


 