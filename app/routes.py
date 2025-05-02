import random
from flask import Blueprint, request, jsonify
from extensions import db  
from app.models import User
from app.utils import send_otp_via_sms, generate_jwt_token, verify_otp_validity
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime,timedelta
import secrets



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered."}), 400

    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        password=data.get('password')  
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    
    if not data or 'phone' not in data:
        return jsonify({'error': 'Phone number is required'}), 400

    phone = data['phone']


    user = User.query.filter_by(phone=phone).first()

    otp = str(random.randint(1000, 9999))  
    otp_created_at = datetime.now() 

    if user:
        user.otp = otp
        user.otp_created_at = otp_created_at
    else:
        new_user = User(phone=phone, otp=otp, otp_created_at=otp_created_at)
        db.session.add(new_user)

    db.session.commit()

    send_otp_via_sms(phone, otp)

    return jsonify({'message': 'OTP sent successfully!'}), 200


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()

    user = User.query.filter_by(phone=data['phone']).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not user.otp:
        return jsonify({'message': 'OTP not sent yet. Please request OTP.'}), 400

    if not verify_otp_validity(user.otp_created_at):
        return jsonify({'message': 'OTP expired. Please request a new OTP.'}), 400

    if user.otp != data['otp']:
        return jsonify({'message': 'Invalid OTP'}), 400

    token = generate_jwt_token(user.id)

    user.otp = None
    user.otp_created_at = None
    db.session.commit()

    return jsonify({'message': 'OTP verified successfully!', 'token': token}), 200


@auth_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.now() + timedelta(minutes=30)
    db.session.commit()

    return jsonify({"message": "Reset token generated", "reset_token": reset_token}), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"message": "Invalid or expired token"}), 400

    user.password = new_password
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({"message": "Password reset successfully"}), 200


@auth_bp.route('/update-account', methods=['PUT'])
@jwt_required()
def update_account():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone = data.get('phone', user.phone)
    user.password = data.get('password', user.password)

    db.session.commit()

    return jsonify({"message": "Account information updated successfully"}), 200
