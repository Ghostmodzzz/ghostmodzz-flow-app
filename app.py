# app.py
from factory import create_app

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    # For local development only
    app.run(host='0.0.0.0', port=5000, debug=True)
