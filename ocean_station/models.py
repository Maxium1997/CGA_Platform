import os

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from registration.models import User
from ocean_station.definitions import Region, ContentFlag
from multi_relation.models import TaggedItem, TextItem

# Create your models here.


def station_upload_path(instance, filename):
    return os.path.join("Ocean_Stations/%s" % instance.name, filename)


class TaggedAttraction(TaggedItem):
    name = models.CharField(max_length=10, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Content(TextItem):
    content_flag = models.PositiveSmallIntegerField(default=ContentFlag.Content.value[0])

    def __str__(self):
        return self.description[:30]


class Station(models.Model):
    images = models.ImageField(upload_to=station_upload_path, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)     # 管理員
    region = models.PositiveIntegerField(default=Region.Unset.value[0])         # 地區
    address = models.CharField(max_length=255)                                  # 地址
    coordinate = models.CharField(max_length=22, null=True, blank=True)         # 座標
    contact = models.CharField(max_length=255)                                  # 聯絡電話
    fans_page_url = models.URLField(null=True, blank=True)                      # 粉絲專頁網址
    attractions = GenericRelation(TaggedAttraction)                             # 景點
    introductions = GenericRelation(Content)

    def __str__(self):
        return self.name
