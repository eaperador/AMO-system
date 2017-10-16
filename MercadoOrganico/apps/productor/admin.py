# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EstadoOferta, Oferta
from ..administrador.models import Producto
from ..comun.models import Usuario

class EstadoOfertaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', )
    ordering = ('id',)

class OfertaAdmin(admin.ModelAdmin):
    list_display = ('fecha','get_productor', 'cantidad', 'precio', 'get_estado', 'get_producto')

    def get_estado(self, obj):
        return obj.estado.nombre

    get_estado.short_description = 'Estado'
    get_estado.admin_order_field = 'nombre'

    def get_productor(self, obj):
        return obj.productor.auth_user_id.first_name + " " + obj.productor.auth_user_id.last_name

    get_productor.short_description = 'Productor'
    get_productor.admin_order_field = 'nombre'

    def get_producto(self, obj):
        return obj.producto.nombre

    get_producto.short_description = 'Producto'
    get_producto.admin_order_field = 'nombre'


# Register your models here.

admin.site.register(EstadoOferta, EstadoOfertaAdmin)
admin.site.register(Oferta, OfertaAdmin)