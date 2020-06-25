import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from halalmas.core.tasks import send_email
from django.template.loader import get_template



class Command(BaseCommand):

    help = """
    Send email using AWS SES

    e.g. ./manage.py send_email test@email.com
    """

    # parser.add_argument('mode', type=str, help='Indicates the number of users to be created')
    # parser.add_argument('-select', '--selection', type=str,
    #                     help='migrate data, -select=buildings for migrate building data, others (building_categories, rating_master, rooms, cms_users)', )
    # parser.add_argument('-m', '--mode', type=int,
    #                     help='Define a mode to exececute ex: -m=0 is all, -m=10 for ten records only', )

    def add_arguments(self, parser):
        # parser.add_argument('to', nargs='+', type=str,
        #                     help='cobaan.xwork@gmail.com', )
        parser.add_argument('-to', '--to', type=str,
                            help='cobaan.xwork@gmail.com', )


    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)
        
        template_user_html = 'user/user.html'
        render_html = get_template(template_user_html)
        url = 'http://tempat.com/welcome/yuybinompihgofdtf7yguh'
        username = 'Antonio Kendrik cacaca'
        waktu = 7
        render_context = render_html.render({
            'user': {
                'username': username,
                'content': 'Sepertinya Anda lupa password Anda, klik tombol dibawah untuk ganti password',
                'button': 'Ganti Password',
                'url': url,
                'url_cut': url[:33],
                'while': f'{waktu} hari'
            }
        })

        payload = {
            'body': render_context,
            'attachment': []
        }

        recipient = options['to'] 
        print("Starting command... {}".format(recipient))
        send_email(recipient, payload, subject="hohoho")

        logging.info("Send email to {}".format(recipient))
