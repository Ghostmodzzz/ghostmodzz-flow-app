from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config
from flask import url_for

def send_confirmation_email(to_email, token):
    link = url_for("main.confirm_email", token=token, _external=True)
    message = Mail(
        from_email=Config.EMAIL_SENDER,
        to_emails=to_email,
        subject="Confirm your GhostModzz Flow account",
        html_content=f"<p>Please click <a href='{link}'>here</a> to confirm your email.</p>"
    )
    sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
    sg.send(message)
