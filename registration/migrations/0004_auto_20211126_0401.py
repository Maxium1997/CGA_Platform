# Generated by Django 3.2.9 on 2021-11-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_user_id_number_is_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Chose your gender'), (1, 'Male'), (2, 'Female'), (3, 'Privacy')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='identity',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Chose your identity'), (1, 'Citizen'), (2, 'Civil Servant'), (3, 'Military'), (4, 'Police')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='privilege',
            field=models.PositiveSmallIntegerField(choices=[(255, 'Super User'), (1, 'User')], default=1),
        ),
    ]
