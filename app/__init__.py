from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import User, Admin
    # Try to load user first
    user = User.query.get(int(user_id))
    if user:
        return user
    # If not found, try admin
    return Admin.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Change this to a secure random key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enhanced security settings
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # Session timeout
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'  # Enable strong session protection

    from .routes import main, user, admin
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    with app.app_context():
        # Create all tables
        db.create_all()

        # Import and check for default admin
        from .models import Admin
        try:
            if not Admin.query.filter_by(username='admin').first():
                admin = Admin(username='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            print(f"[ERROR] Could not create default admin: {e}")

    return app


def initialize_admin():
    from .models import Admin
    if not Admin.query.first():
        admin = Admin(username="admin")
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
