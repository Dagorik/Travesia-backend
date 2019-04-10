# Generated by Django 2.1.2 on 2019-04-09 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsapp', '0008_checkpoint_num_checkpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpoint',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes'),
        ),
        migrations.AlterField(
            model_name='race',
            name='start_hour',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Hora de Inicio'),
        ),
    ]
