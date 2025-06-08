from flask import Flask  # ← IMPORTANT IMPORT
from extensions import db, login_manager, mail
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from models import User, Paycheck, Bill
        db.create_all()  # <-- Auto-create missing tables on startup

    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
