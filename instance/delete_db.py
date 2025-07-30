import os
db_path = 'parking.db'
try:
    os.remove(db_path)
    print("deleted")
except FileNotFoundError:
    print(f"{db_path} not found.")
except PermissionError:
    print(f"Permission denied. Close any programs using {db_path} and try again.")
except Exception as e:
    print(f"Error deleting {db_path}: {e}")