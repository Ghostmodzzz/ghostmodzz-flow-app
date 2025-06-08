from flask import Flask
from extensions import db, login_manager, mail
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Auto-create database tables
    with app.app_context():
        from models import User, Bill, Paycheck
        db.create_all()

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
