# Generated by Django 3.2.9 on 2022-01-22 08:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cgaforum', '0002_auto_20220121_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=ckeditor.fields.RichTextField(default=None),
        ),
    ]
