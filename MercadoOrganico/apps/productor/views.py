# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
import json
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
    return HttpResponse(serializers.serialize("json", listaOfertas,use_natural_foreign_keys=True))
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