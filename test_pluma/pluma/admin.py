from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis import admin
from .models import Test1, Aerovias, Corridas, Puntos, RutasMulti, RutasIndv
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#Models
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','user')
    list_filter = ('created','modified')

class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )


class PlumaAdmin(LeafletGeoAdmin):
    list_display =('id', 'mpoly')

class AeroviasAdmin(LeafletGeoAdmin):
    list_display=('name', 'geom')

class CorridasAdmin(LeafletGeoAdmin):
    list_display=('id', 'geom')

class PuntosAdmin(LeafletGeoAdmin):
    list_display=('id', 'geom')

class AeroAdmin(LeafletGeoAdmin):
    list_display=('name', 'geom')

class AeroIAdmin(LeafletGeoAdmin):
    list_display=('name', 'geom')


admin.site.register(Test1, PlumaAdmin)
admin.site.register(Aerovias, AeroviasAdmin)
admin.site.register(Corridas, CorridasAdmin)
admin.site.register(Puntos, PuntosAdmin)
admin.site.register(RutasMulti, AeroAdmin)
admin.site.register(RutasIndv, AeroIAdmin)
