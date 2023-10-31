from django.core.mail.message import EmailMessage
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
# from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from accounts.models import User
from .forms import SignupForm, ChangeUserForm
from board.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import CheckPasswordForm
from django.contrib.auth.decorators import login_required
from django.core.mail.message import EmailMessage

# Create your views here.


class UserCreateView(CreateView):
    form_class = SignupForm
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


class ProfileView(TemplateView, LoginRequiredMixin):
    model = User
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    paginate_by = 1

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(writer=self.request.user)
        context['comments'] = Comment.objects.filter(writer=self.request.user)
        return context


class EditProfileView(UpdateView, LoginRequiredMixin):
    form_class = ChangeUserForm
    model = User
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:edit_profile')

    def get_object(self):
        return self.request.user


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset.html'
    mail_title = "비밀번호 재설정"

    def form_valid(self, form):
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


def send_email(request):
    subject = "메시지"
    to = ['good19422@naver.com']
    from_email = 'good19422@gmail.com'
    message = "메시지를 성공적으로 전송"
    EmailMessage(subject=subject, body=message,
                 to=to, from_email=from_email).send()
