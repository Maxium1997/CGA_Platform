# Generated by Django 3.2.9 on 2022-01-09 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multi_relation', '0004_auto_20220102_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('slug', models.SlugField()),
                ('remark', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('slug', models.SlugField()),
                ('remark', models.TextField()),
                ('f', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cgaforum.category')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('status', models.PositiveIntegerField(default=1)),
                ('published_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('f', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cgaforum.subcategory')),
                ('tags', models.ManyToManyField(related_name='topic_tags', to='multi_relation.TaggedItem')),
            ],
        ),
    ]