from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.site.site_header = "🚀 FormMaster Yönetim Merkezi"
admin.site.site_title = "FormMaster Yönetim Paneli"
admin.site.index_title = "FormMaster Anket ve Veri Yönetimi"

urlpatterns = [
    path("anketler/", include("anketler.urls")),
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="anketler/", permanent=True)), # Ana dizini anketlere yönlendir
]
