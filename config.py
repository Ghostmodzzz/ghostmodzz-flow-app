import os

class Config:
    # Flask & WTF
    SECRET_KEY               = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT   = os.environ.get("SECURITY_PASSWORD_SALT")

    # Database (if you’re using Render Postgres, you can also pull DATABASE_URL here)
    SQLALCHEMY_DATABASE_URI  = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SendGrid
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    EMAIL_SENDER     = os.environ.get("EMAIL_SENDER")

    # OpenRouter
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
