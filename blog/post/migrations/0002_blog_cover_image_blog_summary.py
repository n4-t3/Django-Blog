# Generated by Django 4.1.1 on 2022-09-13 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to='covers'),
        ),
        migrations.AddField(
            model_name='blog',
            name='summary',
            field=models.CharField(default='Summary not provided:(', max_length=255),
        ),
    ]
