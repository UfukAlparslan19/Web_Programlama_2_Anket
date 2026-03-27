from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Anket, Soru, Secenek

class IndeksGorunumu(generic.ListView):
    template_name = "anketler/index.html"
    context_object_name = "anket_listesi"

    def get_queryset(self):
        return Anket.objects.filter(yayin_tarihi__lte=timezone.now()).order_by("-yayin_tarihi")

class DetayGorunumu(generic.DetailView):
    model = Anket
    template_name = "anketler/detay.html"

    def get_queryset(self):
        return Anket.objects.filter(yayin_tarihi__lte=timezone.now())

class SonucGorunumu(generic.DetailView):
    model = Anket
    template_name = "anketler/sonuclar.html"

class oy_ver(generic.View):
    def post(self, request, pk):
        anket = get_object_or_404(Anket, pk=pk)
        hata = False
        secilen_secenekler = []

        for soru in anket.sorular.all():
            secenek_id = request.POST.get(f"soru_{soru.id}")
            if not secenek_id:
                hata = True
                break
            try:
                secilen_secenek = soru.secenekler.get(pk=secenek_id)
                secilen_secenekler.append(secilen_secenek)
            except (KeyError, Secenek.DoesNotExist):
                hata = True
                break

        if hata:
            return render(
                request,
                "anketler/detay.html",
                {
                    "anket": anket,
                    "error_message": "Lütfen tüm soruları cevaplayın!",
                },
            )
        else:
            for secenek in secilen_secenekler:
                secenek.oy_sayisi = F("oy_sayisi") + 1
                secenek.save()
            
            messages.success(request, "Anket başarıyla tamamlandı, teşekkürler!")
            return HttpResponseRedirect(reverse("anketler:sonuclar", args=(anket.id,)))
