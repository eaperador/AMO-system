# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.http import HttpResponse

from.models import EstadoOferta
from django.shortcuts import render

# Create your views here.


def getStateList(request):
    listaEstados = EstadoOferta.objects.all()
    return HttpResponse(serializers.serialize("json", listaEstados))

def ver_ofertas(request):
	return render(request, "verOfertas.html")