from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
# Create your views here.


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup_form.html'
    success_url = settings.LOGOUT_URL


class UserLoginView(LoginView):
    template_name = 'accounts/login_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            return reverse_lazy('board:postlist')


logout = LogoutView.as_view(
    next_page=settings.LOGOUT_URL
)


def profile(request):
    return render(request, 'accounts/profile.html')
