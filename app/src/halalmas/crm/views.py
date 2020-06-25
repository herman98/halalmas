from django import forms
from django.conf import settings

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


from tempatdotcom.crm.objects.dashboard.views \
    import index as dashboard_index


@login_required
def welcome(request):
    return render(request, 'core/welcome.html')


def welcome(request):
    # return render(request, "auth/success.html")
    return dashboard_index(request)


class RFPAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control input-lg',
               'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control input-lg',
               'placeholder': 'Password'}))


def login_view(request):
    if request.method == 'POST':
        form = RFPAuthForm(request, request.POST)
        if form.is_valid():
            print(form)
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=pwd)
            if user is not None:
                return welcome(request)
        else:
            print("FORM not valid")
    else:
        form = RFPAuthForm(request)
    return render(request, "auth/login_theme.html", {'form': form})


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return login_view(request)


def empty(request):
    return render(request, '503.html')


def index_page(request):
    return reverse('accounts:login')
