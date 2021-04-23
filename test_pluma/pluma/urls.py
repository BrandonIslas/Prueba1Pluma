from django.urls import path
from . import views

urlpatterns=[
    path('',views.inicio, name="inicio"),
    path('nube',views.nube, name="nube"),
    path('cargar_rutas',views.cargar_rutas, name="cargar_rutas"),
    path('cargar_pluma',views.cargar_pluma, name="cargar_pluma"),
    path('pluma', views.index),
]
