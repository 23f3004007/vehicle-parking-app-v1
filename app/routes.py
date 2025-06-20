from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import Admin
from flask import request, jsonify
from .models import ParkingLot, ParkingSpot, User, db
from datetime import datetime
from .models import Reservation

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
        return redirect(url_for('user.user_dashboard'))
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


@user.route('/parking-lots')
@login_required
def view_parking_lots():
    lots = ParkingLot.query.all()
    return render_template('user/parking_lots.html', lots=lots)

@user.route('/reserve/<int:lot_id>', methods=['POST'])
@login_required
def reserve_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    # Find first available spot using the correct status field
    available_spot = next((spot for spot in lot.spots if spot.status == 'A'), None)
    
    if not available_spot:
        flash('No spots available in this lot.', 'error')
        return redirect(url_for('user.view_parking_lots'))
    
    # Create reservation and explicitly set spot_id
    reservation = Reservation(
        user_id=current_user.id,
        spot_id=available_spot.id,  # Explicitly set spot_id
        parking_time=datetime.utcnow(),
        cost_per_hour=lot.price_per_hour
    )
    available_spot.status = 'O'  # Update status to Occupied
    
    db.session.add(reservation)
    db.session.commit()
    
    flash('Spot reserved successfully!', 'success')
    return redirect(url_for('user.view_reservations'))

@user.route('/release/<int:reservation_id>', methods=['POST'])
@login_required
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    
    if reservation.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('user.view_reservations'))
    
    reservation.leaving_time = datetime.utcnow()
    reservation.spot.status = 'A'  # Update status to Available
    db.session.commit()
    
    flash(f'Parking spot released. Total cost: ${reservation.calculate_total_cost()}', 'success')
    return redirect(url_for('user.view_reservations'))

@user.route('/reservations')
@login_required
def view_reservations():
    return render_template('user/reservations.html', 
                         reservations=current_user.reservations,
                         now=datetime.utcnow)

@user.route('/history')
@login_required
def parking_history():
    completed_reservations = Reservation.query.filter_by(
        user_id=current_user.id
    ).filter(
        Reservation.leaving_time.isnot(None)
    ).order_by(Reservation.parking_time.desc()).all()
    return render_template('user/history.html', reservations=completed_reservations)


@admin.route('/reservations')
@admin_required
def view_all_reservations():
    # Get all reservations with user and spot information
    reservations = Reservation.query.order_by(Reservation.parking_time.desc()).all()
    return render_template('admin/reservations.html', reservations=reservations)

@admin.route('/reports')
@admin_required
def view_reports():
    # Get statistics for the reports
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    total_users = User.query.count()
    active_reservations = Reservation.query.filter(Reservation.leaving_time.is_(None)).count()
    completed_reservations = Reservation.query.filter(Reservation.leaving_time.isnot(None)).count()
    
    # Calculate total revenue
    completed_bookings = Reservation.query.filter(Reservation.leaving_time.isnot(None)).all()
    total_revenue = sum(booking.calculate_total_cost() for booking in completed_bookings)
    
    return render_template('admin/reports.html',
                          total_lots=total_lots,
                          total_spots=total_spots,
                          total_users=total_users,
                          active_reservations=active_reservations,
                          completed_reservations=completed_reservations,
                          total_revenue=total_revenue)


@admin.route('/search')
@admin_required
def search():
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'user')
    
    if not query:
        return redirect(url_for('admin.admin_dashboard'))
    
    results = []
    if search_type == 'user':
        results = User.query.filter(
            User.username.ilike(f'%{query}%') |
            User.full_name.ilike(f'%{query}%')
        ).all()
    elif search_type == 'spot':
        results = ParkingSpot.query.filter(
            ParkingSpot.id.ilike(f'%{query}%')
        ).all()
    elif search_type == 'location':
        results = ParkingLot.query.filter(
            ParkingLot.prime_location_name.ilike(f'%{query}%') |
            ParkingLot.address.ilike(f'%{query}%')
        ).all()
    
    return render_template('admin/search_results.html', 
                           results=results, 
                           search_type=search_type,
                           query=query)