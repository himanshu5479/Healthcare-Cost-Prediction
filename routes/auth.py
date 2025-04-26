from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user_models import User

auth = Blueprint('auth', __name__)


# Signup Route 
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data received or invalid JSON"}), 400

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    if not all([email, username, password, confirmPassword]):
        return jsonify({"status": "error", "message": "Please fill in all fields"}), 400
    if password != confirmPassword:
        return jsonify({"status": "error", "message": "Passwords do not match"}), 400
    if '@' not in email:
        return jsonify({"status": "error", "message": "Invalid email address"}), 400

    if User.find_by_email(email):
        return jsonify({"status": "error", "message": "Email already exists"}), 400

    new_user = User(email=email, username=username, password=password)
    new_user.save()

    return jsonify({
        "status": "success",
        "message": "Signup successful",
        "data": {
            "username": username,
            "email": email
        }
    }), 201


# Login Route

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data received or invalid JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Please provide both email and password"}), 400

    user = User.find_by_email(email)
    if user and user.check_password(password):
        token = create_access_token(identity=email)
        return jsonify({
            "status": "success",
            "token": token  
        }), 200

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401
