# Generated by Django 2.1.2 on 2018-12-04 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181203_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.URLField(blank=True, null=True),
        ),
    ]