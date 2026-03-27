from django.contrib import admin
from .models import Anket, Soru, Secenek

class SecenekInline(admin.TabularInline):
    model = Secenek
    extra = 1

class SoruInline(admin.StackedInline):
    model = Soru
    extra = 1
    show_change_link = True

@admin.register(Anket)
class AnketAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Anket Bilgileri", {"fields": ["baslik", "aciklama"]}),
        ("Tarih Bilgileri", {"fields": ["yayin_tarihi"], "classes": ["collapse"]}),
    ]
    inlines = [SoruInline]
    list_display = ["baslik", "yayin_tarihi", "yeni_mi"]
    list_filter = ["yayin_tarihi"]
    search_fields = ["baslik"]

@admin.register(Soru)
class SoruAdmin(admin.ModelAdmin):
    list_display = ["soru_metni", "anket"]
    inlines = [SecenekInline]
    search_fields = ["soru_metni"]

admin.site.register(Secenek)
