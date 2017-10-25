# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt

from ..consumidor.models import ProductoCatalogo
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    lista_productos = ProductoCatalogo.objects.all()
    return render(request, "catalogoCompras.html", {'productos':lista_productos})

@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        productoId = jsonOferta['productoId']
        producto = ProductoCatalogo.objects.get(id=productoId)
        prodAdd = ProductoCatalogo(cantidad='1',
                                 id_producto_catalogo=producto)
        prodAdd.save()
    return JsonResponse({"mensaje": "ok"})