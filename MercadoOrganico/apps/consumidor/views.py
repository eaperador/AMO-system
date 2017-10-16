# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt
from ..administrador.models import CatalogoOferta
from django.http import HttpResponseRedirect
from models import CompraProducto
from django.shortcuts import render

# Create your views here.

@csrf_exempt
def catalogo_compras(request):
    lista_productos = CatalogoOferta.objects.all()
    return render(request, "catalogoCompras.html", {'productos':lista_productos})

def agregar_producto(request,id):
    producto = CatalogoOferta.objects.get(id=id)

    print request.method
    if request.method == "POST":
        prodAdd = CompraProducto(estado='Activo',
                                 id_catalogoProducto=producto.id)
        prodAdd.save()
        return HttpResponseRedirect('/')

    context = {'producto': producto}
    print producto.producto.nombre
    return render(request, 'agregarProducto.html', context)
