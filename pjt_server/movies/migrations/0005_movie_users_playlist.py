# Generated by Django 3.1.3 on 2020-11-24 12:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0004_auto_20201122_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='users_playlist',
            field=models.ManyToManyField(related_name='movies_playlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
