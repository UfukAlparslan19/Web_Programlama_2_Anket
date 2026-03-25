from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Soru, Secenek

class IndeksGorunumu(generic.ListView):
    template_name = "anketler/index.html"
    context_object_name = "son_sorular"

    def get_queryset(self):
        return Soru.objects.order_by("-yayin_tarihi")[:5]

class DetayGorunumu(generic.DetailView):
    model = Soru
    template_name = "anketler/detay.html"

class SonucGorunumu(generic.DetailView):
    model = Soru
    template_name = "anketler/sonuclar.html"

def oy_ver(request, soru_id):
    soru = get_object_or_404(Soru, pk=soru_id)
    try:
        secilen_secenek = soru.secenek_set.get(pk=request.POST["secenek_id"])
    except (KeyError, Secenek.DoesNotExist):
        return render(
            request,
            "anketler/detay.html",
            {
                "soru": soru,
                "error_message": "Lütfen bir seçenek belirleyin!",
            },
        )
    else:
        secilen_secenek.oy_sayisi = F("oy_sayisi") + 1
        secilen_secenek.save()
        return HttpResponseRedirect(reverse("anketler:sonuclar", args=(soru.id,)))
