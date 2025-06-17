from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import Admin

main = Blueprint('main', __name__)
user = Blueprint('user', __name__, url_prefix='/user')
admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash('You need to be logged in as an admin to view this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    if current_user.is_authenticated:
        if isinstance(current_user, Admin):
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    return render_template('index.html')

@user.route('/dashboard')
@login_required
def user_dashboard():
    if isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))
    return render_template('user/dashboard.html')

@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')