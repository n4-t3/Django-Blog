# Generated by Django 4.1.1 on 2022-09-22 09:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0004_blog_views_alter_blog_category'),
        ('authentication', '0004_userprofile_bookmarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to='post.blog'),
        ),
    ]
