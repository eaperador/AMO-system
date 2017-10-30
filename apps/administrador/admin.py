# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Producto, Categoria, TipoUnidad, CatalogoProductos, ProductoCatalogo

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', )
    ordering = ('id',)

class TipoUnidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','abreviatura' )
    ordering = ('id',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','foto','descripcion','activo','get_categoria','get_tipoUnidad' )

    def get_categoria(self, obj):
        return obj.id_categoria.nombre

    get_categoria.short_description = 'Categoria'
    get_categoria.admin_order_field = 'nombre'

    def get_tipoUnidad(self, obj):
        return obj.id_tipo_unidad.abreviatura

    get_tipoUnidad.short_description = 'Tipo Unidad'
    get_tipoUnidad.admin_order_field = 'abreviatura'

class CatalogoProductosAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'activo')

#class ProductoCatalogo(models.Model):
#    precio_definido = models.FloatField()
#    cantidad_definida = models.IntegerField()
#    cantidad_disponible = models.IntegerField()
#    id_producto = models.ForeignKey(Producto, null=False)
#    id_catalogo = models.ForeignKey(CatalogoProductos, null=False)

class ProductoCatalogoAdmin (admin.ModelAdmin):
    list_display = ('precio_definido','cantidad_definida','cantidad_disponible','get_producto','get_catalogo')

    def get_producto(self, obj):
        return obj.id_producto.nombre

    get_producto.short_description = 'Producto'
    get_producto.admin_order_field = 'nombre'

    def get_catalogo(self, obj):
        return obj.id_catalogo.id

    get_catalogo.short_description = 'Catalogo'
    get_catalogo.admin_order_field = 'id'

# Register your models here.
admin.site.register(TipoUnidad, TipoUnidadAdmin),
admin.site.register(Categoria, CategoriaAdmin),
admin.site.register(Producto, ProductoAdmin),
admin.site.register(CatalogoProductos, CatalogoProductosAdmin),
admin.site.register(ProductoCatalogo, ProductoCatalogoAdmin)