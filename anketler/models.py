import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Anket(models.Model):
    baslik = models.CharField("Anket Başlığı", max_length=200)
    aciklama = models.TextField("Açıklama", blank=True, null=True)
    yayin_tarihi = models.DateTimeField("Yayınlanma Tarihi", default=timezone.now)

    def __str__(self):
        return self.baslik

    @admin.display(
        boolean=True,
        ordering="yayin_tarihi",
        description="Yeni mi?",
    )
    def yeni_mi(self):
        simdi = timezone.now()
        return simdi - datetime.timedelta(days=1) <= self.yayin_tarihi <= simdi

class Soru(models.Model):
    anket = models.ForeignKey(Anket, on_delete=models.CASCADE, related_name="sorular")
    soru_metni = models.CharField(max_length=200)

    def __str__(self):
        return self.soru_metni

class Secenek(models.Model):
    soru = models.ForeignKey(Soru, on_delete=models.CASCADE, related_name="secenekler")
    secenek_metni = models.CharField(max_length=200)
    oy_sayisi = models.IntegerField(default=0)

    def __str__(self):
        return self.secenek_metni
