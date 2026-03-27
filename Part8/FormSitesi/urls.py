from django.contrib import admin
from django.urls import include, path
from django.conf import settings

# Admin Paneli Başlıklarını Özelleştiriyoruz
admin.site.site_header = "🚀 FormMaster Yönetim Merkezi"
admin.site.site_title = "FormMaster Yönetim Paneli"
admin.site.index_title = "FormMaster Anket ve Veri Yönetimi"

urlpatterns = [
    # anketler/ rotasını buraya ekliyoruz!
    path("anketler/", include("anketler.urls")),
    path("admin/", admin.site.urls),
]

# Eğer DEBUG modundaysak Debug Toolbar'ı aktif et
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
