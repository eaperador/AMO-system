# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime

import os
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from ..administrador.models import CatalogoProductos, Producto, ProductoCatalogo
from ..consumidor.models import ItemCompra, Compra, MedioPago, ItemCarrito, Carrito, FormConsumidor
from ..productor.models import Usuario, Oferta, CatalogoOfertas, CompraOfertado
from ..comun.models import Direccion, Rol
from ..distribuidor.models import Entrega, Ruta
from django.shortcuts import render
from django.contrib.auth.models import User
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
    return render(request, "catalogoCompras.html", {'catalogo':listaCatalogoProductos.first(),
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
        productos = ProductoCatalogo.objects.filter(id_catalogo_id = catalogo[0].id).filter(cantidad_disponible__gt=0).order_by('id_producto__nombre')
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
            listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=catalogo.id).filter(id_producto=producto.id).\
                filter(cantidad_disponible__gt=0).order_by('id')
        else:
            listaProductosCatalogo = ProductoCatalogo.objects.filter(id_catalogo=catalogo.id).filter(cantidad_disponible__gt=0).order_by('id')
        ON_CODESHIP = os.getenv('ON_CODESHIP', False)
        ON_HEROKU_BUG = os.getenv('ON_HEROKU_BUG', False)
        ON_HEROKU_TEST = os.getenv('ON_HEROKU_TEST', False)
        ON_HEROKU_PROD = os.getenv('ON_HEROKU_PROD', False)
        if (ON_CODESHIP or  ON_HEROKU_BUG or ON_HEROKU_TEST or ON_HEROKU_PROD):
            hoursDelta = 0
        else:
            hoursDelta = 5
        limit_date = datetime.datetime.now() - datetime.timedelta(minutes=5) + datetime.timedelta(hours=hoursDelta)

        for prod in listaProductosCatalogo:
            itemsReserva = ItemCarrito.objects.filter(id_producto_catalogo=prod.id).filter(id_carrito__fecha_hora__gte=limit_date)
            reserved = 0
            for item in itemsReserva:
                reserved += item.cantidad
            prod.cantidad_disponible -= reserved

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
        carrito_id = request.GET.get('carrito')
        itemsCarrito = ItemCarrito.objects.filter(id_carrito=carrito_id)
        lista_productos = [{'id': item.id,
                            'nombre': item.id_producto_catalogo.id_producto.nombre,
                            'precio': item.id_producto_catalogo.precio_definido,
                            'cantidad': item.cantidad,
                            'unidad': item.id_producto_catalogo.id_producto.id_tipo_unidad.abreviatura
                            } for item in itemsCarrito]

    data_convert = json.dumps(lista_productos)
    return HttpResponse(data_convert)

@csrf_exempt
def saveCompra(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        usuario = Usuario.objects.get(auth_user_id=request.user)
        carrito_id = jsonData['carrito']
        dir = jsonData['direccion']
        carroCompra = Carrito.objects.get(id=carrito_id)
        itemsCarrito = ItemCarrito.objects.filter(id_carrito=carrito_id)
        dirUsuario = Direccion.objects.get(id_usuario_comprador=usuario.id)
        if not Direccion.objects.filter(id_usuario_comprador=usuario.id).exists():
            dirUsuario = Direccion(direccion=dir,
                                   id_usuario_comprador=usuario)
            dirUsuario.save()
        medioPago = MedioPago.objects.get(id_usuario_comprador=usuario.id)
        if not MedioPago.objects.filter(id_usuario_comprador=usuario.id).exists():
            medioPago = MedioPago(nombre='Efectivo',
                                  id_usuario_comprador=usuario)
            medioPago.save()
        ruta = Ruta(descripcion='Ruta',
                    id_usuario_distribuidor=usuario)
        ruta.save()
        entrega = Entrega(estado='Pendiente',
                          id_ruta=ruta)
        entrega.save()

        compra = Compra(fecha_compra=datetime.datetime.now(),
                        valor_total=0,
                        cantidad_items=0,
                        fecha_entrega=datetime.datetime.now(),
                        id_usuario_comprador=usuario,
                        id_direccion_compra=dirUsuario,
                        id_entrega=entrega,
                        id_medio_pago=medioPago);
        compra.save()

        vTotal = 0.0;
        canIt = 0;
        for item in itemsCarrito:
            vTotal += float(item.id_producto_catalogo.precio_definido) * int(item.cantidad)
            canIt += int(item.cantidad)
            itemCompra = ItemCompra(cantidad=item.cantidad,
                                    id_producto_catalogo=item.id_producto_catalogo,
                                    id_compra=compra)
            pCatalog = ProductoCatalogo.objects.get(id=item.id_producto_catalogo_id)
            pCatalog.cantidad_disponible -= int(item.cantidad)
            pCatalog.save()
            itemCompra.save()

            catalogoOf = CatalogoOfertas.objects.filter(activo=True).order_by('fecha_inicio')
            ofertas = Oferta.objects.filter(id_catalogo_oferta=catalogoOf[catalogoOf.count()-1].id, id_producto=item.id_producto_catalogo.id_producto.id).order_by('precio')
            print (catalogoOf[catalogoOf.count()-1].id)

            cantOfr = int(item.cantidad)
            for oferta in ofertas:
                if oferta.id_producto.id == item.id_producto_catalogo.id_producto.id and cantOfr > 0:
                    if int(cantOfr) >= int(oferta.cantidad_disponible):
                        cantOfr -= int(oferta.cantidad_disponible)
                        oferta.cantidad_disponible = 0
                    else:
                        oferta.cantidad_disponible -= int(cantOfr)
                        cantOfr = 0
                    cOfertado = CompraOfertado(cantidad=item.cantidad,
                                               id_item_compra=itemCompra,
                                               id_oferta=oferta)
                    cOfertado.save()
                    oferta.save()
            item.delete()

        compra.valor_total=vTotal
        compra.cantidad_items=canIt
        compra.save()
        carroCompra.delete()

    return JsonResponse({"mensaje": "OK"})

@csrf_exempt
def registrarse(request):
    form = FormConsumidor()
    context = {'form': form}
    return render(request, "registroComprador.html", context)

@csrf_exempt
def registrarComprador(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        foto = jsonData['foto']
        m_pago = jsonData['medio_pago']
        direcciones = jsonData['direcciones']
        usuario = jsonData['username']
        clave = jsonData['password']
        nombres = jsonData['first_name']
        apellidos = jsonData['last_name']
        correo = jsonData['email']
        telefono = jsonData['telefono']

        antUser = User.objects.filter(username=usuario)
        if antUser.count() == 0:
            user_data = User.objects.create_user(username=usuario, password=clave)
            user_data.first_name = nombres
            user_data.last_name = apellidos
            user_data.email = correo
            user_data.save()

            rol = Rol.objects.get(nombre="Consumidor")
            usuario_data = Usuario.objects.create(foto=foto,
                                                 telefono=telefono,
                                                 id_rol=rol,
                                                 auth_user_id=user_data)
            usuario_data.save()

            medio_pago = MedioPago.objects.create(nombre=m_pago,
                                                 id_usuario_comprador=usuario_data)
            medio_pago.save()

            for dir_item in direcciones.split(","):
                if dir_item != "":
                    dir_usu = Direccion.objects.create(direccion=dir_item,
                                                       id_usuario_comprador=usuario_data)
                    dir_usu.save()
        else:
            return JsonResponse({"mensaje": "El usuario ya existe."})
        
    return JsonResponse({"mensaje": "OK"})
