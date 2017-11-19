# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


from .models import EstadoOferta, Oferta, CatalogoOfertas, CompraOfertado
from ..comun.models import Usuario
from ..administrador.models import Producto
from django.shortcuts import render, redirect


# Create your views here.

### Variable para obtener el estado de oferta activo ###
estado_oferta = EstadoOferta.objects.filter(pk=1)

@csrf_exempt
def listarEstadosOferta(request):
    listaEstados = EstadoOferta.objects.all()
    return HttpResponse(serializers.serialize("json", listaEstados))


@csrf_exempt
def listarOfertas(request):
    # listaOfertas = Oferta.objects.all()
    usuario = Usuario.objects.get(auth_user_id=request.user.id)
    catalogo_list = CatalogoOfertas.objects.all().order_by('-id')
    listaOfertas = Oferta.objects.filter(id_productor=usuario.id)
    ofertas_catalogo = [{
        "catalogo" : catalogo,
        "ofertas" : listaOfertas.filter(id_catalogo_oferta = catalogo.id)
    } for catalogo in catalogo_list]
    
    if (request.method == 'POST'):
        jsonFilter = json.loads(request.body)
        filterEstado = jsonFilter.get('filter_estado')
        filterProducto = jsonFilter.get('filter_producto')
        if (int(filterEstado) > 0 and int(filterProducto) > 0):
            ofertas_catalogo = [{
                "catalogo" : catalogo,
                "ofertas" : listaOfertas.filter(id_estado_oferta=filterEstado)
                                        .filter(id_producto=filterProducto)
                                        .filter(id_catalogo_oferta=catalogo.id),
            }
            for catalogo in catalogo_list]
        elif (int(filterEstado) > 0):
            ofertas_catalogo = [{
                "catalogo" : catalogo,
                "ofertas": listaOfertas.filter(id_estado_oferta=filterEstado)
                                       .filter(id_catalogo_oferta=catalogo.id),
            }for catalogo in catalogo_list]
        elif (int(filterProducto) > 0):
            ofertas_catalogo = [{
                "catalogo" : catalogo,
                "ofertas": listaOfertas.filter(id_producto=filterProducto)
                                        .filter(id_catalogo_oferta=catalogo.id),
            } for catalogo in catalogo_list]

    page = request.GET.get('page', 1)
    paginator = Paginator(ofertas_catalogo, 3)

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
    print(ofertas.object_list)
    listaOfertasJson = [{
        "catalogo" : { "id" : oferta_catalogo.get('catalogo').id,
                       "fecha_ini" : oferta_catalogo.get('catalogo').fecha_inicio.strftime('%Y-%m-%d'),
                       "fecha_fin" : oferta_catalogo.get('catalogo').fecha_fin.strftime('%Y-%m-%d')
                        },
        "ofertas" : [{
                    "pk": oferta.id,
                    "fecha": oferta.fecha.strftime('%Y-%m-%d %H:%M'),
                    "precio": oferta.precio,
                    "cantidad": oferta.cantidad,
                    "vendido": oferta.cantidad-oferta.cantidad_disponible,
                    "estado": oferta.id_estado_oferta.nombre,
                    "producto": oferta.id_producto.nombre,
                    "unidad": oferta.id_producto.id_tipo_unidad.abreviatura,
                    "editable": oferta.id_estado_oferta.id == 1,   # id estado pendiente
                    "catalogo_id": oferta.id_catalogo_oferta.id
                }for oferta in oferta_catalogo.get('ofertas')]
    } for oferta_catalogo in ofertas.object_list]
    json_ = [{"ofertas": listaOfertasJson,
              "ofertasPag": ofertasPag
              }]

    return HttpResponse(json.dumps(json_))


@csrf_exempt
def ver_ofertas(request):
    return render(request, "verOfertas.html")

# Método que realiza la creación de la oferta
@csrf_exempt
def crearOferta(request):
    estadoOferta = EstadoOferta.objects.get(id=1)  # Ofertas pendientes
    if request.method == 'POST':
        dias = CalculoDiasCatalogoOfertas()
        # hoy = hoy - timedelta(4) ##Para lanzar ejemplo con cualquier dia
        hoy = dias[0]
        print("hoy: ", hoy)
        intdia = hoy.strftime("%w")
        dia = diaSemana(intdia)
        print("Dia de la semana: ", dia)

        if (dia == 'Domingo'):
            print('Las ofertas solo pueden realizarse de Lunes a Sabado')
            # return mensaje
            json_response_s = [{'mensaje': "Las ofertas solo pueden realizarse de Lunes a viernes"}]
            data_convert_s = json.dumps(json_response_s)
            return HttpResponse(data_convert_s, content_type='application/json')
        #elif (dia == 'Sabado'):
        #     print('Las ofertas solo pueden realizarse de Lunes a viernes')
        #     # return mensaje
        #     json_response_s = [{'mensaje': "Las ofertas solo pueden realizarse de Lunes a viernes"}]
        #     data_convert_s = json.dumps(json_response_s)
        #     return HttpResponse(data_convert_s, content_type='application/json')
        else:
            print('Dia disponible para realizar ofertas')
            # Fecha inicio Oferta
            _diaInicioOferta = dias[1]
            _diaFinOferta = dias[2]

            #Consulta catalogo de ofertas para la semana
            _catalogoOferta = CatalogoOfertas.objects.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy)
            #catalogo = CatalogoOfertas()
            print ('Catalogos de ofertas en el rango de fechas: ',_catalogoOferta.count())
            if _catalogoOferta.count() > 0:
                print('Existe catalogo oferta para esta semana')
                catalogo = _catalogoOferta.first()
            else:
                print('No existe catalogo para la semana, se creara uno')
                catalogo = CatalogoOfertas(fecha_inicio= _diaInicioOferta,
                                           fecha_fin=_diaFinOferta,
                                           activo=True)
                catalogo.save()
                print('Creacion correcta del catalogo')
                #_catalogoOferta = CatalogoOfertas.objects.filter(fecha_inicio__gte=_diaInicioOferta, fecha_fin__gte=_diaFinOferta)


        #Se crea el objeto oferta a guardar
        jsonObj = json.loads(request.body)
        precio = jsonObj['precio']
        print ('precio: ', precio)
        cantidad = jsonObj['cantidad']
        print ('cantidad: ', cantidad)
        idproducto = jsonObj['producto']
        producto = Producto.objects.get(id=idproducto)
        idproductor = jsonObj['user']
        print('id productor: ', idproductor)
        productor = Usuario.objects.get(auth_user_id=idproductor)


        #cantidad_disponible***
        print ('Creacion de la oferta')
        print ('precio: ', precio)
        print ('cantidad: ', cantidad)
        print ('cantidad_disponible: ', 50)
        print ('id_estado_oferta: ', estadoOferta)
        print ('id_producto: ', producto)
        print ('id_productor: ', productor)
        print ('id_catalogo_oferta: ', catalogo)

        oferta_model = Oferta(precio=precio, cantidad=cantidad, cantidad_disponible=cantidad, id_estado_oferta=estadoOferta,
                              id_producto=producto, id_productor=productor, id_catalogo_oferta=catalogo)
        oferta_model.save()
        print('Oferta creada exitosamente')
        json_response = [{'mensaje': "OK"}]
        data_convert = json.dumps(json_response)
        return HttpResponse(data_convert, content_type='application/json')


#Metodo que calcula los días en que la oferta estaría
# disponible de acuerdo al día actual de la consult
def CalculoDiasCatalogoOfertas():
    # Hoy
    hoy = datetime.now().date()
    hoy = hoy - timedelta(2) ##Para lanzar ejemplo con cualquier dia
    print ('Hoy TEST: ', hoy)
    intdia = hoy.strftime("%w")
    dia = diaSemana(intdia)
    #print("Dia de la semana: ", dia)
    _numeroDiasOferta = 5

    if (dia == 'Domingo'):
        #print 'Las ofertas solo pueden realizarse de Lunes a viernes'
        #Fecha inicio Oferta
        _diaInicioOferta = hoy + timedelta(days=1)
        #print('Inicio de Oferta: ', _diaInicioOferta)
    else:
        #print 'Dia disponible para realizar ofertas'
        # Fecha inicio Oferta
        _intDiaInicioOferta = int(intdia) - (int(intdia) - 1)
        #print('int inicio oferta', _intDiaInicioOferta)
        _diaInicioOferta = hoy - timedelta(days=int(intdia) - 1)
        #print('Inicio de Oferta: ', _diaInicioOferta)

    _diaFinOferta = _diaInicioOferta + timedelta(days=_numeroDiasOferta)
    #print('Fin de Oferta: ', _diaFinOferta)
    return (hoy, _diaInicioOferta, _diaFinOferta)

# Metodo que retorna el nombre del día
# cuando se envía el id del día.
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


#Metodo que realiza la consulta de la semana actual de oferta
@csrf_exempt
def ConsultaFechaSemanaOferta(request):
    if request.method == 'GET':
        try:
            diasOferta = CalculoDiasCatalogoOfertas()
            #_hoy = diasOferta[0]
            _diaInicioOferta = diasOferta[1]
            #print('Fecha Inicio: ', _diaInicioOferta)
            _diaFinOferta = diasOferta[2]
            #print('Fecha Fin: ', _diaFinOferta)
            json_response = \
                [{'semanaOferta': ' ' + _diaInicioOferta.strftime(" %d/%m/%Y") + ' a ' + _diaFinOferta.strftime(" %d/%m/%Y")}]
            data_convert = json.dumps(json_response)
            return HttpResponse(data_convert, content_type='application/json')
        except:
            json_response = [{'mensaje': "Fail"}]
            data_convert = json.dumps(json_response)
            return HttpResponse(data_convert, content_type='application/json')
    else:
        json_response = [{'mensaje': "Fail"}]
        data_convert = json.dumps(json_response)
        return HttpResponse(data_convert, content_type='application/json')

# Metodo que realiza la consulta de lista de productos
# por listos para ofertar
@csrf_exempt
def ConsultarProductosaOfertar(request):
    # filtrar para obtener productos que NO estén en las ofertas hechas
    dias = CalculoDiasCatalogoOfertas()
    hoy = dias[0]
    print ('Hoy: ', hoy)
    intdia = hoy.strftime("%w")
    dia = diaSemana(intdia)
    print("Dia de la semana: ", dia)

    if (dia == 'Domingo'):
        print('Las ofertas solo pueden realizarse de Lunes a Sabado')
        # return mensaje
        json_response_s = [{'mensaje': "Las ofertas solo pueden realizarse de Lunes a Sabado"}]
        data_convert_s = json.dumps(json_response_s)
        return HttpResponse(data_convert_s, content_type='application/json')
    else:
        productos_ini = list(Producto.objects.filter(activo=True).order_by('nombre'))
        listaProductos = list()
        if (len(productos_ini) > 0):
            _catalogoOferta = CatalogoOfertas.objects.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy)
            if (_catalogoOferta.count() > 0):
                ofertas = Oferta.objects.filter(id_catalogo_oferta_id=_catalogoOferta,
                                                id_productor__auth_user_id=request.user.id)
            for item in productos_ini:
                try:
                    # Fecha inicio Oferta
                    # Se le adiciona un día a la fecha porque en el filtro
                    # los registros de la fechaFin son tomados hasta las 00:00.1
                    # Si se le suma un dìa al afecha fin, se tiene en cuenta
                    # en el filtro las 24 hrs del día de la fecha fin.
                    #nuevafechaFin = _diaFinOferta + timedelta(days=1)
                    #Se busca el id de catálogo de la semana
                    if (_catalogoOferta.count() > 0):
                        producto = ofertas.filter(id_producto_id=item)
                        if (producto.count() > 0):
                            print('El producto', item.nombre, ' ya ha sido ofertado')

                        else:
                            print('El producto', item.nombre, ' no ha sido ofertado')
                            listaProductos.append(item)
                except Oferta.DoesNotExist:
                    print('No existen ofertas')
                except CatalogoOfertas.DoesNotExist:
                    print('No existen Catalogos de ofertas')
            page = request.GET.get('page', 1)
            paginator = Paginator(listaProductos, 5)
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

            listaProductosJson = [{
                "pk": producto.id,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "tipoUnidad": producto.id_tipo_unidad.abreviatura,
                "categoria": producto.id_categoria.nombre,
            } for producto in productos.object_list]

            jsonReturn = [{"productos": listaProductosJson,
                           "productosPag": productosPag
                           }]

            return HttpResponse(json.dumps(jsonReturn), content_type='application/json')
        else:
            json_response = [{'mensaje': "No hay productos para ofertar"}]
            data_convert = json.dumps(json_response)
            return HttpResponse(data_convert, content_type='application/json')

@csrf_exempt
def ver_productos(request):
    #user = request.user
    #print user.id
    return render(request, "productosaOfertar.html")


@csrf_exempt
def editarOferta(request):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(auth_user_id=request.user.id)
            jsonObj = json.loads(request.body)
            precio = jsonObj['precio']
            cantidad = jsonObj['cantidad']
            idoferta = jsonObj['oferta']

            if (int(idoferta) > 0):
                oferta = Oferta.objects.filter(id_productor=usuario.id).filter(id_estado_oferta=1).get(id=idoferta)  # id estado pendiente
                oferta.cantidad = cantidad
                oferta.cantidad_disponible = cantidad
                oferta.precio = precio
                oferta.save()
            json_response = [{'mensaje': "OK"}]
            data_convert = json.dumps(json_response)
            return HttpResponse(data_convert, content_type='application/json')
        except Oferta.DoesNotExist:
            return JsonResponse({'mensaje': 'No se puede modificar la oferta'})

@csrf_exempt
def listarProductosOfertas(request):
    usuario = Usuario.objects.get(auth_user_id=request.user.id)
    listaOfertas = Oferta.objects.filter(id_productor=usuario.id)\
                                  .distinct('id_producto__nombre')\
                                  .order_by('id_producto__nombre')
    if request.method == "GET":
        lista_productos = [{'id': oferta.id_producto.id,
                            'nombre': oferta.id_producto.nombre,
                            'descripcion': oferta.id_producto.descripcion,
                            'activo': oferta.id_producto.activo} for oferta in listaOfertas]
    data_convert = json.dumps(lista_productos)
    return HttpResponse(data_convert)
