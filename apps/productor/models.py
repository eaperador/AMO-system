# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..administrador.models import Producto
from ..comun.models import Usuario
from ..consumidor.models import ItemCompra

class EstadoOferta (models.Model):
    nombre = models.CharField(max_length=100, null=True)
    def __unicode__(self):
        return'{}'.format(self.nombre)

    def natural_key(self):
        return {"nombre":self.nombre}

class CatalogoOfertas (models.Model):
    fecha_inicio = models.DateField(auto_now=False)
    fecha_fin = models.DateField(auto_now=False)
    activo = models.BooleanField(null=False)

class Oferta(models.Model):
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    cantidad_disponible = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True, editable=False)
    id_estado_oferta = models.ForeignKey(EstadoOferta, null=False)
    id_productor = models.ForeignKey(Usuario, null=False)
    id_producto = models.ForeignKey(Producto, null=False)
    id_catalogo_oferta = models.ForeignKey(CatalogoOfertas, null=False)
    #fechaFormat = fecha.strftime('%Y-%m-%d %H:%M')


    #natural_key.dependencies = ['estado','']

