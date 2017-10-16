from django.conf.urls import url

import views

urlpatterns = [
    url(r'listarEstados/$', views.listarEstadosOferta, name='listaEstados'),
    url(r'listarOfertas/$', views.listarOfertas, name='listaOfertas'),
    url(r'ver_ofertas/$', views.ver_ofertas, name='ver_ofertas'),
    url(r'crearOferta$', views.crearOferta, name='crearOferta'),
    url(r'editarOferta$', views.editarOferta, name='editarOferta'),
    url(r'listaProductos/$', views.ConsultarProductosaOfertar, name='productosaOfertar'),
    url(r'ver_productos/$', views.ver_productos, name='ver_productos'),
    ]
