# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import MedioPago

class MedioPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_usuario_comprador')

    def get_usuario_comprador(self, obj):
        return obj.id_usuario_comprador.id

# Register your models here.
admin.site.register(MedioPago, MedioPagoAdmin)
