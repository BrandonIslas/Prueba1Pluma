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
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings


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

def link_callback(uri, rel):
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
        else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

            # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
        return path

def generate_pdf(request):
    template = get_template('pluma/pdf.html')
    rutas = serialize('geojson',Aerovias.objects.all())
    pluma = serialize('geojson',Corridas.objects.all())
    punt= serialize('geojson',Puntos.objects.all())
    #Revision de afectacion
    aero = gpd.read_file(rutas)
    test = gpd.read_file(pluma)
    puntos= gpd.read_file(punt)
    afectado = []
    coordenadas =[]
    for i in range(len(aero)):
        for j in range(len(test)):
            if aero.iloc[i,3].intersection(test.iloc[j,2]).is_empty == False:
                afectado.append(aero.iloc[i,0])
                #aero.iloc[i,1]=0
    consult=list(set(afectado))
    for i in range(0,len(consult)):
        query= Aerovias.objects.get(name=consult[i])
        coordenadas.append(query.geom.coords)
    plt.style.use('dark_background')
    figsize= (50,40)
    test.plot(cmap='plasma')
    plt.savefig('/home/brandon/Documentos/TT/Pruebas/test_pluma/pluma/media/pdf/test.png', bbox_inches='tight')
    mapa= puntos.plot(color='#011f4b', linewidth=0.05, figsize=figsize)
    aero.plot(ax=mapa, color='#ffffff', markersize=0.5)
    test.plot(cmap='plasma',ax=mapa)
    plt.savefig('/home/brandon/Documentos/TT/Pruebas/test_pluma/pluma/media/pdf/ima.png', bbox_inches='tight')

    context={'Rutas_Afectadas': consult,
    'Coordenadas_Afectadas': coordenadas,
    'imagen1': '{}{}'.format(settings.MEDIA_URL, 'test.png')}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,
       link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
