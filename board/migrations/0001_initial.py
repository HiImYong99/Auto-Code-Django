# Generated by Django 4.2.6 on 2023-11-05 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='board/images/%Y/%m/%d')),
                ('file', models.FileField(blank=True, null=True, upload_to='board/files/%Y/%m/%d/')),
                ('category', models.CharField(choices=[('자유', '자유'), ('질문', '질문'), ('고민', '고민'), ('스터디', '스터디')], default='자유', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('like_user', models.ManyToManyField(blank=True, related_name='like_posts', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='board.tag')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='board.post')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
