from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis import admin
from .models import Test1, Aerovias, Corridas


class PlumaAdmin(LeafletGeoAdmin):
    list_display =('id', 'mpoly')

class AeroviasAdmin(LeafletGeoAdmin):
    list_display=('name', 'geom')

class CorridasAdmin(LeafletGeoAdmin):
    list_display=('id', 'geom')


admin.site.register(Test1, PlumaAdmin)
admin.site.register(Aerovias, AeroviasAdmin)
admin.site.register(Corridas, CorridasAdmin)
