from django.shortcuts import render, HttpResponse, redirect
from .models import Test1, Aerovias, Corridas
from django.core.serializers import serialize

# Create your views here.
def inicio(request):
    return render(request, "pluma/index.html")

# Create your views here.
def nube(request):
    return render(request, "pluma/nube.html")

def cargar_rutas(request):
    rutas = serialize('geojson',Aerovias.objects.all())
    return HttpResponse(rutas,content_type='json')

def cargar_pluma(request):
    pluma = serialize('geojson',Corridas.objects.all())
    return HttpResponse(pluma,content_type='json')

def index(request):
    return render(request, 'pluma/feed.html')
