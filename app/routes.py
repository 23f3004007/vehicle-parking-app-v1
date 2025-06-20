from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import Admin
from flask import request, jsonify
from .models import ParkingLot, ParkingSpot, User, db

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
            return redirect(url_for('admin.admin_dashboard'))  # Change from 'admin.dashboard' to 'admin.admin_dashboard'
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


@admin.route('/lots')
@admin_required
def manage_lots():
    lots = ParkingLot.query.all()
    return render_template('admin/lots.html', lots=lots)

@admin.route('/lots/create', methods=['GET', 'POST'])
@admin_required
def create_lot():
    if request.method == 'POST':
        lot = ParkingLot(
            prime_location_name=request.form['name'],
            address=request.form['address'],
            pin_code=request.form['pin_code'],
            price_per_hour=float(request.form['price_per_hour']),
            max_spots=int(request.form['max_spots'])
        )
        db.session.add(lot)
        
        # Create parking spots based on max_spots
        for _ in range(lot.max_spots):
            spot = ParkingSpot(lot=lot)
            db.session.add(spot)
            
        db.session.commit()
        flash('Parking lot created successfully!', 'success')
        return redirect(url_for('admin.manage_lots'))
    return render_template('admin/lot_form.html')

@admin.route('/lots/<int:lot_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.prime_location_name = request.form['name']
        lot.address = request.form['address']
        lot.pin_code = request.form['pin_code']
        lot.price_per_hour = float(request.form['price_per_hour'])
        db.session.commit()
        flash('Parking lot updated successfully!', 'success')
        return redirect(url_for('admin.manage_lots'))
    return render_template('admin/lot_form.html', lot=lot)

@admin.route('/lots/<int:lot_id>/delete', methods=['POST'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted successfully!', 'success')
    return redirect(url_for('admin.manage_lots'))

@admin.route('/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/lots/<int:lot_id>/details')
@admin_required
def lot_details(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    return render_template('admin/lot_details.html', lot=lot)

@admin.route('/users/<int:user_id>/details')
@admin_required
def view_user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_details.html', user=user)