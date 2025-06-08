# app.py

from factory import create_app

app = create_app()

# Optional for local development only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
