# Generated by Django 2.1.2 on 2018-12-20 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_baucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='valid_baucher',
            field=models.BooleanField(default=False),
        ),
    ]
