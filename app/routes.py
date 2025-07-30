from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from flask import request, jsonify
from .models import ParkingLot, ParkingSpot, User, db
from datetime import datetime
from .models import Reservation
from .decorators import admin_required, user_required

main = Blueprint('main', __name__)
user = Blueprint('user', __name__, url_prefix='/user')
admin = Blueprint('admin', __name__, url_prefix='/admin')

# # Admin-only decorator
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or not isinstance(current_user, Admin):
#             flash('You need to be logged in as an admin to view this page.')
#             return redirect(url_for('auth.login'))
#         return f(*args, **kwargs)
#     return decorated_function

# # User-only decorator
# def user_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or not isinstance(current_user, User):
#             flash('You need to be logged in as a user to view this page.')
#             return redirect(url_for('auth.login'))
#         return f(*args, **kwargs)
#     return decorated_function

@main.route('/')
def index():
    if current_user.is_authenticated:
        if isinstance(current_user, is_admin = True):
            return redirect(url_for('admin.admin_dashboard'))  # Change from 'admin.dashboard' to 'admin.admin_dashboard'
        return redirect(url_for('user.user_dashboard'))
    return render_template('index.html')

@user.route('/dashboard')
@login_required
@user_required
def user_dashboard():
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
        # Backend validation
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        pin_code = request.form.get('pin_code', '')
        price_per_hour = request.form.get('price_per_hour', 0)
        max_spots = request.form.get('max_spots', 0)

        # Validate inputs
        if not (3 <= len(name) <= 100):
            flash('Location name must be between 3 and 100 characters.', 'error')
            return render_template('admin/lot_form.html')

        if not (10 <= len(address) <= 200):
            flash('Address must be between 10 and 200 characters.', 'error')
            return render_template('admin/lot_form.html')

        if not pin_code.isdigit() or len(pin_code) != 6:
            flash('PIN Code must be exactly 6 digits.', 'error')
            return render_template('admin/lot_form.html')

        try:
            price = float(price_per_hour)
            if not (0.01 <= price <= 10000):
                raise ValueError
        except ValueError:
            flash('Invalid price value. Must be between ₹0.01 and ₹10,000.', 'error')
            return render_template('admin/lot_form.html')

        try:
            spots = int(max_spots)
            if not (1 <= spots <= 1000):
                raise ValueError
        except ValueError:
            flash('Invalid number of spots. Must be between 1 and 1000.', 'error')
            return render_template('admin/lot_form.html')

        # If validation passes, create the lot
        lot = ParkingLot(
            prime_location_name=name,
            address=address,
            pin_code=pin_code,
            price_per_hour=price,
            max_spots=spots
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
        # Backend validation
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        pin_code = request.form.get('pin_code', '')
        price_per_hour = request.form.get('price_per_hour', 0)

        # Validate inputs
        if not (3 <= len(name) <= 100):
            flash('Location name must be between 3 and 100 characters.', 'error')
            return render_template('admin/lot_form.html', lot=lot)

        if not (10 <= len(address) <= 200):
            flash('Address must be between 10 and 200 characters.', 'error')
            return render_template('admin/lot_form.html', lot=lot)

        if not pin_code.isdigit() or len(pin_code) != 6:
            flash('PIN Code must be exactly 6 digits.', 'error')
            return render_template('admin/lot_form.html', lot=lot)

        try:
            price = float(price_per_hour)
            if not (0.01 <= price <= 10000):
                raise ValueError
        except ValueError:
            flash('Invalid price value. Must be between ₹0.01 and ₹10,000.', 'error')
            return render_template('admin/lot_form.html', lot=lot)

        # If validation passes, update the lot
        lot.prime_location_name = name
        lot.address = address
        lot.pin_code = pin_code
        lot.price_per_hour = price
        db.session.commit()
        flash('Parking lot updated successfully!', 'success')
        return redirect(url_for('admin.manage_lots'))
    return render_template('admin/lot_form.html', lot=lot)

@admin.route('/lots/<int:lot_id>/delete', methods=['POST'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    occupied_spots = any(spot.status == 'O' for spot in lot.spots)
    if occupied_spots:
        flash('Cannot delete lot with occupied spots.', 'error')
        return redirect(url_for('admin.manage_lots'))
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
@user_required
def view_parking_lots():
    lots = ParkingLot.query.all()
    return render_template('user/parking_lots.html', lots=lots)

@user.route('/reserve/<int:lot_id>', methods=['POST'])
@login_required
@user_required
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
@user_required
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
@user_required
def view_reservations():
    return render_template('user/reservations.html', 
                         reservations=current_user.reservations,
                         now=datetime.utcnow)

@user.route('/history')
@login_required
@user_required
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
    from datetime import datetime
    reservations = Reservation.query.order_by(Reservation.parking_time.desc()).all()
    now = datetime.utcnow()
    return render_template('admin/reservations.html', reservations=reservations, now=now)

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


# Add these imports at the top
from flask import jsonify

# API endpoints for parking lots
@admin.route('/api/lots', methods=['GET'])
@admin_required
def get_lots():
    lots = ParkingLot.query.all()
    return jsonify([
        {
            'id': lot.id,
            'name': lot.prime_location_name,
            'address': lot.address,
            'price_per_hour': lot.price_per_hour,
            'total_spots': lot.max_spots,
            'available_spots': lot.available_spots
        } for lot in lots
    ])

# API endpoint for spots in a lot
@admin.route('/api/lots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def get_lot_spots(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    return jsonify([
        {
            'id': spot.id,
            'status': spot.status,
            'is_available': spot.is_available()
        } for spot in lot.spots
    ])

# API endpoint for reservations
@admin.route('/api/reservations', methods=['GET'])
@admin_required
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([
        {
            'id': res.id,
            'user': res.user.username,
            'spot_id': res.spot_id,
            'parking_time': res.parking_time.isoformat(),
            'leaving_time': res.leaving_time.isoformat() if res.leaving_time else None,
            'cost': res.calculate_total_cost()
        } for res in reservations
    ])

# User-specific API endpoints
@user.route('/api/my-history', methods=['GET'])
@login_required
@user_required
def get_user_history():
    reservations = Reservation.query.filter_by(
        user_id=current_user.id
    ).filter(
        Reservation.leaving_time.isnot(None)
    ).order_by(Reservation.parking_time.desc()).all()
    
    return jsonify([
        {
            'location': res.spot.lot.prime_location_name,
            'parking_time': res.parking_time.isoformat(),
            'leaving_time': res.leaving_time.isoformat(),
            'duration': round((res.leaving_time - res.parking_time).total_seconds() / 3600, 1),
            'cost': res.calculate_total_cost()
        } for res in reservations
    ])

@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
@user_required
def edit_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name=request.form.get('full_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password and password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('user.edit_profile'))
        
        current_user.email = email
        current_user.full_name = full_name
        if password:
            current_user.set_password(password)
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('user.edit_profile'))
    return render_template('user/edit_profile.html')