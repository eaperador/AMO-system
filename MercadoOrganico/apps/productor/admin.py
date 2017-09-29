# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EstadoOferta, Oferta


class EstadoOfertaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'descripcion', )
    ordering = ('pk',)


class OfertaAdmin(admin.ModelAdmin):
    list_display = ('cantidad', 'precio', 'get_estado')


    def get_estado(self, obj):
        return obj.estado.descripcion

    get_estado.short_description = 'Estado'
    get_estado.admin_order_field = 'descripcion'




# Register your models here.

admin.site.register(EstadoOferta, EstadoOfertaAdmin)
admin.site.register(Oferta, OfertaAdmin)