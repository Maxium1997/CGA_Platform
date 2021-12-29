import os
from uuid import uuid4
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from cga_booking.definitions import Usages, ReservationStatus, PaymentStatus, Gender, ContentFlag
from registration.models import User
from multi_relation.models import TextItem, TaggedItem

# Create your models here.


def hotel_upload_path(instance, filename):
    return os.path.join("hotels/{}/{}".format(instance.name,
                                              filename))


def room_upload_path(instance, filename):
    return os.path.join("hotels/{}/{}/{}".format(instance.content_object.belongs2.name,
                                                 instance.content_object.name,
                                                 filename))


class Attraction(TaggedItem):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class InternalPhoto(TextItem):
    path = models.ImageField(upload_to=room_upload_path, null=True, blank=True)

    def __str__(self):
        return self.description[:30]


class Intro(TextItem):
    CONTENT_FLAG_CHOICES = [(_.value[0], _.value[1]) for _ in ContentFlag.__members__.values()]
    content_flag = models.PositiveSmallIntegerField(default=ContentFlag.Content.value[0],
                                                    choices=CONTENT_FLAG_CHOICES)
    sequence = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.description[:30]


class Hotel(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    slug = models.SlugField()
    address = models.CharField(max_length=255, unique=True, null=False, blank=False)
    coordinate = models.CharField(max_length=50, unique=True, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    external_appearance = models.ImageField(upload_to=hotel_upload_path, null=True, blank=True)
    attractions = GenericRelation(Attraction)
    introductions = GenericRelation(Intro)

    def get_overview(self):
        try:
            return self.introductions.filter(content_flag=ContentFlag.Overview.value[0])[0]
        except IndexError:
            return None

    def __str__(self):
        return self.name


class Room(models.Model):
    belongs2 = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    photos = GenericRelation(InternalPhoto)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    single_bed = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    double_bed = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    def people_limit(self):
        return self.single_bed * 1 + self.double_bed * 2

    def __str__(self):
        return self.name
