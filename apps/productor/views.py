# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


from .models import EstadoOferta, Oferta, CatalogoOfertas
from ..comun.models import Usuario
from ..administrador.models import Producto
from django.shortcuts import render, redirect


# Create your views here.



@csrf_exempt
def listarEstadosOferta(request):
    listaEstados = EstadoOferta.objects.all()
    return HttpResponse(serializers.serialize("json", listaEstados))


@csrf_exempt
def listarOfertas(request):
    # listaOfertas = Oferta.objects.all()
    print(request.user.id)
    usuario = Usuario.objects.get(auth_user_id=request.user)
    listaOfertas = Oferta.objects.filter(productor=usuario.id)
    if (request.method == 'POST'):
        jsonFilter = json.loads(request.body)
        filter = jsonFilter.get('filter')
        user = request.user
        if (int(filter) > 0):
            # listaOfertas = Oferta.objects.filter(estado=filter)
            listaOfertas = Oferta.objects.filter(estado=filter).filter(productor=usuario.id)

    page = request.GET.get('page', 1)
    paginator = Paginator(listaOfertas, 3)

    try:
        ofertas = paginator.page(page)
    except PageNotAnInteger:
        ofertas = paginator.page(1)
    except EmptyPage:
        ofertas = paginator.page(paginator.num_pages)

    prevPage = 0
    nextPage = 0
    if (ofertas.has_previous()):
        prevPage = ofertas.previous_page_number()

    if (ofertas.has_next()):
        nextPage = ofertas.next_page_number()

    ofertasPag = {"has_other_pages": ofertas.has_other_pages(),
                  "has_previous": ofertas.has_previous(),
                  "previous_page_number": prevPage,
                  "page_range": ofertas.paginator.num_pages,
                  "has_next": ofertas.has_next(),
                  "next_page_number": nextPage,
                  "current_page": ofertas.number,
                  "first_row": ofertas.start_index()}

    listaOfertasJson = [{
        "pk": oferta.id,
        "fecha": oferta.fecha.strftime('%Y-%m-%d %H:%M'),
        "precio": oferta.precio,
        "cantidad": oferta.cantidad,
        "estado": oferta.estado.nombre,
        "producto": oferta.producto.nombre,
        "unidad": oferta.producto.tipoUnidad.abreviatura,
    } for oferta in ofertas.object_list]
    json_ = [{"ofertas": listaOfertasJson,
              "ofertasPag": ofertasPag
              }]

    return HttpResponse(json.dumps(json_))


@csrf_exempt
def ver_ofertas(request):
    return render(request, "verOfertas.html")


@csrf_exempt
def crearOferta(request):
    estadoOferta = EstadoOferta.objects.get(id=1) #Ofertas activas

    if request.method == 'POST':
        dias = CalculoDiasCatalogoOfertas()
        # hoy = hoy - timedelta(4) ##Para lanzar ejemplo con cualquier dia
        hoy = dias[0]
        print "hoy: ", hoy
        intdia = hoy.strftime("%w")
        dia = diaSemana(intdia)
        print "Dia de la semana: ", dia

        if (dia == 'Domingo'):
            print 'Las ofertas solo pueden realizarse de Lunes a viernes'
            # return mensaje
        elif (dia == 'Sabado'):
             print 'Las ofertas solo pueden realizarse de Lunes a sábado'
            # return mensaje
        else:
            print 'Dia disponible para realizar ofertas'
            # Fecha inicio Oferta
            _diaInicioOferta = dias[1]
            _diaFinOferta = dias[2]
            # Consulta catalogo de ofertas para la semana
            _catalogoOferta = CatalogoOfertas.objects.filter(fecha_inicio__gte=hoy, fecha_fin__lte=hoy)
            if _catalogoOferta.count() > 0:
                print 'Existe catálogo oferta para esta semana, se adicionará la oferta a ese catálogo'
                id_catalogo_oferta = _catalogoOferta
            else:
                print 'No existe catálogo para la semana, se creará uno'
                id_catalogo_oferta = CatalogoOfertas(fecha_inicio = _diaInicioOferta,
                                                     fecha_fin=_diaFinOferta,
                                                     activo=True)
                id_catalogo_oferta.save()
                print 'Creacion correcta del catálogo'

        #Se crea el objeto oferta a guardar
        jsonObj = json.loads(request.body)
        precio = jsonObj['precio']
        cantidad = jsonObj['cantidad']
        idproducto = jsonObj['producto']
        producto = Producto.objects.get(id=idproducto)
        idproductor = jsonObj['user']
        productor = Usuario.objects.get(pk=idproductor)

        #cantidad_disponible***
        oferta_model = Oferta(precio=precio, cantidad=cantidad, cantidad_disponible=10, id_estado_oferta=estadoOferta,
                              id_producto=producto, id_productor=productor, id_catalogo_oferta=id_catalogo_oferta)
        oferta_model.save()

        json_response = [{'mensaje': "OK"}]
        data_convert = json.dumps(json_response)
        return HttpResponse(data_convert, content_type='application/json')

def CalculoDiasCatalogoOfertas():
    # Hoy
    hoy = datetime.now()
    # hoy = hoy - timedelta(4) ##Para lanzar ejemplo con cualquier dia
    print "hoy: ", hoy
    intdia = hoy.strftime("%w")
    dia = diaSemana(intdia)
    print "Dia de la semana: ", dia
    _numeroDiasOferta = 4

    if (dia == 'Domingo'):
        #print 'Las ofertas solo pueden realizarse de Lunes a sábado'
        #print 'Inicio de Oferta: ', hoy + timedelta(days=1)
        #Fecha inicio Oferta
        _diaInicioOferta = hoy + timedelta(days=1)
    elif (dia == 'Sabado'):
        #print 'Las ofertas solo pueden realizarse de Lunes a sábado'
        #print 'Inicio de Oferta: ', hoy + timedelta(days=2)
        # Fecha inicio Oferta
        _diaInicioOferta = hoy + timedelta(days=2)
    else:
        #print 'Dia disponible para realizar ofertas'
        # Fecha inicio Oferta
        _intDiaInicioOferta = intdia - (intdia - 1)
        _diaInicioOferta = hoy - timedelta(days=_intDiaInicioOferta)
        #print 'Inicio de Oferta: ', _diaInicioOferta
        #print 'Fin de la oferta: ', _diaFinOferta

    _diaFinOferta = _diaInicioOferta + timedelta(days=_numeroDiasOferta)
    return (hoy, _diaInicioOferta, _diaFinOferta)

def diaSemana(day):
        return {
            '0': 'Domingo',
            '1': 'Lunes',
            '2': 'Martes',
            '3': 'Miercoles',
            '4': 'Jueves',
            '5': 'Viernes',
            '6': 'Sabado'
        }.get(day, 'No es un dia de la semana')


@csrf_exempt
def ConsultarProductosaOfertar(request):
    # filtrar para obtener productos que NO estén en las ofertas hechas
    #for pet in pets:
    #    print(pet)

    listaProductos = Producto.objects.filter(activo=True)
    if (listaProductos.count() > 0):
        page = request.GET.get('page', 1)
        paginator = Paginator(listaProductos, 3)

        try:
            productos = paginator.page(page)
        except PageNotAnInteger:
            productos = paginator.page(1)
        except EmptyPage:
            productos = paginator.page(paginator.num_pages)

        prevPage = 0
        nextPage = 0
        if (productos.has_previous()):
            prevPage = productos.previous_page_number()

        if (productos.has_next()):
            nextPage = productos.next_page_number()

        productosPag = {"has_other_pages": productos.has_other_pages(),
                        "has_previous": productos.has_previous(),
                        "previous_page_number": prevPage,
                        "page_range": productos.paginator.num_pages,
                        "has_next": productos.has_next(),
                        "next_page_number": nextPage,
                        "current_page": productos.number,
                        "first_row": productos.start_index()}

        listaProductos = [{
            "pk": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            #"tipoUnidad": producto.tipoUnidad.abreviatura,
            "tipoUnidad": producto.id_tipo_unidad.abreviatura,
            "categoria": producto.id_categoria.nombre,
        } for producto in productos.object_list]

        jsonReturn = [{"productos": listaProductos,
                       "productosPag": productosPag
                       }]

        return HttpResponse(json.dumps(jsonReturn), content_type='application/json')
    else:
        return JsonResponse({'mensaje': 'No hay productos para ofertar'})


@csrf_exempt
def ver_productos(request):
    #user = request.user
    #print user.id
    return render(request, "productosaOfertar.html")


def editarOferta(request):
    return render(request, "editarOferta.html")

@csrf_exempt
def verOfertasVendidas(request):
    return render(request, "consultarOfertasVendidas.html")