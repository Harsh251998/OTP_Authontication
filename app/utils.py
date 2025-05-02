import random
import time
from datetime import datetime, timedelta
from twilio.rest import Client
import jwt
from extensions import db
from .models import User
from flask_jwt_extended import create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

def send_otp_via_sms(phone, otp):
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    if not twilio_sid or not twilio_auth_token or not twilio_phone_number:
        raise ValueError("Twilio credentials are not set in the environment variables.")
    
    twilio_client = Client(twilio_sid, twilio_auth_token)
    twilio_client.messages.create(
        body=f"Your OTP is {otp}",
        from_=twilio_phone_number,  
        to=phone
    )
    
    return otp

def generate_jwt_token(user_id, role):
    token = create_access_token(identity=user_id, additional_claims={"role": role})
    return token

def verify_otp_validity(user):
    otp_expiry_time = user.otp_created_at + timedelta(minutes=5)
    if datetime.now() > otp_expiry_time:
        return False
    return True
