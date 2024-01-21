from email.message import EmailMessage

from config import AppSettings

settings = AppSettings()


def get_email_template_verify_user(user_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = '[Control system] Verification email'
    email['From'] = settings.SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {user_email}.</h1>'
        '<p>Thank you for registering on the control system.</p>'
        '<p>To complete the registration, input the token below.</p>'
        f'<p>Token: {token}.</p>'
        '</div>',
        subtype='html'
    )
    return email
