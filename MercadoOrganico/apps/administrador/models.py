# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Catalogo(models.Model):
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)

class Producto(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=1000)
    imagen = models.ImageField(upload_to='images', null=True)
    estado = models.BooleanField(default=False, null=False)

    def __unicode__(self):
       return "%s" % (self.imagen)

class CatalogoOferta(models.Model):
    precio_definido = models.FloatField()
    cantidad_definida = models.IntegerField()
    catalogo = models.ForeignKey(Catalogo, null=True)
    producto = models.ForeignKey(Producto, null=True)