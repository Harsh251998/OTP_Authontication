from flask import Flask
from app.routes import auth_bp  
from extensions import db, jwt  
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
