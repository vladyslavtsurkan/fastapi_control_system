from celery import Celery

from tasks.utils import (
    send_email,
    get_email_template_verify_user,
    get_email_template_forgot_password,
)
from config import AppSettings

settings = AppSettings()

celery = Celery(
    'celery_app',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
)


@celery.task
def send_email_for_verification_user(email: str, token: str) -> None:
    email = get_email_template_verify_user(email, token)
    send_email(email)


@celery.task
def send_email_for_forgot_password(email: str, token: str) -> None:
    email = get_email_template_forgot_password(email, token)
    send_email(email)
