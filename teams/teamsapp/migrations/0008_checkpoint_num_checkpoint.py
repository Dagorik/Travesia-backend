# Generated by Django 2.1.2 on 2019-04-09 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsapp', '0007_auto_20190409_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpoint',
            name='num_checkpoint',
            field=models.IntegerField(default=0),
        ),
    ]
