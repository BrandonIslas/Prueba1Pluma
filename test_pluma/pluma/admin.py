from django.contrib.gis import admin
from .models import Test1

admin.site.register(Test1, admin.OSMGeoAdmin)
