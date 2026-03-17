from django.db import models
from django.utils import timezone
import datetime

class Soru(models.Model):
    soru_metni = models.CharField(max_length=200)
    yayin_tarihi = models.DateTimeField("Yayınlanma Tarihi")

    def __str__(self):
        return self.soru_metni

    def yeni_mi(self):
        return self.yayin_tarihi >= timezone.now() - datetime.timedelta(days=1)

class Secenek(models.Model):
    soru = models.ForeignKey(Soru, on_delete=models.CASCADE)
    secenek_metni = models.CharField(max_length=200)
    oy_sayisi = models.IntegerField(default=0)

    def __str__(self):
        return self.secenek_metni
