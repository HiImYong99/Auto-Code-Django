from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('auto-coding/', views.IndexView.as_view(), name='index'),
]
