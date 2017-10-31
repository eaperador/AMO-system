# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt

from ..consumidor.models import ItemCompra, Compra
from ..administrador.models import CatalogoProductos, Producto, ProductoCatalogo
from django.http import JsonResponse, HttpResponse
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