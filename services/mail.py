from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app, url_for

def send_confirmation_email(user):
    token = user.get_confirm_token()
    confirm_url = url_for("main.confirm_email", token=token, _external=True)
    html = f"""
      <h3>Welcome to GhostModzz Flow!</h3>
      <p>Please click the link below to confirm your account:</p>
      <p><a href="{confirm_url}">Confirm Your Account</a></p>
    """
    msg = Mail(
        from_email=current_app.config["MAIL_DEFAULT_SENDER"],
        to_emails=user.email,
        subject="Confirm Your GhostModzz Account",
        html_content=html
    )
    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
    sg.send(msg)
