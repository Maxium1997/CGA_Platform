# Generated by Django 3.2.9 on 2022-01-22 08:22

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cga_case', '0006_alter_lr_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='legal_resources',
        ),
        migrations.AddField(
            model_name='case',
            name='legal_resources',
            field=ckeditor.fields.RichTextField(default=None, null=True),
        ),
        migrations.DeleteModel(
            name='LR',
        ),
    ]
