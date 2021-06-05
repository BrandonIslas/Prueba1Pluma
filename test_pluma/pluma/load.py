from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Test1, Aerovias, Corridas

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
