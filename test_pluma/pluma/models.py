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
