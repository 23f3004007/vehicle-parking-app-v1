# Vehicle Parking App - V1

A Flask-based multi-user web application for managing 4-wheeler parking lots, spots, and reservations, featuring role-based access for administrators and registered users.

## Project Overview

Vehicle Parking App - V1 enables efficient management of parking lots and spots for 4-wheelers. The platform supports two roles: Admin (superuser, no registration required) and User (register/login to reserve parking). Admins can manage lots and monitor spot statuses, while users can book and release spots with automated allocation.
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/f4427d4d-4378-4565-a7d5-b7e2ebc88dd7" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/b6133897-58ab-4aa6-9564-24a84830e7cd" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/a8feb8aa-e910-46cc-acbe-19ba8073a12f" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/555462b7-0c15-47e8-8897-e658702e66b9" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/f2b372be-ee0c-4a6a-abe3-b50a3959a9d5" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/9a0d4524-34bf-40ac-b87b-66a427286588" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/98605959-c6e6-4190-a47a-1036bc764f40" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/b167fb85-54a4-4ad3-be90-e0b09a2103d9" />
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/2a3dca24-e1e4-4270-bb82-7d11778369e0" />

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
