from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

category_select = (
    ('자유', '자유'),
    ('질문', '질문'),
    ('고민', '고민'),
    ('스터디', '스터디')
)


class Post(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    content = models.TextField()
    img = models.ImageField(
        upload_to='board/images/%Y/%m/%d', blank=True, null=True
    )
    file = models.FileField(
        upload_to='board/files/%Y/%m/%d/', blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=category_select, default='자유')
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
