from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main as main_blueprint
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    # register blueprints
    app.register_blueprint(main_blueprint)
    return app

# ── expose the app for Gunicorn ───────────────────────
app = create_app()

if __name__ == "__main__":
    # local dev server
    app.run(debug=True)
