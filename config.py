import os

class Config:
    # Flask secret
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    # itsdangerous salt for email confirmation
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "")
    # SendGrid API key (strip out any stray newline)
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "").strip()
    # The “from” address you registered as a Single Sender in SendGrid
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "").strip()
    # Your OpenRouter key
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
