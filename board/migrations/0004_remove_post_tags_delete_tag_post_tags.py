# Generated by Django 4.2.6 on 2023-10-27 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_remove_tag_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]
