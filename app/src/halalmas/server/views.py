from django.conf import settings

from django.shortcuts import render


def welcome(request):
    return render(request, 'core/server/welcome.html')


def empty(request):
    return render(request, '503.html')
