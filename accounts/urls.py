from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit/profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('edit/password/', views.EditProfileView.as_view(), name='edit_password'),
    # path('profile/delete/', views.profile_delete_view, name='profile_delete'),
]
