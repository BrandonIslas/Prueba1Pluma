from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Test1, Aerovias, Corridas, Puntos, RutasMulti, RutasIndv

# Auto-generated `LayerMapping` dictionary for Test1 model
test1_mapping = {
    'id': 'id',
    'mpoly': 'MULTIPOLYGON',
}

test_shp = Path(__file__).resolve().parent / 'data' / 'GIS_18000_24925_01.shp'

def run(verbose=True):
    lm = LayerMapping(Test1, str(test_shp), test1_mapping, transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

aerovias_mapping = {
    'name': 'Name',
    'afectado': 'afectado',
    'geom': 'MULTILINESTRING',
}

aerovias_shp = Path(__file__).resolve().parent / 'data' / 'aerovias_mexico.shp'

def run2(verbose=True):
    lma=LayerMapping(Aerovias, str(aerovias_shp), aerovias_mapping, transform=False, encoding='iso-8859-1')
    lma.save(strict=True, verbose=verbose)


corridas_mapping = {
    'id': 'Id',
    'capa': 'Capa',
    'geom': 'MULTIPOLYGON',
}
corridas_shp=Path(__file__).resolve().parent / 'data' / 'pluma_corrida.shp'

def run3(verbose=True):
    lmc=LayerMapping(Corridas, str(corridas_shp), corridas_mapping, transform=False, encoding='iso-8859-1')
    lmc.save(strict=True, verbose=verbose)


puntos_mapping = {
    'latitud': 'Latitud',
    'longitud': 'Longitud',
    'nombre': 'Nombre',
    'aerovia': 'Aerovia',
    'geom': 'MULTIPOINT',
}
puntos_shp=Path(__file__).resolve().parent / 'data' / 'RadioAyudas.shp'

def run4(verbose=True):
    lmp=LayerMapping(Puntos, str(puntos_shp), puntos_mapping, transform=False, encoding='iso-8859-1')
    lmp.save(strict=True, verbose=verbose)

rutasmulti_mapping = {
    'name': 'Name',
    'afectado': 'afectado',
    'geom': 'MULTILINESTRING',
}
aero_shp=Path(__file__).resolve().parent / 'data' / 'aerovias_mexico_F.shp'

def run5(verbose=True):
    lmam=LayerMapping(RutasMulti, str(aero_shp), rutasmulti_mapping, transform=False, encoding='iso-8859-1')
    lmam.save(strict=True, verbose=verbose)

rutasindv_mapping = {
    'name': 'Name',
    'afectado': 'afectado',
    'geom': 'MULTILINESTRING',
}

aeroi_shp=Path(__file__).resolve().parent / 'data' / 'aerovias_mexico_I.shp'

def run6(verbose=True):
    lmai=LayerMapping(RutasIndv, str(aeroi_shp), rutasindv_mapping, transform=False, encoding='iso-8859-1')
    lmai.save(strict=True, verbose=verbose)
