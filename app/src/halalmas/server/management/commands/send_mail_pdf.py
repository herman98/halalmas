import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from tempatdotcom.core.lib.pdf import render_to_pdf
from tempatdotcom.core.lib.ses_mail import SES

EMAIL_NO_REPLY = getattr(settings, 'EMAIL_NO_REPLY',
                         "'tempat dot com' <noreply@tempat.com>")


class Command(BaseCommand):
    help = 'Send email with pdf'

    def add_arguments(self, parser):
        # parser.add_argument('to', nargs='+', type=str,
        #                     help='tech@tempat.com', )
        parser.add_argument('-to', '--to', type=str,
                            help='tech@tempat.com', )

    def handle(self, *args, **options):
        print("Render pdf...")
        # ---
        recipient = options['to'] 
        print("Starting command... {}".format(recipient))
        # recipient = options.get('to')

        context = {'notes': 'Hi There'}
        pdf = render_to_pdf('testing/page1.html', context)

        email = SES("Email test", EMAIL_NO_REPLY, recipient)
        email.message_body = 'Hi..'
        email.attachments = [
            {
                'file': pdf,
                'filename': 'report.pdf'
            }
        ]

        # try:
        print("try to send email..")
        runs, status = email.send()
        print(runs, status)
        # except Exception as e:
        #     print("Failed to send email, err:{}".format(e))

        logging.info("Send email to {}".format(recipient))
