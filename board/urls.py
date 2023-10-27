from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.postlist, name='postlist'),
    path('post/write/', views.postcreate, name='postcreate'),
    path('post/<int:pk>/', views.postdetail, name='postdetail'),
    path('post/edit/<int:pk>/', views.postupdate, name='postupdate'),
    path('post/delete/<int:pk>/', views.postdelete, name='postdelete'),
    path('<int:pk>/comment/new/', views.comment_new, name='comment_new'),
]
