# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.core.serializers.json import DjangoJSONEncoder
import time
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Catalogo, Producto
from ..productor.models import EstadoOferta, Oferta

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
        productos = Producto.objects.filter(activo=True)
        lista_productos = [{'id': producto.id,
                            'nombre': producto.nombre,
                            'descripcion': producto.descripcion,
                            'imagen': str(producto.imagen),
                            'activo': producto.activo} for producto in productos]
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

### Listar ofertas de los productores ###
@csrf_exempt
def listarOfertas(request, productoId):
    if request.method == 'GET':
        if productoId == '0':
            data_oferta = []
        else:
            listaOfertas = Oferta.objects.filter(producto=productoId)
            data_oferta = [{'id': oferta.id,
                            'producto': oferta.producto.nombre,
                            'fecha': oferta.fecha,
                            'productor':oferta.productor.auth_user_id.first_name + " " + oferta.productor.auth_user_id.last_name,
                            'cantidad':oferta.cantidad,
                            'precio':oferta.precio,
                            'estadoId':oferta.estado.id,
                            'estadoNombre':oferta.estado.nombre,
                            'unidad': oferta.producto.tipoUnidad.abreviatura}for oferta in listaOfertas]
    data_convert = json.dumps(data_oferta,cls=DjangoJSONEncoder)
    return HttpResponse(data_convert)

@csrf_exempt
def guardarOferta(request):
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        ofertaId = jsonOferta['ofertaId']
        estadoId = jsonOferta['estadoId']
        Oferta.objects.filter(pk=ofertaId).update(estado = estadoId)

    return JsonResponse({"mensaje": "ok"})

@csrf_exempt
def evaluarOfertas(request):
    return render(request, "Ofertas/evaluar_ofertas.html")



