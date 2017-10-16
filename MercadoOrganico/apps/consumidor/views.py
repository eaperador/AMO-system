# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt
from ..administrador.models import CatalogoOferta
from django.http import JsonResponse
from models import CompraProducto
from django.shortcuts import render

# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    lista_productos = CatalogoOferta.objects.all()
    return render(request, "catalogoCompras.html", {'productos':lista_productos})

@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        productoId = jsonOferta['productoId']
        print productoId
        producto = CatalogoOferta.objects.get(id=productoId)
        print producto.producto.nombre
        prodAdd = CompraProducto(estado='Activo',
                                 id_catalogoProducto=producto)
        prodAdd.save()
    return JsonResponse({"mensaje": "ok"})