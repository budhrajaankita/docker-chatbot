import os
from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import redis
import json

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

celery_app = Celery('worker', broker=CELERY_BROKER_URL, result_backend=CELERY_RESULT_BACKEND)
#redis_client = redis.Redis(host='redis_container', port=6379)

@celery_app.task
def send_email(from_email, to_email, subject, body):
    try:
        SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        content = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=body)
        response = sg.send(content)
        return response
    except Exception as e:
        print(str(e))
        return str(e)