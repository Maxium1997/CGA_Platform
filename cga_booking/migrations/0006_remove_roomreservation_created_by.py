# Generated by Django 3.2.9 on 2022-01-02 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cga_booking', '0005_roomreservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomreservation',
            name='created_by',
        ),
    ]
