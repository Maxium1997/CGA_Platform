from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from multi_relation.definitions import Status, PaymentStatus, MessageStatus
from registration.models import User

# Create your models here.


class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = models.Manager()

    def __str__(self):
        return self.tag


class TextItem(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    description = models.TextField(blank=True)      # this object main content

    objects = models.Manager()


class Reservation(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    serial_number = models.CharField(max_length=255, unique=True, null=True)
    price = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='customer')
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    STATUS_CHOICES = [(_.value[0], _.value[1]) for _ in Status.__members__.values()]
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=Status.Pending.value[0])

    PAYMENT_STATUS_CHOICES = [(_.value[0], _.value[1]) for _ in PaymentStatus.__members__.values()]
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS_CHOICES,
                                                      default=PaymentStatus.Unpaid.value[0])

    created_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    f = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    t = GenericForeignKey('content_type', 'object_id')

    STATUS_CHOICES = [(_.value[0], _.value[1]) for _ in MessageStatus.__members__.values()]
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=MessageStatus.Sent.value[0])

    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
