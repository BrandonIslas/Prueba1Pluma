from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Test1

# Auto-generated `LayerMapping` dictionary for Test1 model
test1_mapping = {
    'id': 'id',
    'mpoly': 'MULTIPOLYGON',
}

test_shp = Path(__file__).resolve().parent / 'data' / 'GIS_18000_24925_01.shp'

def run(verbose=True):
    lm = LayerMapping(Test1, str(test_shp), test1_mapping, transform=True)
    lm.save(strict=True, verbose=verbose)
