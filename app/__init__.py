from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'veditharv'  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = True 
    app.config['SESSION_COOKIE_HTTPONLY'] = True 
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60) 
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'

    from .routes import main, user, admin
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()
        from .models import User
        try:
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin')
                admin.set_password('admin123')
                admin.is_admin=True
                admin.email = 'admin@example.com'
                admin.full_name = 'Admin'
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            print(f"[ERROR] Could not create default admin: {e}")

    return app
