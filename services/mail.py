import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import Config

def send_confirmation_email(to_email: str, token: str):
    """
    Send the account‐confirmation email via SendGrid.
    """
    confirm_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/confirm/{token}"
    message = Mail(
        from_email=Config.EMAIL_SENDER,
        to_emails=to_email,
        subject="Please confirm your GhostModzz Flow email",
        html_content=f"""
            <p>Welcome to GhostModzz Flow!</p>
            <p>Click <a href="{confirm_url}">here to confirm your email</a>.</p>
            <p>This link will expire in 1 hour.</p>
        """
    )
    client = SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
    client.send(message)
