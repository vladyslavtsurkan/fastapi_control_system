import smtplib
from email.message import EmailMessage

from config import AppSettings

settings = AppSettings()


def send_email(email: EmailMessage) -> None:
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
        smtp.send_message(email)


def get_email_template_verify_user(user_email: str, token: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = '[Control system] Verification email'
    email['From'] = settings.SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1>Hello, {user_email}.</h1>'
        '<p>Thank you for registering on the control system.</p>'
        '<p>To complete the registration, input the token below.</p>'
        f'<p>Token: {token}</p>'
        '</div>',
        subtype='html'
    )
    return email


def get_email_template_forgot_password(user_email: str, token: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = '[Control system] Forgot password'
    email['From'] = settings.SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1>Hello, {user_email}.</h1>'
        '<p>You have requested a password reset.</p>'
        '<p>To reset your password, input the token below.</p>'
        f'<p>Token: {token}</p>'
        '</div>',
        subtype='html'
    )
    return email
