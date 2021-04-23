from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis import admin
from .models import Test1, Aerovias


class PlumaAdmin(LeafletGeoAdmin):
    list_display =('id', 'mpoly')

class AeroviasAdmin(LeafletGeoAdmin):
    list_display=('name', 'geom')


admin.site.register(Test1, PlumaAdmin)
admin.site.register(Aerovias, AeroviasAdmin)
