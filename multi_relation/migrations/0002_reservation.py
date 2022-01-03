# Generated by Django 3.2.9 on 2021-12-31 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('multi_relation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Passed'), (3, 'Failed'), (4, 'Canceled')], default=1)),
                ('payment_status', models.PositiveSmallIntegerField(choices=[(1, 'Unpaid'), (2, 'Paid'), (3, 'Refunded')], default=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
        ),
    ]