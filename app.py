from flask import Flask
from flask_login import LoginManager
from extensions import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)