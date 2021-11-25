from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definitions import Gender, Identity, Privilege
# Create your models here.


class User(AbstractUser):
    ID_Number = models.CharField(max_length=10, unique=True, null=True, blank=False)
    ID_Number_is_verify = models.BooleanField(default=False)

    GENDER_CHOICES = [(_.value[0], _.value[1]) for _ in Gender.__members__.values()]
    gender = models.PositiveSmallIntegerField(default=Gender.Unset.value[0],
                                              choices=GENDER_CHOICES)

    IDENTITY_CHOICES = [(_.value[0], _.value[1]) for _ in Identity.__members__.values()]
    identity = models.PositiveSmallIntegerField(default=Identity.Unset.value[0],
                                                choices=IDENTITY_CHOICES)

    PRIVILEGE_CHOICES = [(_.value[0], _.value[1]) for _ in Privilege.__members__.values()]
    privilege = models.PositiveSmallIntegerField(default=Privilege.User.value[0],
                                                 choices=PRIVILEGE_CHOICES)

    email = models.EmailField(unique=True, null=True, blank=False)
    email_is_verify = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=False)
    phone_is_verify = models.BooleanField(default=False)
    birthday = models.DateField(null=True, auto_now=False)
    updated_time = models.DateTimeField(auto_now=True)
    introduction = models.TextField()

