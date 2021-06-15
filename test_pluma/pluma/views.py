from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Test1, Aerovias, Corridas, Puntos, RutasMulti, RutasIndv, Archivos
from .forms import SubidaArchivosForm
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
import requests
import urllib
from django.template import RequestContext
import networkx as nx
from geopandas import GeoDataFrame

# Models
from django.contrib.auth.models import User
#from Webforms.models import Profile

# Forms
from pluma.forms import SignupForm

#AUTOMATION CODE
s = requests.Session()
s.auth = ('jjimeneze@ipn.mx', 'Alexandro04')


# Create your views here.
def inicio(request):
    return render(request, "pluma/pdf.html")

# Create your views here.
def nube(request):
    return render(request, "pluma/nube.html")
# Create your views here.
def optima(request):
    return render(request, "pluma/ruta_optima.html")

def cargar_rutas(request):
    rutas = serialize('geojson',RutasIndv.objects.all())
    return HttpResponse(rutas,content_type='json')

def cargar_pluma(request):
    pluma = serialize('geojson',Corridas.objects.all())
    return HttpResponse(pluma, content_type='json')

def cargar_puntos(request):
    puntos = serialize('geojson',Puntos.objects.all())
    return HttpResponse(puntos, content_type='json')

def afectacion(request):
    rutas = serialize('geojson',RutasIndv.objects.all())
    pluma = serialize('geojson',Corridas.objects.all())
    #Revision de afectacion
    aero = gpd.read_file(rutas)
    test = gpd.read_file(pluma)
    afectado = []
    print(list(aero))
    for i in range(len(aero)):
        for j in range(len(test)):
            if aero.iloc[i,3].intersection(test.iloc[j,2]).is_empty == False:
                afectado.append(aero.iloc[i,0])
                #aero.iloc[i,1]=0
    consult=list(set(afectado))
    print(consult)
    for i in range(0,len(consult)):
        query= RutasIndv.objects.get(name=consult[i])
        query.afectado=0
        query.save()

    return HttpResponseRedirect('cargar_rutas')

def index(request):
    return render(request, 'pluma/feed.html')

def link_call(uri, rel):
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
    rutas = serialize('geojson',RutasIndv.objects.all())
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
        query= RutasIndv.objects.get(name=consult[i])
        coordenadas.append(query.geom.coords)
    optimo = []
    for i in range(len(aero)):
        if(aero.loc[i][1] == 2):
            optimo.append(aero.iloc[i, 0])
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
    'Ruta_Optima': optimo,
    'imagen1': Path(__file__).resolve().parent / 'media' / 'pdf' / 'test.png',
    'imagen2': Path(__file__).resolve().parent / 'media' / 'pdf' / 'ima.png'}
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('pluma')
        else:
            print("HOLA PPASOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            return render(request, 'pluma/login.html', {'error': 'Invalid username and password'})

    return render(request, 'pluma/login.html')


def signup_view(request):
    """Sign up view."""
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        print("123456789")
        form = SignupForm()

    return render(
        request=request,
        template_name='pluma/signup.html',
        context={'form': form}
    )

@login_required
def logout_view(request):
    """Logout a user."""
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request, 'pluma/feed.html')

def formulario(request):
    #missing line using model <<here>>
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        #form = PlumaForm(request.POST)
        #if form.is_valid():
        return redirect(request, 'Pluma/pluma_form2.html')
    else:

        r = s.get("https://www.ready.noaa.gov/hyreg-bin/dispsrc.pl?category=Volcanic_ash",auth=('jjimeneze@ipn.mx', 'Alexandro04'))
        return render(request, 'Pluma/pluma_form.html')

def formulario2(request):
    import pdb; pdb.set_trace()
    if request.method == 'POST':
        #r=s.post("https://www.ready.noaa.gov/hyreg-bin/disptype.pl",auth=('jjimeneze@ipn.mx', 'Alexandro04'))
        return render(request, 'Pluma/pluma_form2.html')
    else:
        return render(request, 'Pluma/pluma_form2.html')

def formulario3(request):
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        #print(request)
        return render(request, 'Pluma/pluma_form3.html')
    else:
        return render(request, 'Pluma/pluma_form3.html')

def subidaArchivos(request):
    form = SubidaArchivosForm(data=request.POST or None, files= request.FILES or None )
    context={
        "form": form
    }
    if form.is_valid():
        form.save()
        archivo_shp= form.cleaned_data.get("archivo_shp")
        archivo_sdbf= form.cleaned_data.get("archivo_sdbf")
        archivo_shx= form.cleaned_data.get("archivo_shx")
        archivo_prj= form.cleaned_data.get("archivo_prj")
        archivo_cpg= form.cleaned_data.get("archivo_cpg")
        rutas = serialize('geojson',RutasIndv.objects.all())
        #Revision de afectacion
        aero = gpd.read_file(rutas)
        afectado = []
        for i in range(len(aero)):
            if(aero.loc[i][1] == 2 or  aero.loc[i][1] == 0):
                afectado.append(aero.iloc[i, 0])
        print(afectado)
        for i in range(len(afectado)):
            query= RutasIndv.objects.get(name=afectado[i])
            query.afectado=1
            query.save()
        return redirect('nube')

    return render(request, "pluma/prueba.html", context)

def RutaOptima(request):
    form = OrigenDestinoForm(data=request.POST or None, files= request.FILES or None )
    context={
        "form": form
    }
    if form.is_valid():
        origen= form.cleaned_data.get("origen")
        destino= form.cleaned_data.get("destino")
    rutas = serialize('geojson',RutasIndv.objects.all())
    pluma = serialize('geojson',Corridas.objects.all())
    #Leemos shapefile
    df2=gpd.read_file(rutas)
    filasshape=df2.shape[0]

    #Creatmos el dataframe a partir del archivo xls y obtenemos el número filas
    df = pd.read_excel('pluma/dataset-dijkstra.xlsx')
    filas=df.shape[0]

    #Dataframe original
    dfdatos = pd.read_excel('pluma/aero.xls')
    filasdatos = dfdatos.shape[0]


    nuevopeso=pd.DataFrame()
    nuevopeso=nuevopeso.assign(Nombre=None)
    nuevopeso=nuevopeso.assign(Nombre2=None)

    print(df2.head())

    nombrepeso1=""
    nombrepeso2=""
    conpeso=0

    for i in range (filasshape):

        afectado = df2.iloc[i,1]

        if(afectado==0):

            linea=df2.iloc[i,3]
            #print(list(linea[0].coords))
            coordsradio = list(linea[0].coords)

            latradio1 = coordsradio[0][1];
            lonradio1 = coordsradio[0][0];

            latradio1=round(latradio1,10)
            lonradio1=round(lonradio1,10)

            latradio2 = coordsradio[1][1];
            lonradio2 = coordsradio[1][0];

            latradio2=round(latradio2,10)
            lonradio2=round(lonradio2,10)
            #print(latradio1, lonradio1)
            bandera=0;

            for j in range (filasdatos):

                item1 = np.float64(dfdatos.loc[j][0])
                latpeso = round(item1.item(),10)

                item2 = np.float64(dfdatos.loc[j][1])
                lonpeso = round(item2.item(),10)

                if (latpeso==latradio1 and lonpeso==lonradio1):
                    print("XDDDDDD")
                    nombrepeso1= dfdatos.loc[j][4]
                    break

            for j in range (filasdatos):

                item1 = np.float64(dfdatos.loc[j][0])
                latpeso = round(item1.item(),10)

                item2 = np.float64(dfdatos.loc[j][1])
                lonpeso = round(item2.item(),10)

                if (latpeso==latradio2 and lonpeso==lonradio2):
                    print("XDDDDDD2")
                    nombrepeso2= dfdatos.loc[j][4]
                    break

            nuevopeso.loc[conpeso] = [nombrepeso1, nombrepeso2]
            conpeso += 1


    print(nuevopeso)
    filasnuevopeso = nuevopeso.shape[0]

    for i in range(filasnuevopeso):
        nombremodificar1 = nuevopeso.loc[i][0]
        nombremodificar2 = nuevopeso.loc[i][1]

        for j in range(filas):
            radio1 = df.loc[j][0]
            radio2 = df.loc[j][1]

            if(nombremodificar1 == radio1 and nombremodificar2 == radio2 ):
                df.iloc[j,2]=50000
                break
            elif(nombremodificar1 == radio2 and nombremodificar2 == radio1 ):
                df.iloc[j, 2] = 50000
                break

    print(df)
    #Creamos la lista de vértices o el grafo.
    espacioAereo = nx.from_pandas_edgelist(df,source='Aero1',target='Aero2',edge_attr='Peso')

    print("Posibilidades")
    #print(espacioAereo.edges())
    print("\n")

    datafinal=pd.DataFrame()
    datafinal=datafinal.assign(Nombre=None)
    datafinal=datafinal.assign(Latitud=None)
    datafinal=datafinal.assign(Longitud=None)

    try:
        djk_path=nx.dijkstra_path(espacioAereo, source='UJ33-16', target='UJ33-18', weight='Peso')
        djknum=len(djk_path)

        bandera=0;
        for i in range(djknum):
            if(bandera==1):
                break
            nombreRA = djk_path[i]
            for j in range(filasnuevopeso):
                nombreafectado1 = nuevopeso.loc[j][0]
                nombreafectado2 = nuevopeso.loc[j][1]

                if(nombreRA == nombreafectado1 or nombreRA == nombreafectado2 ):
                    bandera=1
                    break


        if (bandera == 1):
            print("No existe una ruta alterna para el origen y destino seleccionados")
        else:

            contador = 0
            for i in range(djknum):
                for j in range(filasdatos):

                    if (djk_path[i] == dfdatos.loc[j][4]):
                        nomb = djk_path[i]
                        lat = dfdatos.loc[j][0]
                        lon = dfdatos.loc[j][1]
                        datafinal.loc[contador] = [nomb, lat, lon]
                        contador += 1
                        break

            print(datafinal)

            for i in range(djknum-1):

                item1 = np.float64(datafinal.loc[i][1])
                latnat1 = item1.item()

                item2 = np.float64(datafinal.loc[i][2])
                lonnat1 = item2.item()

                item1 = np.float64(datafinal.loc[i+1][1])
                latnat2 = item1.item()

                item2 = np.float64(datafinal.loc[i+1][2])
                lonnat2 = item2.item()

                latnat1=round(latnat1,6)
                lonnat1=round(lonnat1,6)

                latnat2=round(latnat2,6)
                lonnat2=round(lonnat2,6)


                for j in range(filasshape):
                    linea=df2.iloc[j,3]
                    #print(list(linea[0].coords))
                    coordsradio = list(linea[0].coords)

                    latradio1 = coordsradio[0][1];
                    lonradio1 = coordsradio[0][0];
                    latradio1=round(latradio1,6)
                    lonradio1=round(lonradio1,6)

                    latradio2 = coordsradio[1][1];
                    lonradio2 = coordsradio[1][0];
                    latradio2=round(latradio2,6)
                    lonradio2=round(lonradio2,6)


                    if (latnat1 == latradio1 and lonnat1 == lonradio1):
                        if(latnat2 == latradio2 and lonnat2 == lonradio2):
                            df2.iloc[j, 1] = 2

                    elif (latnat1 == latradio2 and lonnat1 == lonradio2):
                        if (latnat2 == latradio1 and lonnat2 == lonradio1):
                            df2.iloc[j, 1] = 2
            print(djk_path)
            afectado = []
            for i in range(len(df2)):
                if(df2.loc[i][1] == 2):
                    afectado.append(df2.iloc[i, 0])
            print(afectado)
            for i in range(len(afectado)):
                query= RutasIndv.objects.get(name=afectado[i])
                query.afectado=2
                query.save()
            df2.to_excel(r'rutaalterna.xlsx', index=False)
    except Exception as E:
        return HttpResponseRedirect('cargar_rutas')
        print(E)
    return HttpResponseRedirect('cargar_rutas')
