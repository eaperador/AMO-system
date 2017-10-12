# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..administrador.models import Producto
from ..comun.models import Usuario

from django.forms import forms

class EstadoOferta (models.Model):
    nombre = models.CharField(max_length=100, null=True)
    def __unicode__(self):
        return'{}'.format(self.nombre)

    def natural_key(self):
        return {"nombre":self.nombre}

class Oferta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, editable=False)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    estado = models.ForeignKey(EstadoOferta, null=False)
    producto = models.ForeignKey(Producto, null=False)
    productor = models.ForeignKey(Usuario, null=False)
    #fechaFormat = fecha.strftime('%Y-%m-%d %H:%M')
    def natural_key(self):
        return {"precio":self.precio,
                "cantidad":self.cantidad,
                "fecha":self.fechaFormat,
                "estado":self.estado.natural_key(),
                "producto":self.producto.natural_key()}

    #natural_key.dependencies = ['estado','']