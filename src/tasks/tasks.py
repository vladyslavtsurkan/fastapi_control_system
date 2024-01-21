import smtplib

from celery import Celery

from tasks.utils import get_email_template_verify_user
from config import AppSettings

settings = AppSettings()

celery = Celery(
    'celery_app',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
)


@celery.task
def send_email_for_verification_user(email: str, token: str) -> None:
    email = get_email_template_verify_user(email, token)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
        smtp.send_message(email)
