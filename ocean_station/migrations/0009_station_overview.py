# Generated by Django 3.2.9 on 2022-01-22 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_station', '0008_station_introductions'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='overview',
            field=models.TextField(default=None, null=True),
        ),
    ]
