from django.http import HttpResponse

def index(request):
    return HttpResponse("Merhaba, Sınav Projesi - Anketler Sayfası'ndasınız (Part 1)")
