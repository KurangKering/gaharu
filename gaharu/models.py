from django.db import models
from django_pandas.managers import DataFrameManager
# Create your models here.


class Dataset(models.Model):
    filename = models.ImageField(upload_to="uploads")
    form_factor = models.FloatField(null=True, blank=True)
    aspect_ratio = models.FloatField(null=True, blank=True)
    rect = models.FloatField(null=True, blank=True)
    narrow_factor = models.FloatField(null=True, blank=True)
    prd = models.FloatField(null=True, blank=True)
    plw = models.FloatField(null=True, blank=True)
    idm = models.FloatField(null=True, blank=True)
    entropy = models.FloatField(null=True, blank=True)
    asm = models.FloatField(null=True, blank=True)
    contrast = models.FloatField(null=True, blank=True)
    correlation = models.FloatField(null=True, blank=True)
    kelas = models.IntegerField(null=True, blank=True)
    is_extracted = models.CharField(max_length=1, null=True, blank=True)
    pdobjects = DataFrameManager()


class Model(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    filename = models.FileField(upload_to="models")
    datalatih_ids = models.TextField(null=True, blank=True)
    datauji_ids = models.TextField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    




