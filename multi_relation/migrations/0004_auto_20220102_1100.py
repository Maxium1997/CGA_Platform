# Generated by Django 3.2.9 on 2022-01-02 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multi_relation', '0003_reservation_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
