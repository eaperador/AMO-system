# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..administrador.models import ProductoCatalogo
from ..comun.models import Usuario, Direccion
from ..distribuidor.models import Entrega

class MedioPago(models.Model):
    nombre = models.CharField(max_length=100)
    id_usuario_comprador = models.ForeignKey(Usuario, null=False)

class Compra(models.Model):
    fecha_compra = models.DateTimeField(auto_now_add=True, editable=False)
    valor_total = models.FloatField()
    cantidad_items = models.IntegerField()
    fecha_entrega = models.DateTimeField(auto_now_add=True, editable=False)
    id_usuario_comprador = models.ForeignKey(Usuario, null=False)
    id_direccion_compra = models.ForeignKey(Direccion, null=False)
    id_entrega = models.ForeignKey(Entrega, null=False)
    id_medio_pago = models.ForeignKey(MedioPago, null=False)

class ItemCompra(models.Model):
    cantidad = models.IntegerField()
    id_producto_catalogo = models.ForeignKey(ProductoCatalogo, null=False)
    id_compra = models.ForeignKey(Compra, null=False)

class Carrito(models.Model):
    valor_total = models.FloatField()
    cantidad_items = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now=True, editable=False)

class ItemCarrito(models.Model):
    cantidad = models.IntegerField()
    id_producto_catalogo = models.ForeignKey(ProductoCatalogo, null=False)
    id_carrito = models.ForeignKey(Carrito, null=False)
