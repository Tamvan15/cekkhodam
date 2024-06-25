from django.db import models


# Create your models here.
class khodam(models.Model):
    namaKhodam = models.CharField(max_length=200)
    kekuatanKhodam = models.IntegerField()
    
    def __str__(self):
        return self.namaKhodam

