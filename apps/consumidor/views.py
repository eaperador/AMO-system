# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from ..administrador.models import CatalogoProductos, Producto, ProductoCatalogo
from ..consumidor.models import ItemCompra, Compra, MedioPago, ItemCarrito, Carrito
from ..productor.models import Usuario
from ..comun.models import Direccion
from ..distribuidor.models import Entrega
from django.shortcuts import render
# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
    if request.method == 'GET':
        try:
            carrito_id = request.GET.get('carrito')
            itemsList = [{'id': item.id,
                          'cantidad': item.cantidad,
                          'producto': item.id_producto_catalogo.id}
                         for item in ItemCarrito.objects.filter(id_carrito=carrito_id)]
        except ItemCarrito.DoesNotExist:
            itemsList = []
        istemsJson = json.dumps(itemsList)
    return render(request, "catalogoCompras.html", {'catalogo':listaCatalogoProductos[0],
                                                    'items': istemsJson})

@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        jsonOferta = json.loads(request.body)
        producto_cat_id = jsonOferta['productoId']
        cantidad = jsonOferta['cantidad']
        catalogo_id = jsonOferta['catalogo']
        carrito_id = jsonOferta['carrito']
        producto = ProductoCatalogo.objects.filter(id=producto_cat_id).filter(id_catalogo=catalogo_id).first()
        if (carrito_id is not None):
            carrito = Carrito.objects.get(id = carrito_id)
            itemCompras = ItemCarrito.objects.filter(id_producto_catalogo=producto).filter(id_carrito=carrito_id)
            if (len(itemCompras) > 0):
                itemCompra = itemCompras.first()
                itemCompra.cantidad = itemCompra.cantidad + int(cantidad)
            else:
                itemCompra = ItemCarrito(cantidad=cantidad,
                                         id_producto_catalogo=producto,
                                         id_carrito = Carrito.objects.get(id = carrito_id))
        else:
            carrito = Carrito(cantidad_items = int(cantidad),
                              valor_total = producto.precio_definido * int(cantidad))
            carrito.save()
            itemCompra = ItemCarrito(cantidad=int(cantidad),
                                     id_producto_catalogo=producto,
                                     id_carrito = carrito)
        carrito.save();
        itemCompra.save()
        itemsList = [{'id': item.id,
                      'cantidad': item.cantidad,
                      'producto': item.id_producto_catalogo.id}
                     for item in ItemCarrito.objects.filter(id_carrito=carrito.id)]

        istemsJson = json.dumps(itemsList)
    return JsonResponse({"mensaje": "ok",
                         "carrito_id": carrito.id,
                         "items": itemsList})
@csrf_exempt
def eliminar_producto(request):
    if request.method == 'PUT':
        jsonOferta = json.loads(request.body)
        producto_id = jsonOferta['productoId']
        cantidad = jsonOferta['cantidad']
        catalogo_id = jsonOferta['catalogo']
        carrito_id = jsonOferta['carrito']
        producto = ProductoCatalogo.objects.filter(id_producto_id=producto_id).filter(id_catalogo=catalogo_id).first()
        itemsList = []
        if (carrito_id is not None):
            carrito = Carrito.objects.get(id=carrito_id)
            itemCompras = ItemCarrito.objects.filter(id_producto_catalogo=producto).filter(id_carrito=carrito_id)
            if (len(itemCompras) > 0):
                itemCompra = itemCompras.first()
                itemCompra.cantidad = itemCompra.cantidad - int(cantidad)
            carrito.save();
            if (itemCompra.cantidad > 0):
                itemCompra.save()
            else:
                itemCompra.delete()
            itemsList = [{'id': item.id,
                          'cantidad': item.cantidad,
                          'producto': item.id_producto_catalogo.id}
                         for item in ItemCarrito.objects.filter(id_carrito=carrito.id)]

    return JsonResponse({"mensaje": "ok",
                         "carrito_id": carrito.id,
                         "items": itemsList})

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
    # Filtrar por los productos que existen dentro del catálogo
    if request.method == "GET":
        catalogo = CatalogoProductos.objects.filter(activo = True)
        productos = ProductoCatalogo.objects.filter(id_catalogo_id = catalogo[0].id)
        lista_productos = [{'id': productoCat.id_producto.id,
                            'nombre': productoCat.id_producto.nombre,
                            'descripcion': productoCat.id_producto.descripcion,
                            'imagen': str(productoCat.id_producto.foto),
                            'activo': productoCat.id_producto.activo} for productoCat in productos]
        data_convert = json.dumps(lista_productos)
        return HttpResponse(data_convert)

@csrf_exempt
def select_producto(request, id, page):
    if request.method == "GET":
        listaCatalogoProductos = CatalogoProductos.objects.filter(activo=1)
        catalogo = listaCatalogoProductos.first()
        if (int(id) > 0):
            producto = Producto.objects.get(pk=id)
            listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=catalogo.id).filter(id_producto=producto.id).order_by('id')
        else:
            listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=catalogo.id).order_by('id')

        limit_date = datetime.datetime.now() - datetime.timedelta(minutes=5) + datetime.timedelta(hours=5)
        for prod in listaProductosCatalogo:
            itemsReserva = ItemCarrito.objects.filter(id_producto_catalogo=prod.id).filter(id_carrito__fecha_hora__gte=limit_date)
            reserved = 0
            for item in itemsReserva:
                reserved += item.cantidad
            prod.cantidad_disponible -= reserved
            # TODO revisar esto respecto a la compra
            itemsCompra = ItemCompra.objects.filter(id_producto_catalogo=prod.id).filter(id_producto_catalogo__id_catalogo=catalogo.id)
            compra = 0
            for item in itemsCompra:
                compra += item.cantidad
            prod.cantidad_disponible -= compra

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
def items_carrito(request):
    sum = 0
    try:
        if request.method == 'GET':
            carrito_id = request.GET.get('carrito')
            itemsCarrito = ItemCarrito.objects.filter(id_carrito=carrito_id)
            for item in itemsCarrito:
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


