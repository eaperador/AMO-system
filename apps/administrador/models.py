# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CatalogoProductos(models.Model):
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    activo = models.BooleanField(null=False)

class TipoUnidad(models.Model):
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=5)

    def __unicode__(self):
       return '{}'.format(self.abreviatura)

    def natural_key(self):
        return {"abreviatura":self.abreviatura}

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
       return "%s" % (self.nombre)

class Producto(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=1000)
    foto = models.ImageField(upload_to='images', null=True)
    activo = models.BooleanField(default=False, null=False)
    id_tipo_unidad = models.ForeignKey(TipoUnidad, null=False)
    id_categoria = models.ForeignKey(Categoria, null=False)

    def __unicode__(self):
       return "%s" % (self.nombre)

    def natural_key(self):
        return {"nombre" : self.nombre, "unidad": self.tipoUnidad.natural_key()}

class ProductoCatalogo(models.Model):
    precio_definido = models.FloatField()
    cantidad_definida = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    id_producto = models.ForeignKey(Producto, null=False)
    id_catalogo = models.ForeignKey(CatalogoProductos, null=False)

