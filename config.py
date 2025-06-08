import os

class Config:
    # Flask secret for sessions, CSRF protection, etc.
    SECRET_KEY = os.environ["SECRET_KEY"]

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SendGrid (email verification)
    SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

    # OpenRouter (AI budgeting)
    OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

    # itsdangerous salt for email confirmation tokens
    SECURITY_PASSWORD_SALT = os.environ["SECURITY_PASSWORD_SALT"]
