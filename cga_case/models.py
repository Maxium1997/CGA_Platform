import os
from django.db import models
from django.urls import reverse_lazy
from tinymce.models import HTMLField

# Create your models here.


class CaseCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CaseSection(models.Model):
    is_part_of = models.ForeignKey(CaseCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def case_flow_chart_upload_path(instance, filename):
    return os.path.join("Case/{}/{}".format(instance, (str(instance.serial_number)+"_"+str(instance.title)+"_"+filename)))


class Case(models.Model):
    is_one_of = models.ForeignKey(CaseSection, on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255, unique=True, null=False)
    legal_resources = HTMLField(default=None, null=True)
    handling_point = HTMLField(default=None, null=True)
    cautions = HTMLField(default=None, null=True)
    flow_chart = models.ImageField(upload_to=case_flow_chart_upload_path, null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('case_update', kwargs={'case_title': self.title})

    def __str__(self):
        return self.title
