# Generated by Django 2.1.2 on 2018-10-08 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='teams',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
