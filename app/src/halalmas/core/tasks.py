from __future__ import absolute_import, unicode_literals
import datetime
import json

from django.conf import settings

from halalmas.core.lib.ses_mail import SES
from halalmas.core.lib.pdf import render_to_pdf

from celery import shared_task
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from email.utils import COMMASPACE


EMAIL_NO_REPLY = getattr(settings, 'EMAIL_NO_REPLY',
                         "halalmas <noreply@tempat.com>")
EMAIL_CS_HALALMAS = getattr(settings, 'EMAIL_CS_HALALMAS',
                         "hello@tempat.com")
CELERY_RUNNING = getattr(settings, 'CELERY_RUNNING', False)

logger = get_task_logger(__name__)


@shared_task
def send_email_task(recipient, payload={}, **kwargs):
    """Helper function"""
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))

    if isinstance(recipient, (list, tuple)):
        recipient = COMMASPACE.join(recipient)

    # print(kwargs)
    logger.debug(f'EMAIL_NO_REPLY: {EMAIL_NO_REPLY}, recipient: {recipient} {kwargs}')

    subject = kwargs.get('subject', "halalmas-mail-service-{}".format(date))
    # print("subject: {}".format(subject))
    email = SES(subject,
                EMAIL_NO_REPLY, recipient)
    email.reply_address = EMAIL_CS_HALALMAS
    if 'body' in payload:
        email.message_body = payload['body']
    else:
        email.message_body = 'testing mail from django command generator!!'
    if 'attachment' in payload:
        email.attachments = payload['attachment']
    email.send()
    print("Email has been sent to {}".format(recipient))

    return 1


@shared_task
def ses_send_mail_pdf_task(recipient, subject, body_msg, pdf_template, pdf_context, pdf_name='attachment.pdf'):
    pdf = render_to_pdf(pdf_template, pdf_context)

    email = SES(subject, EMAIL_NO_REPLY, recipient)
    email.message_body = pdf_context
    email.attachments = [
        {
            'file': pdf,
            'filename': pdf_name,
        }
    ]
    try:
        print("ses_send_mail_pdf sending email..")
        runs, status = email.send()
        print(runs, status)
    except Exception as e:
        print("Failed to send email, err:{}".format(e))

    logger.info("Send PDF email to {}".format(recipient))
    return 1


@shared_task
def ses_send_mail_task(recipient, subject, body_msg, attachment=None):
    """Helper function"""
    # date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    print(f'EMAIL_NO_REPLY: {EMAIL_NO_REPLY}, recipient: {recipient}')
    logger.debug(f'EMAIL_NO_REPLY: {EMAIL_NO_REPLY}, recipient: {recipient}')
    email = SES("{}".format(subject),
                EMAIL_NO_REPLY, recipient)
    if body_msg:
        email.message_body = body_msg
    else:
        email.message_body = 'You got mail from tempat.com!!'
    if attachment:
        email.attachments = attachment
    email.send()
    # print('DEBUG STATUS :',IS_DEBUG_ENVIRONMENT)
    print("SES Email has been sent to {}".format(recipient))
    logger.info("SES Email has been sent to {}".format(recipient))
    return 1



@shared_task
def ses_send_mail_w_sender_task(sender, recipient, subject, body_msg, attachment=None):
    """Helper ses_send_mail_w_sender_task function"""
    # date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    print(f'sender: {sender}, recipient: {recipient}')
    logger.debug(f'sender: {sender}, recipient: {recipient}')
    email = SES("{}".format(subject),
                sender, recipient)
    if body_msg:
        email.message_body = body_msg
    else:
        email.message_body = 'You got mail from tempat.com!!'
    if attachment:
        email.attachments = attachment
    email.send()
    # print('DEBUG STATUS :',IS_DEBUG_ENVIRONMENT)
    print("SES Email has been sent to {}".format(recipient))
    logger.info("SES Email has been sent to {}".format(recipient))
    return 1


def send_email(recipient, payload={}, **kwargs):
    # There is issue for async email ses, email not sent
    # if CELERY_RUNNING:
    #     send_email_task.delay(recipient, payload, **kwargs)
    # else:
    send_email_task(recipient, payload, **kwargs)
    return 1

def send_email_w_subject(subject_in, recipient, payload={}):
    """Send mail SES with subject"""

    send_email(recipient, payload, subject=subject_in)

    return "OK"
