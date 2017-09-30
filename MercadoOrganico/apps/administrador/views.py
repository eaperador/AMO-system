# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Catalogo, Producto


@csrf_exempt
def index(request):
    return render(request,'Catalogo/index.html')

### Agregar nuevo catalogo ###
@csrf_exempt
def add_catalogo(request):
    if request.method == 'POST':
        print 'Entro'
        jsonData = json.loads(request.body)

        fecha_inicio = jsonData['fecha_inicio']
        fecha_fin = jsonData['fecha_fin']

        catalogo = Catalogo(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        catalogo.save()

        catalogo = {'fecha_inicio': str(catalogo.fecha_inicio), 'fecha_fin': str(catalogo.fecha_fin)}
        convert_catalogo = json.dumps(catalogo)

    return HttpResponse(convert_catalogo)

### Buscar ultimo catalogo y retornar el valor siguiente para el nuevo catalogo ###
@csrf_exempt
def numero_nuevo_catalogo(request):
    if request.method == "GET":
        ultimo_catalogo = Catalogo.objects.all().last()
        data = {'numero': (ultimo_catalogo.id + 1)}
        convert_data = json.dumps(data)

    return HttpResponse(convert_data)

### Seleccionar todos los catalogos ###
@csrf_exempt
def select_catalogos(request):
    if request.method == "GET":
        catalogos = Catalogo.objects.all()
        lista_catalogos = [{'id': catalogo.id, 'fecha_inicio': str(catalogo.fecha_inicio), 'fecha_fin': str(catalogo.fecha_fin)} for catalogo in catalogos]
        data = json.dumps(lista_catalogos)
    return HttpResponse(data)

### Seleccionar todos los productos que estan estado de aprobados ###
@csrf_exempt
def select_productos(request):
    if request.method == "GET":
        productos = Producto.objects.filter(estado=True)
        lista_productos = [{'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'imagen': str(producto.imagen), 'estado': producto.estado} for producto in productos]
    data_convert = json.dumps(lista_productos)
    return HttpResponse(data_convert)

### Seleccionar un producto en especifico ###
@csrf_exempt
def select_producto(request, id):
    print request
    if request.method == "GET":
        producto = Producto.objects.get(pk=id)
        data_producto = {'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'imagen': str(producto.imagen), 'estado': producto.estado}
    data_convert = json.dumps(data_producto)
    return HttpResponse(data_convert)