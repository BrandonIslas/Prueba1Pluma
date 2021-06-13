from django.urls import path
from . import views

urlpatterns=[
    path('', views.cargar_rutas, name="cargar_rutas"),
    path('test',views.inicio, name="inicio"),
    path('nube',views.nube, name="nube"),
    path('cargar_rutas',views.cargar_rutas, name="cargar_rutas"),
    path('cargar_pluma',views.cargar_pluma, name="cargar_pluma"),
    path('cargar_puntos',views.cargar_puntos, name="cargar_puntos"),
    path('cargar_afectacion', views.afectacion, name="cargar_afectacion"),
    path('pluma', views.index),
    path('generate_pdf', views.generate_pdf, name="generate_pdf"),
    path('test_archivos', views.subidaArchivos, name="test_archivos"),
    path(
        route = 'index/',
        view = views.index,
        name="pluma"
    ),

    path(
        route = 'pluma/login/',
        view = views.login_view,
        name='login'
        ),

    path(
        route = 'pluma/logout/',
        view = views.logout_view,
        name='logout'
        ),

    path(
        route = 'pluma/signup/',
        view = views.signup_view,
        name = 'signup'
        ),

    path(
        route = 'form/',
        view = views.formulario,
        name="form"
        ),

    path(
        route = 'form2/',
        view = views.formulario2,
        name="form2"
        ),

    path(
        route = 'form3/',
        view = views.formulario3,
        name="form3"
        )
]
