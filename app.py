# app.py
from factory import create_app

# Create the app instance
app = create_app()

# Only run the app if this file is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
