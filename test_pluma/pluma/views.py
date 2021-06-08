from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import Test1, Aerovias, Corridas, Puntos
from django.core.serializers import serialize
import pandas as pd
from shapely.geometry import Point, LineString, shape, MultiLineString
import geopandas as gpd
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
from shapely import ops
import numpy as np
import mplleaflet as mpl
from shapely.ops import *
import json
from pathlib import Path


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
    return HttpResponse(pluma, content_type='json')

def cargar_puntos(request):
    puntos = serialize('geojson',Puntos.objects.all())
    return HttpResponse(puntos, content_type='json')

def afectacion(request):
    rutas = serialize('geojson',Aerovias.objects.all())
    pluma = serialize('geojson',Corridas.objects.all())
    #Revision de afectacion
    aero = gpd.read_file(rutas)
    test = gpd.read_file(pluma)
    afectado = []
    for i in range(len(aero)):
        for j in range(len(test)):
            if aero.iloc[i,3].intersection(test.iloc[j,2]).is_empty == False:
                afectado.append(aero.iloc[i,0])
                #aero.iloc[i,1]=0
    consult=list(set(afectado))
    for i in range(0,len(consult)):
        query= Aerovias.objects.get(name=consult[i])
        query.afectado=0
        query.save()

    return HttpResponseRedirect('cargar_rutas')

def index(request):
    return render(request, 'pluma/feed.html')
