from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile')
]
