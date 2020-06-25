from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class HashedPasswordAuthBackend(ModelBackend):

    def true_authenticate(self, username=None, password=None):
        print(f'my- true authenticate: {username} {password}')
        user = User.objects.filter(username=username, password=password)

        if user.count() >= 1:
            return user.first()
        else:
            raise Exception('no user created')

    def authenticate(self, username=None, password=None):
        print(f'my- authenticate: {username} {password}')
        try:
            return User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
