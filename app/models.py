from extensions import db  

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    otp = db.Column(db.String(6))
    otp_created_at = db.Column(db.DateTime)
    role = db.Column(db.String(50), default="user")
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


    def __repr__(self):
        return f'<User {self.email}>'
