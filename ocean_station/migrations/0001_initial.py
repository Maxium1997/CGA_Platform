# Generated by Django 3.2.9 on 2021-11-25 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ocean_station.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('multi_relation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('textitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='multi_relation.textitem')),
                ('content_flag', models.PositiveSmallIntegerField(default=4)),
            ],
            bases=('multi_relation.textitem',),
        ),
        migrations.CreateModel(
            name='TaggedAttraction',
            fields=[
                ('taggeditem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='multi_relation.taggeditem')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            bases=('multi_relation.taggeditem',),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to=ocean_station.models.station_upload_path)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('region', models.PositiveIntegerField(default=0)),
                ('address', models.CharField(max_length=255)),
                ('coordinate', models.CharField(blank=True, max_length=22, null=True)),
                ('contact', models.CharField(max_length=255)),
                ('fans_page_url', models.URLField(blank=True, null=True)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]