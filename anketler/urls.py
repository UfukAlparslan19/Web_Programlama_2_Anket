from django.urls import path
from . import views

app_name = "anketler"
urlpatterns = [
    path("", views.IndeksGorunumu.as_view(), name="index"),
    path("<int:pk>/", views.DetayGorunumu.as_view(), name="detay"),
    path("<int:pk>/sonuclar/", views.SonucGorunumu.as_view(), name="sonuclar"),
    path("<int:pk>/oy_ver/", views.oy_ver.as_view(), name="oy_ver"),
]
