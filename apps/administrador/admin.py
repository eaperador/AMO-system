# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Producto, Categoria, TipoUnidad

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', )
    ordering = ('id',)

class TipoUnidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','abreviatura' )
    ordering = ('id',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','foto','descripcion','activo','get_categoria','get_tipoUnidad' )

    def get_categoria(self, obj):
        return obj.categoria.nombre

    get_categoria.short_description = 'Categoria'
    get_categoria.admin_order_field = 'nombre'

    def get_tipoUnidad(self, obj):
        return obj.tipoUnidad.abreviatura

    get_tipoUnidad.short_description = 'Tipo Unidad'
    get_tipoUnidad.admin_order_field = 'abreviatura'

# Register your models here.
admin.site.register(TipoUnidad, TipoUnidadAdmin),
admin.site.register(Categoria, CategoriaAdmin),
admin.site.register(Producto, ProductoAdmin)