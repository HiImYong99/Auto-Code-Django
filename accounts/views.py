from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from accounts.models import User
from .forms import SignupForm, ChangeUserForm
from board.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import CheckPasswordForm
from django.contrib.auth.decorators import login_required

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


@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            return redirect('/users/login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'accounts/profile_delete.html', {'password_form': password_form})
