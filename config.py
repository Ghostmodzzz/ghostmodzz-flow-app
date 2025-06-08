import os

class Config:
    # Secret key for sessions
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Salt for email confirmation tokens
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SendGrid API Key for sending emails
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "").strip()
    # The email address you're sending from
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "").strip()

    # OpenRouter API Key
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
