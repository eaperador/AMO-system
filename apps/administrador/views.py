# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta, datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import time
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from ..comun.views import sendMailNotification
from .models import CatalogoProductos, Producto
from ..productor.models import EstadoOferta, Oferta, CatalogoOfertas
from ..administrador.models import ProductoCatalogo

@csrf_exempt
def index(request):
    return render(request,'Catalogo/add_catalogo.html')

### Agregar nuevo catalogo ###
@csrf_exempt
def add_catalogo(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body)

        fecha_inicio = jsonData['fecha_inicio']
        fecha_fin = jsonData['fecha_fin']

        catalogo = CatalogoProductos(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, activo=True)
        catalogo.save()

        catalogo = {'fecha_inicio': str(catalogo.fecha_inicio), 'fecha_fin': str(catalogo.fecha_fin), 'activo': str(catalogo.activo)}
        convert_catalogo = json.dumps(catalogo)

    return HttpResponse(convert_catalogo)

### Buscar ultimo catalogo y retornar el valor siguiente para el nuevo catalogo ###
@csrf_exempt
def numero_nuevo_catalogo(request):
    if request.method == "GET":
        ultimo_catalogo = CatalogoProductos.objects.all().last()
        if ultimo_catalogo:
            data = {'numero': (ultimo_catalogo.id + 1)}
        else:
            data = {'numero': 1}

        convert_data = json.dumps(data)

    return HttpResponse(convert_data)

### Seleccionar todos los catalogos ###
@csrf_exempt
def select_catalogos(request):
    if request.method == "GET":
        catalogos = CatalogoProductos.objects.all()
        lista_catalogos = [{'id': catalogo.id, 'fecha_inicio': str(catalogo.fecha_inicio), 'fecha_fin': str(catalogo.fecha_fin)} for catalogo in catalogos]
        data = json.dumps(lista_catalogos)
    return HttpResponse(data)

### Seleccionar todos los productos que estan estado de aprobados ###
@csrf_exempt
def select_productos(request):
    if request.method == "GET":
        catalogo = CatalogoOfertas.objects.filter(activo=True)
        listaOfertas = Oferta.objects.filter(id_catalogo_oferta=catalogo.first().id)\
                                     .distinct('id_producto__nombre')\
                                     .order_by('id_producto__nombre')
        if request.method == "GET":
            lista_productos = [{'id': oferta.id_producto.id,
                                'nombre': oferta.id_producto.nombre,
                                'descripcion': oferta.id_producto.descripcion,
                                'activo': oferta.id_producto.activo} for oferta in listaOfertas]
    data_convert = json.dumps(lista_productos)

    return HttpResponse(data_convert)

### Seleccionar un producto en especifico ###
@csrf_exempt
def select_producto(request, id):
    if request.method == "GET":
        producto = Producto.objects.get(pk=id)
        data_producto = {'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'imagen': str(producto.foto), 'activo': producto.activo}
    data_convert = json.dumps(data_producto)
    return HttpResponse(data_convert)

### Listar ofertas de los productores ###
@csrf_exempt
def listarOfertas(request, productoId, filtro):
    if request.method == 'GET':
        listaCatalogoOfertas = CatalogoOfertas.objects.filter(activo=1)
        if productoId == '0':
            listaOfertas = Oferta.objects.filter(id_catalogo_oferta=listaCatalogoOfertas[0].id)
        else:
            estado_oferta = EstadoOferta.objects.filter(pk=2)# estado 2 es activa
            if filtro == '1':
                listaOfertas = Oferta.objects.filter(id_producto=productoId).filter(id_catalogo_oferta=listaCatalogoOfertas[0].id)
            elif filtro == '2':
                listaOfertas = Oferta.objects.filter(id_producto=productoId).filter(id_catalogo_oferta=listaCatalogoOfertas[0].id).filter(id_estado_oferta=estado_oferta)

        data_oferta = [{'id': oferta.id,
                        'producto': oferta.id_producto.nombre,
                        'fecha': oferta.fecha.strftime('%Y-%m-%d %H:%M'),
                        'productor': oferta.id_productor.auth_user_id.first_name + " " + oferta.id_productor.auth_user_id.last_name,
                        'cantidad': oferta.cantidad,
                        'precio': oferta.precio,
                        'estadoId': oferta.id_estado_oferta.id,
                        'estadoNombre': oferta.id_estado_oferta.nombre,
                        'unidad': oferta.id_producto.id_tipo_unidad.abreviatura} for oferta in listaOfertas.order_by('id_producto__nombre', 'precio')]
        data_convert = json.dumps(data_oferta, cls=DjangoJSONEncoder)
    return HttpResponse(data_convert)

def enviarNotificacion(oferta):
    prod = oferta.id_productor
    email = prod.auth_user_id.email
    asunto = "Han respondido una oferta"
    mensaje = "Señor(a) "+prod.auth_user_id.first_name+" "+prod.auth_user_id.last_name+": \n\n"
    mensaje = mensaje + "De la forma más atenta queremos informale que la oferta que realizó en la fecha "+oferta.fecha.strftime('%Y-%m-%d %H:%M')+" \n"
    mensaje = mensaje + "sobre el producto "+oferta.id_producto.nombre+" por un valor de $"+str(oferta.precio)+" se encuentra en estado:\n"
    mensaje = mensaje + oferta.id_estado_oferta.nombre.upper()+"\n\n"
    mensaje = mensaje + "Puede consultar el estado de la oferta en su perfil y recuerde estar atento a futuras notificaciones\n\n"
    mensaje = mensaje + "Saludos."
    sendMailNotification(email, asunto, mensaje)

@csrf_exempt
def guardarOferta(request):
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        ofertaId = jsonOferta['ofertaId']
        estadoId = jsonOferta['estadoId']
        Oferta.objects.filter(pk=ofertaId).update(id_estado_oferta = estadoId)
        enviarNotificacion(Oferta.objects.get(id=ofertaId))
    return JsonResponse({"mensaje": "ok"})

@csrf_exempt
def evaluarOfertas(request):
    return render(request, "Ofertas/evaluar_ofertas.html")

@csrf_exempt
def catalogoProductos(request):
    return render(request, "Ofertas/catalogoProductos.html")

@csrf_exempt
def ingresarCatalogoOferta(request):
    if request.method == "POST":
        jsonData = json.loads(request.body)
        precio_definido = jsonData['precio_definido']
        cantidad_definida = jsonData['cantidad_definida']
        idcatalogo = jsonData['catalogo']
        catalogo = CatalogoProductos.objects.get(pk=idcatalogo)
        idproducto = jsonData['producto']
        producto = Producto.objects.get(pk=idproducto)
        catalgo_oferta = ProductoCatalogo(precio_definido=precio_definido, cantidad_definida=cantidad_definida, cantidad_disponible=cantidad_definida,  id_catalogo=catalogo, id_producto=producto)
        catalgo_oferta.save()
    return JsonResponse({"mensaje": "ok"})


@csrf_exempt
def get_CatalogoOfertaActivo(request):
    if request.method == 'GET':
        catalogoOferta = CatalogoOfertas.objects.get(activo=1)
        data_catalogoOferta = {'fecha_inicio': catalogoOferta.fecha_inicio.strftime('%Y-%m-%d'), 'fecha_fin': catalogoOferta.fecha_fin.strftime('%Y-%m-%d')}
        data_convert = json.dumps(data_catalogoOferta)
    return HttpResponse(data_convert)

@csrf_exempt
def getCatalogoProducto(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        id_catalogo = jsonData['catalogo']
        catalogo = CatalogoProductos.objects.get(pk=id_catalogo)
        id_producto = jsonData['producto']
        producto = Producto.objects.get(pk=id_producto)

        producto_catalogo = ProductoCatalogo.objects.filter(id_producto=producto,id_catalogo=catalogo)

        if producto_catalogo:
            message = "Si"
        else:
            message = "No"

    return JsonResponse({"mensaje": message})

@csrf_exempt
def listar_productos(request):
    if request.method == "GET":
        listado_productos = Producto.objects.all()
        data_producto = [{'id': producto.id,
                         'nombre': producto.nombre,
                         'descripcion': producto.descripcion,
                         'imagen': str(producto.foto),
                         'activo': producto.activo} for producto in listado_productos]
    data_convert = json.dumps(data_producto)
    return HttpResponse(data_convert)

@csrf_exempt
def guardarEstadoProducto(request):
    if request.method == 'POST':
        jsonProducto = json.loads(request.body)
        productoId = jsonProducto['productoId']
        estado = jsonProducto['estado']
        catalogo_oferta = CatalogoOfertas.objects.get(activo=1)

        if estado == 1:
            Producto.objects.filter(pk=productoId).update(activo=estado)
            mensaje = "ok"
        else:
            if catalogo_oferta.fecha_fin >= datetime.now().date():
                ofertas = Oferta.objects.filter(id_catalogo_oferta = catalogo_oferta).filter(id_producto = productoId)
                if ofertas.count() == 0 :
                    Producto.objects.filter(pk=productoId).update(activo = estado)
                    mensaje = "ok"
                else:
                    mensaje = "no"
            else:
                print("lo cambia de estado adesactivado");
                Producto.objects.filter(pk=productoId).update(activo=estado)
                mensaje="ok"

    return JsonResponse({"mensaje": mensaje})

