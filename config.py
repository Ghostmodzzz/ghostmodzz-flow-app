import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SendGrid Email Setup
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER')

    # OpenRouter AI API Key
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
