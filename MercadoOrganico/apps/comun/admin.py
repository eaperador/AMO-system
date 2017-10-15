# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Usuario,Rol,Cooperativa

class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', )
    ordering = ('id',)

class CooperativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'ciudad')
    ordering = ('id',)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('foto','descripcion','telefono','direccion')

# Register your models here.
admin.site.register(Rol, RolAdmin),
admin.site.register(Cooperativa, CooperativaAdmin),
admin.site.register(Usuario,UsuarioAdmin)
