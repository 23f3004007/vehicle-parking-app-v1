import subprocess
import sys

def install_requirements():
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: requirements.txt not found!")
        sys.exit(1)

if __name__ == '__main__':
    install_requirements()
    from app import create_app
    app = create_app()
    app.run(debug=True)
