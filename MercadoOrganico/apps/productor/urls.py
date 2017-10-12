from django.conf.urls import url

import views

urlpatterns = [
    url(r'listarEstados/$', views.listarEstadosOferta, name='listaEstados'),
    url(r'listarOfertas/$', views.listarOfertas, name='listaOfertas'),
    url(r'ver_ofertas/$', views.ver_ofertas, name='ver_ofertas'),
    ]
