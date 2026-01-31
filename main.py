from app import create_app

# Vercel looks for the variable 'app' in this file
app = create_app()

# This part is only for local development
if __name__ == '__main__':
    app.run(debug=True)
