# Generated by Django 3.2.9 on 2021-11-26 17:03

from django.db import migrations, models
import django.db.models.deletion
import ocean_station.models


class Migration(migrations.Migration):

    dependencies = [
        ('multi_relation', '0001_initial'),
        ('ocean_station', '0004_auto_20211126_0708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('textitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='multi_relation.textitem')),
                ('Title', models.CharField(blank=True, max_length=255, null=True)),
                ('path', models.ImageField(blank=True, null=True, upload_to=ocean_station.models.station_upload_path)),
                ('photo_flag', models.PositiveSmallIntegerField(choices=[(1, 'Overview'), (2, 'Title'), (3, 'Subtitle'), (4, 'Content'), (5, 'Explanation'), (6, 'Traffic Information'), (7, 'Cautions')], default=2)),
            ],
            bases=('multi_relation.textitem',),
        ),
        migrations.RemoveField(
            model_name='station',
            name='images',
        ),
    ]
