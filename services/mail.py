# services/mail.py

import os
import sendgrid
from sendgrid.helpers.mail import Mail
from flask import current_app

def send_confirmation_email(to_email, token):
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    confirm_url = f"{current_app.config['BASE_URL']}/confirm/{token}"

    message = Mail(
        from_email=current_app.config["EMAIL_SENDER"],
        to_emails=to_email,
        subject="Confirm Your Email - Ghostmodzz Flow",
        html_content=f"""
        <h1>Welcome to Ghostmodzz Flow 🚀</h1>
        <p>Click below to confirm your email address:</p>
        <a href="{confirm_url}">Confirm Email</a>
        """
    )
    sg.send(message)
