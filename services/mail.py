import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config

def send_confirmation_email(to_email, token):
    confirm_url = f"https://ghostmodzz-flow-app.onrender.com/confirm/{token}"
    
    message = Mail(
        from_email=Config.EMAIL_SENDER,
        to_emails=to_email,
        subject="Confirm Your Email",
        html_content=f"""
        <p>Welcome to GhostModzz Flow!</p>
        <p>Please confirm your email by clicking on the link below:</p>
        <a href="{confirm_url}">Confirm your email</a>
        <p>If you did not request this, please ignore this email.</p>
        """
    )
    
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(f"Error sending email: {e}")
