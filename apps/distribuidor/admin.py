# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Entrega, Ruta

class EntregaAdmin(admin.ModelAdmin):
    list_display = ('estado', 'get_id_ruta')

    def get_id_ruta(self, obj):
            return obj.get_id_ruta.id

class RutaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'get_id_usuario_distribuidor')

    def get_id_usuario_distribuidor(self, obj):
        return obj.id_usuario_distribuidor.id


# Register your models here.
admin.site.register(Entrega, EntregaAdmin),
admin.site.register(Ruta, RutaAdmin)
