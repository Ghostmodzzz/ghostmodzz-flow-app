from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(main_blueprint)
    return app

app = create_app()
