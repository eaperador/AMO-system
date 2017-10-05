# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..administrador.models import Producto, Productor

# Create your models here.
from django.forms import forms

class EstadoOferta (models.Model):
    descripcion = models.CharField(max_length=100, null=True)
    def __unicode__(self):
        return'{}'.format(self.descripcion)

class Oferta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, editable=False)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    estado = models.ForeignKey(EstadoOferta, null=False)
    producto = models.ForeignKey(Producto, null=False)
    productor = models.ForeignKey(Productor, null=False)

