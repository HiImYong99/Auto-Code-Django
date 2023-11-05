from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='signup'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('delete_success/', views.UserDeleteSuccessView.as_view(),
         name='user_delete_success'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit/profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('password_reset/', views.MyPasswordResetView.as_view(),
         name='password_reset'),
    path('password_email_done/', views.MyPasswordEmailView.as_view(),
         name='password_email_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # path('edit/password/', views.EditProfileView.as_view(), name='edit_password'),
    # path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    # reset pw


    # path('asdf/', views.send_email),
]
