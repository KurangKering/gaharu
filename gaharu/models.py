from django.db import models
from django_pandas.managers import DataFrameManager
# Create your models here.
import json

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
    filename = models.FileField(upload_to="models")
    datalatih_ids = models.TextField(null=True, blank=True)
    datauji_ids = models.TextField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    epoch = models.IntegerField(null=True, blank=True, default=1)
    
    @property
    def jumlah_data_latih(self):
        json_datalatih_ids = json.loads(self.datalatih_ids)

        return  len(json_datalatih_ids)

    @property
    def jumlah_data_uji(self):
        json_datauji_ids = json.loads(self.datauji_ids)

        return  len(json_datauji_ids)




