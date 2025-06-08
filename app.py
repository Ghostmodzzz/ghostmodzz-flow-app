from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main as main_blueprint
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    app.register_blueprint(main_blueprint)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
