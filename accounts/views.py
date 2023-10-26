from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
# Create your views here.

signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name='accounts/signup_form.html',
    success_url=settings.LOGOUT_URL,
)

login = LoginView.as_view(
    template_name='accounts/login_form.html',
    next_page=settings.LOGIN_URL,
)

logout = LogoutView.as_view(
    next_page=settings.LOGOUT_URL
)
