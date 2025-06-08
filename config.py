import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    BASE_URL = os.getenv("BASE_URL")  # You have this one already
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # <--- 🛑 ADD THIS LINE
