# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from ..administrador.models import Catalogo, CatalogoOferta
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    lista_productos = CatalogoOferta.objects.all()
    return render(request, "catalogoCompras.html",{'productos':lista_productos})

def agregar_producto(request):
    print "P1"
    return render(request, "agregarProducto.html")

def agregar_producto_carrito(request,id=None):
    print "P2"
    lista_productos = CatalogoOferta.objects.all()
    producto = CatalogoOferta.objects.get(id=id)
    cantidad=0

    context = {'productos': lista_productos,
               'cantidad':cantidad}
    return render(request, "catalogoCompras.html", context)