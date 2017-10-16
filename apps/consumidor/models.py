# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..administrador.models import CatalogoOferta
from ..comun.models import Usuario

class CompraProducto(models.Model):
    estado = models.CharField(max_length=100)
    id_catalogoProducto = models.ForeignKey(CatalogoOferta, null=False)

class Compra(models.Model):
    fecha_compra = models.DateTimeField(auto_now_add=True, editable=False)
    valor_total = models.FloatField()
    fecha_entrega = models.DateTimeField(auto_now_add=True, editable=False)
    id_compraProducto = models.ForeignKey(CompraProducto, null=False)
    id_comprador = models.ForeignKey(Usuario, null=False)

class MedioPago(models.Model):
    nombre = models.CharField(max_length=100)
    id_comprador = models.ForeignKey(Usuario, null=False)