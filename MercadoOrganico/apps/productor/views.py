# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..administrador.views import enviarNotificacion
from .models import EstadoOferta, Oferta
from ..administrador.models import Producto
from django.shortcuts import render

# Create your views here.



@csrf_exempt
def listarEstadosOferta(request):
    listaEstados = EstadoOferta.objects.all()
    return HttpResponse(serializers.serialize("json", listaEstados))

@csrf_exempt
def listarOfertas(request):
    listaOfertas = Oferta.objects.all()
    #listaOfertas = Oferta.objects.filter(productor = 1) //Filtro con el login
    if (request.method == 'POST'):
        jsonFilter = json.loads(request.body)
        filter = jsonFilter.get('filter')
        user = request.user
        print user
        if (int(filter) > 0):
            listaOfertas = Oferta.objects.filter(estado=filter)
            #listaOfertas = Oferta.objects.filter(estado=filter).filter(productor = 1)  //Filtro con el login



    page = request.GET.get('page', 1)
    paginator = Paginator(listaOfertas,3)

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
    
    ofertasPag = {"has_other_pages" : ofertas.has_other_pages(),
                   "has_previous" : ofertas.has_previous(),
                   "previous_page_number" : prevPage,
                   "page_range" : ofertas.paginator.num_pages,
                   "has_next" : ofertas.has_next(),
                   "next_page_number" : nextPage,
                   "current_page" : ofertas.number,
                   "first_row" : ofertas.start_index()}

    listaOfertasJson = [{
        "pk": oferta.id,
        "fecha": oferta.fecha.strftime('%Y-%m-%d %H:%M'),
        "precio": oferta.precio,
        "cantidad": oferta.cantidad,
        "estado": oferta.estado.nombre,
        "producto": oferta.producto.nombre,
        "unidad": oferta.producto.tipoUnidad.abreviatura,
        } for oferta in ofertas.object_list]
    json_ = [{"ofertas" : listaOfertasJson,
              "ofertasPag" : ofertasPag
              }]

    return HttpResponse(json.dumps(json_))
@csrf_exempt
def ver_ofertas(request):
	return render(request, "verOfertas.html")


@csrf_exempt
def crearOferta(request):
	return render(request, "crearOferta.html")


@csrf_exempt
def ConsultarProductosaOfertar(request):
    listaProductos = Producto.objects.filter(activo= True)
    if (listaProductos.count() > 0):
        page = request.GET.get('page', 1)
        print page
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
            "tipoUnidad": producto.tipoUnidad.abreviatura,
            "categoria": producto.categoria.nombre,
        } for producto in productos.object_list]

        jsonReturn = [{"productos": listaProductos,
                  "productosPag": productosPag
                  }]

        return HttpResponse(json.dumps(jsonReturn), content_type='application/json')
    else:
        return JsonResponse({'mensaje': 'No hay productos para ofertar'})


@csrf_exempt
def ver_productos(request):
	return render(request, "productosaOfertar.html")