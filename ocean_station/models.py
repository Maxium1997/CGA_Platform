import os

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from registration.models import User
from ocean_station.definitions import Region, ContentFlag, PhotoFlag
from multi_relation.models import TaggedItem, TextItem

# Create your models here.


def station_upload_path(instance, filename):
    return os.path.join("Ocean_Stations/%s" % instance.content_object.name, filename)


class TaggedAttraction(TaggedItem):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Content(TextItem):
    CONTENT_FLAG_CHOICES = [(_.value[0], _.value[1]) for _ in ContentFlag.__members__.values()]
    content_flag = models.PositiveSmallIntegerField(default=ContentFlag.Content.value[0],
                                                    choices=CONTENT_FLAG_CHOICES)
    sequence = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.description[:30]


class Photo(TextItem):
    title = models.CharField(max_length=255, null=True, blank=True)
    path = models.ImageField(upload_to=station_upload_path, null=True, blank=True)
    PHOTO_FLAG_CHOICES = [(_.value[0], _.value[1]) for _ in PhotoFlag.__members__.values()]
    photo_flag = models.PositiveSmallIntegerField(default=PhotoFlag.Display.value[0],
                                                  choices=PHOTO_FLAG_CHOICES)

    def __str__(self):
        return self.title


class Station(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)     # 管理員

    REGION_CHOICES = [(_.value[0], _.value[1]) for _ in Region.__members__.values()]
    region = models.PositiveIntegerField(default=Region.Unset.value[0],
                                         choices=REGION_CHOICES)                # 地區

    address = models.CharField(max_length=255)                                  # 地址
    coordinate = models.CharField(max_length=22, null=True, blank=True)         # 座標
    contact_phone = models.CharField(max_length=255)                            # 聯絡電話
    fans_page_url = models.URLField(null=True, blank=True)                      # 粉絲專頁網址
    attractions = GenericRelation(TaggedAttraction)                             # 景點
    introductions = GenericRelation(Content)                                    # 海洋驛站相關訊息內容
    album = GenericRelation(Photo)                                              # 相簿

    def get_main_photo(self):
        return self.album.get(photo_flag=PhotoFlag.Main.value[0])

    def __str__(self):
        return self.name
