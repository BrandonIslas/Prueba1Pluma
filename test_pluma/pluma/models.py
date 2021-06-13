# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class Test1(models.Model):
    id = models.FloatField(primary_key=True)
    mpoly = models.MultiPolygonField(srid=4326)

 # Returns the string representation of the model.
    def __float__(self):
        return self.id

class Aerovias(models.Model):
    name = models.CharField(max_length=80)
    afectado = models.IntegerField()
    geom = models.MultiLineStringField(srid=4326)

    def __str__(self):
        return self.name


class Corridas(models.Model):
    id = models.CharField(max_length=80, primary_key=True)
    capa = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.id

class Puntos(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    nombre = models.CharField(max_length=80)
    aerovia = models.CharField(max_length=80)
    geom = models.MultiPointField(srid=4326)

    def __str__(self):
        return self.nombre

class RutasMulti(models.Model):
    name = models.CharField(max_length=80)
    afectado = models.BigIntegerField()
    geom = models.MultiLineStringField(srid=4326)

    def __str__(self):
        return self.name

class RutasIndv(models.Model):
    name = models.CharField(max_length=80)
    afectado = models.BigIntegerField()
    geom = models.MultiLineStringField(srid=4326)

    def __str__(self):
        return self.name
