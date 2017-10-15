# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Usuario,Rol,Cooperativa

class RolAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', )
    ordering = ('pk',)

class CooperativaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ciudad')
    ordering = ('pk',)

class UsuarioAdmin(admin.ModelAdmin):

    list_display = ('foto','descripcion','telefono','direccion', 'get_rol')
    def get_rol(self, obj):
        return obj.rol.nombre
# Register your models here.
admin.site.register(Rol, RolAdmin),
admin.site.register(Cooperativa, CooperativaAdmin),
admin.site.register(Usuario,UsuarioAdmin)
