# Generated by Django 3.2.9 on 2022-01-06 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20211126_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='privilege',
            field=models.PositiveSmallIntegerField(choices=[(255, 'Super User'), (3, 'Official Account'), (1, 'User')], default=1),
        ),
    ]
