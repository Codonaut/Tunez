# Generated by Django 2.1.3 on 2018-11-20 04:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music_library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='users',
            field=models.ManyToManyField(related_name='songs', through='music_library.Library', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='library',
            unique_together={('user', 'song')},
        ),
    ]
