# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from ..administrador.models import CatalogoProductos, Producto, ProductoCatalogo
from ..consumidor.models import ItemCompra, Compra
from django.shortcuts import render
# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
    listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=listaCatalogoProductos[0].id)
    return render(request, "catalogoCompras.html", {'productos':listaProductosCatalogo})

@csrf_exempt
def agregar_producto(request):
    print request.method
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        productoId = jsonOferta['productoId']
        cantidad = jsonOferta['cantidad']
        producto = ProductoCatalogo.objects.get(id=productoId)
        prodAdd = ItemCompra(cantidad=cantidad,
                                 id_producto_catalogo=producto)
        prodAdd.save()
    return JsonResponse({"mensaje": "ok"})

@csrf_exempt
def listar_productos_catalogo_view(request):
    if request.method == 'GET':
        listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
        listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo = listaCatalogoProductos[0].id)
        data_productos_catalogo = [{'id': productoCatalogo.id,
                                    'producto': productoCatalogo.id_producto.nombre,
                                    'foto': str(productoCatalogo.id_producto.foto),
                                    'unidad':productoCatalogo.id_producto.id_tipo_unidad.abreviatura,
                                    'precio': productoCatalogo.precio_definido}for productoCatalogo in listaProductosCatalogo]

    data_convert = json.dumps(data_productos_catalogo,cls=DjangoJSONEncoder)
    return HttpResponse(data_convert)

@csrf_exempt
def select_productos(request):
    if request.method == "GET":
        productos = Producto.objects.filter(activo=True)
        lista_productos = [{'id': producto.id,
                            'nombre': producto.nombre,
                            'descripcion': producto.descripcion,
                            'imagen': str(producto.foto),
                            'activo': producto.activo} for producto in productos]

        data_convert = json.dumps(lista_productos)
        return HttpResponse(data_convert)
