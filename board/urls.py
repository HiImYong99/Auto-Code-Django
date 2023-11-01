from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.postlist, name='postlist'),
    path('popular_posts/', views.popular_postlist, name='popular_postlist'),
    path('post/write/', views.postcreate, name='postcreate'),
    path('post/<int:pk>/', views.postdetail, name='postdetail'),
    path('post/edit/<int:pk>/', views.postupdate, name='postupdate'),
    path('post/delete/<int:pk>/', views.post_delete, name='postdelete'),
    path('post/<int:pk>/likes/', views.likes, name='likes'),
    path('<int:pk>/comment/new/', views.comment_new, name='comment_new'),
    path('<int:pk>/comment/delete/', views.comment_delete, name='comment_delete'),
]
