from flask import Flask
from config import Config
from extensions import db, login_manager, mail
from routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'main.login'

    # Register Blueprints
    app.register_blueprint(main_blueprint)

    return app
