# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import EstadoOferta, Oferta
from django.shortcuts import render

# Create your views here.



@csrf_exempt
def listarEstadosOferta(request):
    listaEstados = EstadoOferta.objects.all()
    return HttpResponse(serializers.serialize("json", listaEstados))
@csrf_exempt
def listarOfertas(request):
    listaOfertas = Oferta.objects.all()
    if (request.method == 'POST'):
        jsonFilter = json.loads(request.body)
        filter = jsonFilter.get('filter')
        if (int(filter) > 0):
            listaOfertas = Oferta.objects.filter(estado=filter)


    page = request.GET.get('page', 1)
    print page
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

##def crearOferta(request, id=None):
##    oferta = Oferta.objects.get(id=id)
##
##    if request.method == 'POST':
##
##    else:
##
##    return render(request, 'CatalogoApp/Comentario.html', contexto)