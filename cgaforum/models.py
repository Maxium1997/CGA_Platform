from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse_lazy


from cgaforum.definitions import TopicStatus
from registration.models import User
from multi_relation.models import TaggedItem, Message
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=155, null=False, blank=False)
    slug = models.SlugField()
    remark = models.TextField()

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    f = models.ForeignKey(to=Category, on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=155, null=False, blank=False)
    slug = models.SlugField()
    remark = models.TextField()

    def __str__(self):
        return self.name

    def get_latest_topics(self):
        return self.topic_set.all().order_by('-published_time')[:3]


class Topic(models.Model):
    f = models.ForeignKey(to=SubCategory, on_delete=models.PROTECT, null=False)
    title = models.CharField(max_length=512, unique=True)
    content = models.TextField()
    status = models.PositiveIntegerField(default=TopicStatus.Published.value[0])
    published_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name='Author')
    tags = models.ManyToManyField(to=TaggedItem, related_name='topic_tags')
    replies = GenericRelation(Message)

    def get_absolute_url(self):
        return reverse_lazy('topics', kwargs={'category_slug': self.f.f,
                                              'subcategory_slug': self.f.slug})

    def __str__(self):
        return self.title[:30]
