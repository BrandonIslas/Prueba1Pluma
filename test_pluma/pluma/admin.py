from django.contrib.gis import admin
from .models import Test1, Aerovias

admin.site.register(Test1, admin.OSMGeoAdmin)
admin.site.register(Aerovias, admin.OSMGeoAdmin)
