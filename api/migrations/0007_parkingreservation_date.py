# Generated by Django 2.0.6 on 2018-07-03 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180703_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingreservation',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
