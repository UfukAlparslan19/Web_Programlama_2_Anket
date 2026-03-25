from django.contrib import admin
from .models import Soru, Secenek

class SecenekInline(admin.TabularInline):
    model = Secenek
    extra = 3

class SoruAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Soru Metni", {"fields": ["soru_metni"]}),
        ("Tarih Bilgisi", {"fields": ["yayin_tarihi"], "classes": ["collapse"]}),
    ]
    inlines = [SecenekInline]
    list_display = ["soru_metni", "yayin_tarihi", "yeni_mi"]
    list_filter = ["yayin_tarihi"]
    search_fields = ["soru_metni"]

admin.site.register(Soru, SoruAdmin)
