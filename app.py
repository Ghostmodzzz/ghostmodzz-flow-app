from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main as main_blueprint
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(main_blueprint)

    # Auto-create any missing tables
    with app.app_context():
        db.create_all()

    return app

# Expose a module-level 'app' for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
