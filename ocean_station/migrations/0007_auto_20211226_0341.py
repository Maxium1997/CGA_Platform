# Generated by Django 3.2.9 on 2021-12-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocean_station', '0006_auto_20211127_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_flag',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Overview'), (2, 'Title'), (3, 'Subtitle'), (4, 'Content'), (5, 'Explanation'), (6, 'Traffic Information'), (7, 'Cautions'), (8, 'Other')], default=4),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo_flag',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Main'), (2, 'Display'), (3, 'Poster'), (4, 'Activity'), (5, 'Publicity')], default=2),
        ),
        migrations.AlterField(
            model_name='taggedattraction',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
