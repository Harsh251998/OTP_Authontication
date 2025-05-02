This project demonstrates a Flask-based OTP authentication system integrated with Twilio for SMS-based OTP delivery and JWT for secure authentication. It also includes basic user registration, OTP generation, and verification.

Requirements
Python 3.x
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Twilio (for OTP via SMS)
dotenv (for environment variable management)

cloning of repo

git clone <your-repository-url>
cd OTP_Authentication

python3 -m venv venv
venv\Scripts\activate  

install requirement.txt
pip install -r requirements.txt

setup the .env file with your configurations

and run
python main.py 

