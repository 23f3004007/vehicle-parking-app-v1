from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify the login view

    # Register blueprints
    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    with app.app_context():
        from .models import Admin, User, ParkingLot, ParkingSpot, Reservation
        db.create_all()
        initialize_admin()
    return app

def initialize_admin():
    from .models import Admin
    if not Admin.query.first():
        admin = Admin(username="admin")
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
