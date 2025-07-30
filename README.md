# Vehicle Parking App - V1

A Flask-based multi-user web application for managing 4-wheeler parking lots, spots, and reservations, featuring role-based access for administrators and registered users.

## Project Overview

Vehicle Parking App - V1 enables efficient management of parking lots and spots for 4-wheelers. The platform supports two roles: Admin (superuser, no registration required) and User (register/login to reserve parking). Admins can manage lots and monitor spot statuses, while users can book and release spots with automated allocation.


## Architecture

### Backend

- Flask framework for routing and business logic
- SQLAlchemy ORM for database management
- SQLite database for data persistence
- Werkzeug for security features

### Frontend

- Jinja2 templating engine
- Bootstrap for responsive design
- Chart.js for data visualization
- HTML and Custom CSS for styling

## Database Schema
![Example](https://github.com/user-attachments/assets/9a63121b-0bf4-4ed1-8de5-43ed0888fbd8)

## Features

### Authentication System

- Role-based access control (Admin/User)
- Simple login/register forms (no advanced security required)
- Session management

### Admin Features

- Default admin exists on DB creation (no registration)
- Create, edit, delete parking lots
- Set number of spots per lot (spots auto-generated)
- View all parking lots and spot statuses
- View details of occupied spots and parked vehicles
- View all registered users
- Dashboard with summary charts (parking lot usage, occupancy, etc.)

### User Features

- Register and login
- View available parking lots
- Book a spot (auto-allocation of first available)
- Release/vacate spot (updates status)
- View personal reservation history and summary charts

### API Endpoints

- `/login` – Login for admin/user
- `/register` – User registration
- `/admin/dashboard` – Admin dashboard
- `/admin/lots` – CRUD operations for parking lots
- `/admin/users` – View all users
- `/user/dashboard` – User dashboard
- `/user/reserve` – Reserve a parking spot
- `/user/release` – Release a parking spot

## Issues faced and Solutions implemented

### 1. Programmatic Database Creation

**Issue:** Manual DB creation not allowed
**Solution:** Used Flask app startup scripts to auto-create tables if not present.

### 2. Spot Allocation Logic

**Issue:** Users cannot select specific spots
**Solution:** Implemented first-available spot allocation per lot.

### 3. Admin Deletion Constraints

**Issue:** Cannot delete lots with occupied spots
**Solution:** Added checks to prevent deletion unless all spots are empty.

### 4. Role Differentiation

**Issue:** Distinguishing admin from users
**Solution:** Role field in Users table; admin auto-created on DB init.

### 5. Timestamp Management

**Issue:** Accurate parking in/out tracking
**Solution:** Used Python datetime for parking and leaving timestamps.

## Setup Instructions

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```bash
python run.py
```

4. Access the application:

- URL: http://localhost:5000
- Default Admin Credentials:
  - Username: admin
  - Password: admin123

## Project Structure

```bash
vehicle-parking-app-v1/
├─ app/
│  ├─ __pycache__/
│  ├─ templates/
│  │  ├─ admin/
│  │  │  ├─ dashboard.html
│  │  │  ├─ lot_details.html
│  │  │  ├─ lot_form.html
│  │  │  ├─ lots.html
│  │  │  ├─ reports.html
│  │  │  ├─ reservations.html
│  │  │  ├─ search_results.html
│  │  │  ├─ user_details.html
│  │  │  └─ users.html
│  │  ├─ auth/
│  │  │  ├─ login.html
│  │  │  └─ register.html
│  │  ├─ user/
│  │  │  ├─ dashboard.html
│  │  │  ├─ edit_profile.html
│  │  │  ├─ history.html
│  │  │  ├─ parking_lots.html
│  │  │  └─ reservations.html
│  │  ├─ base.html
│  │  └─ index.html
│  ├─ __init__.py
│  ├─ auth.py
│  ├─ decorators.py
│  ├─ models.py
│  └─ routes.py
├─ instance/
│  └─ parking.db
├─ README.md
├─ requirements.txt
└─ run.py
```

## Contributors

### Veditha R 23f3004007
