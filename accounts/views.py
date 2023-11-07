from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from accounts.models import User
from .forms import SignupForm, ChangeUserForm
from board.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
# Create your views here.


class UserCreateView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup_form.html'
    success_url = settings.LOGOUT_URL


class UserDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = 'accounts/user_confirm_delete.html'
    model = get_user_model()

    success_url = reverse_lazy('accounts:user_delete_success')

    def test_func(self):
        return self.get_object() == self.request.user


class UserDeleteSuccessView(TemplateView):
    template_name = 'accounts/user_delete_success.html'


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
    model = get_user_model()
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    paginate_by = 1

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            writer=self.request.user).order_by('-created_at')[:5]
        context['likes'] = Post.objects.filter(
            like_user=self.request.user).order_by('-created_at')[:5]
        context['comments'] = Comment.objects.filter(
            writer=self.request.user).order_by('-created_at')[:5]
        return context


class EditProfileView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    form_class = ChangeUserForm
    model = get_user_model()
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:edit_profile')

    def get_object(self):
        return self.request.user


class MyPasswordResetView(PasswordResetView, LoginRequiredMixin, UserPassesTestMixin):
    success_url = reverse_lazy('accounts:password_email_done')
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset.html'
    mail_title = "비밀번호 재설정"

    def form_valid(self, form):
        return super().form_valid(form)


class MyPasswordEmailView(TemplateView):
    template_name = 'accounts/password_email_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)
