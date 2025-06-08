import os

class Config:
    SECRET_KEY               = os.environ["SECRET_KEY"]
    SECURITY_PASSWORD_SALT   = os.environ["SECURITY_PASSWORD_SALT"]

    SQLALCHEMY_DATABASE_URI  = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENDGRID_API_KEY         = os.environ["SENDGRID_API_KEY"]
    OPENROUTER_API_KEY       = os.environ["OPENROUTER_API_KEY"]
