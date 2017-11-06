# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from ..administrador.models import CatalogoProductos, Producto, ProductoCatalogo
from ..consumidor.models import ItemCompra, Compra, MedioPago
from ..productor.models import Usuario
from ..comun.models import Direccion
from ..distribuidor.models import Entrega
from django.shortcuts import render
# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
    listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=listaCatalogoProductos[0].id)
    return render(request, "catalogoCompras.html", {'productos':listaProductosCatalogo})

@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        productoId = jsonOferta['productoId']
        cantidad = jsonOferta['cantidad']
        producto = ProductoCatalogo.objects.get(id=productoId)

        if int(cantidad) > int(producto.cantidad_disponible):
            cantidad = str(int(producto.cantidad_disponible))

        try:
            itemCompra = ItemCompra.objects.get(id_producto_catalogo=producto)
            itemCompra.cantidad = str(int(itemCompra.cantidad) + int(cantidad))
            itemCompra.save()
        except ItemCompra.DoesNotExist:
            prodAdd = ItemCompra(cantidad=cantidad,
                                 id_producto_catalogo=producto)
            prodAdd.save()

        producto.cantidad_disponible = str(int(producto.cantidad_disponible) - int(cantidad))
        producto.save()

    return JsonResponse({"mensaje": "ok"})

@csrf_exempt
def listar_productos_catalogo_view(request):
    if request.method == 'GET':
        listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
        listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=listaCatalogoProductos[0].id)
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
        productos = Producto.objects.filter(activo=1)
        lista_productos = [{'id': producto.id,
                            'nombre': producto.nombre,
                            'descripcion': producto.descripcion,
                            'imagen': str(producto.foto),
                            'activo': producto.activo} for producto in productos]

        data_convert = json.dumps(lista_productos)
        return HttpResponse(data_convert)

@csrf_exempt
def select_producto(request, id, page):
    if request.method == "GET":
        listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
        if (int(id) > 0):
            producto = Producto.objects.get(pk=id)
            listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=listaCatalogoProductos[0].id).filter(id_producto=producto.id).order_by('id')
        else:
            listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=listaCatalogoProductos[0].id).order_by('id')
        
        #paginacion
        #page = request.GET.get('page', 1)
        paginator = Paginator(listaProductosCatalogo, 4)

        try:
            prodCatalogo = paginator.page(page)
        except PageNotAnInteger:
            prodCatalogo = paginator.page(1)
        except EmptyPage:
            prodCatalogo = paginator.page(paginator.num_pages)

        prevPage = 0
        nextPage = 0
        if (prodCatalogo.has_previous()):
            prevPage = prodCatalogo.previous_page_number()

        if (prodCatalogo.has_next()):
            nextPage = prodCatalogo.next_page_number()

        prodCatalogoPag = {"has_other_pages": prodCatalogo.has_other_pages(),
                      "has_previous": prodCatalogo.has_previous(),
                      "previous_page_number": prevPage,
                      "page_range": prodCatalogo.paginator.num_pages,
                      "has_next": prodCatalogo.has_next(),
                      "next_page_number": nextPage,
                      "current_page": prodCatalogo.number,
                      "first_row": prodCatalogo.start_index()}
        # fin pag
        data_productos_catalogo = [{'id': productoCatalogo.id,
                                    'producto': productoCatalogo.id_producto.nombre,
                                    'foto': str(productoCatalogo.id_producto.foto),
                                    'unidad': productoCatalogo.id_producto.id_tipo_unidad.abreviatura,
                                    'precio': productoCatalogo.precio_definido,
                                    'cantidadDisp': productoCatalogo.cantidad_disponible,
                                    'idProducto': productoCatalogo.id_producto.id}for productoCatalogo in prodCatalogo.object_list]

        #data_convert = json.dumps(data_productos_catalogo, cls=DjangoJSONEncoder)

        json_ = [{"prodCatalogo": data_productos_catalogo,
                  "prodCatalogoPag": prodCatalogoPag
                  }]

    return HttpResponse(json.dumps(json_))

@csrf_exempt
def eliminar_producto(request):
    if request.method == 'PUT':
        jsonOferta = json.loads(request.body)
        productoId = jsonOferta['productoId']
        cantidad = jsonOferta['cantidad']
        producto = ProductoCatalogo.objects.get(id=productoId)
        try:
            itemCompra = ItemCompra.objects.get(id_producto_catalogo=producto)
            if(int(itemCompra.cantidad) != 0 and int(cantidad) <= int(itemCompra.cantidad)):
                itemCompra.cantidad = str(int(itemCompra.cantidad) - int(cantidad))
                itemCompra.save()

                producto.cantidad_disponible = str(int(producto.cantidad_disponible) + int(cantidad))
                producto.save()
            else:
                producto.cantidad_disponible = str(int(producto.cantidad_disponible) + int(itemCompra.cantidad))
                producto.save()

                itemCompra.delete()
        except ItemCompra.DoesNotExist:
           pass
    return JsonResponse({"mensaje": "ok"})

@csrf_exempt
def items_carrito(request):
    sum = 0
    try:
        if request.method == 'GET':
            itemsCompra = ItemCompra.objects.all()
            for item in itemsCompra:
                sum += int(item.cantidad)
    except:
        pass
    return JsonResponse({"sum": str(sum)})

@csrf_exempt
def confirmarCompra(request):
    return render(request, "confirmar_compra.html")

@csrf_exempt
def get_Precios(request):
    if request.method == "GET":
        catalogo_productos = CatalogoProductos.objects.filter(activo=1)
        productosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=catalogo_productos[0].id)
        lista_productos = [{'id': catalogo.id_producto.id,
                            'nombre': catalogo.id_producto.nombre,
                            'precio': catalogo.precio_definido
                            } for catalogo in productosCatalogo]

    data_convert = json.dumps(lista_productos)
    return HttpResponse(data_convert)

@csrf_exempt
def saveCompra(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        cantidad = jsonUser['cantidadItems']
        total = jsonUser['total']
        usuario = Usuario.objects.get(auth_user_id=request.user.id)
        direccion = Direccion.objects.get(id=1)
        medio = MedioPago.objects.get(id=1)
        entrega = Entrega.objects.get(id=1)

        compra = Compra(fecha_compra=datetime.datetime.now(),
                        valor_total= total,
                        cantidad_items= cantidad,
                        fecha_entrega= datetime.datetime.now(),
                        id_usuario_comprador = usuario,
                        id_direccion_compra = direccion,
                        id_entrega = entrega,
                        id_medio_pago=medio);
        compra.save()

    return JsonResponse({"mensaje": "OK"})


