# Generated by Django 3.2.9 on 2022-01-21 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cga_case', '0003_auto_20220118_0249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lr',
            options={'ordering': ['title']},
        ),
    ]
