import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Soru

def soru_olustur(soru_metni, gun_farki):
    """
    Belirtilen 'gun_farki' kadar (geçmiş için negatif, gelecek için pozitif) 
    zaman farkıyla bir soru oluşturur.
    """
    zaman = timezone.now() + datetime.timedelta(days=gun_farki)
    return Soru.objects.create(soru_metni=soru_metni, yayin_tarihi=zaman)

class SoruModelTestleri(TestCase):
    def test_yeni_mi_gelecek_tarihli_soru_icin_yanlis_donmeli(self):
        """
        yayin_tarihi gelecekte olan sorular için yeni_mi() False dönmelidir.
        """
        zaman = timezone.now() + datetime.timedelta(days=30)
        gelecek_soru = Soru(yayin_tarihi=zaman)
        self.assertIs(gelecek_soru.yeni_mi(), False)

    def test_yeni_mi_eski_soru_icin_yanlis_donmeli(self):
        """
        yayin_tarihi 1 günden eski olan sorular için yeni_mi() False dönmelidir.
        """
        zaman = timezone.now() - datetime.timedelta(days=1, seconds=1)
        eski_soru = Soru(yayin_tarihi=zaman)
        self.assertIs(eski_soru.yeni_mi(), False)

class SoruIndexViewTestleri(TestCase):
    def test_soru_yoksa_mesaj_gosterilmeli(self):
        """
        Eğer anket yoksa uygun bir mesaj gösterilmelidir.
        """
        response = self.client.get(reverse("anketler:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Henüz bir anket yayınlanmamış.")
        self.assertQuerySetEqual(response.context["son_sorular"], [])

    def test_gecmis_soru_listelenmeli(self):
        """
        Yayın tarihi geçmiş olan sorular ana sayfada görünmelidir.
        """
        soru = soru_olustur(soru_metni="Geçmiş Soru.", gun_farki=-30)
        response = self.client.get(reverse("anketler:index"))
        self.assertQuerySetEqual(response.context["son_sorular"], [soru])

    def test_gelecek_soru_listelenmemeli(self):
        """
        Yayın tarihi gelecekte olan sorular ana sayfada görünmemelidir.
        """
        soru_olustur(soru_metni="Gelecek Soru.", gun_farki=30)
        response = self.client.get(reverse("anketler:index"))
        self.assertContains(response, "Henüz bir anket yayınlanmamış.")
        self.assertQuerySetEqual(response.context["son_sorular"], [])
