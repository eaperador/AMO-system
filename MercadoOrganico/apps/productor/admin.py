# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EstadoOferta, Oferta
from ..administrador.models import Producto, Productor

class EstadoOfertaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'descripcion', )
    ordering = ('pk',)


class OfertaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'get_productor', 'cantidad', 'precio', 'get_estado', 'get_producto')

    def get_estado(self, obj):
        return obj.estado.descripcion

    get_estado.short_description = 'Estado'
    get_estado.admin_order_field = 'descripcion'

    def get_productor(self, obj):
        return obj.productor.nombre + " " + obj.productor.apellido

    get_productor.short_description = 'Productor'
    get_productor.admin_order_field = 'nombre'

    def get_producto(self, obj):
        return obj.producto.nombre

    get_producto.short_description = 'Producto'
    get_producto.admin_order_field = 'nombre'


# Register your models here.

admin.site.register(EstadoOferta, EstadoOfertaAdmin)
admin.site.register(Oferta, OfertaAdmin)