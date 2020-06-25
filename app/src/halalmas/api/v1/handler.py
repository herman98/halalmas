from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime

from rest_framework.authtoken.models import Token


# this return left time
def expires_in(token):
    time_elapsed = datetime.now() - token.created
    # print(
    #     f'time_elapsed: {time_elapsed}, now: {datetime.now()}, token {token.created}')
    left_time = timedelta(
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    # print(
    #     f'left_time: {left_time}, /60: {left_time/60}')
    return left_time/(60)


def date_expires_in(token):
    date_exp = token.created + \
        timedelta(seconds=(settings.TOKEN_EXPIRED_AFTER_SECONDS))
    print(
        f'date_exp: {date_exp}, token.created: {token.created}, exp-sec {settings.TOKEN_EXPIRED_AFTER_SECONDS}')
    return date_exp

# token checker if token expired or not


def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created

def token_expire_handler(token):
    return False, token
    # is_expired = is_token_expired(token)
    # if is_expired:
    #     token.delete()
    #     token = Token.objects.create(user=token.user)
    # return is_expired, token
