from django.conf.urls import url

import views

urlpatterns = [
    url(r'catalogo_compras/$', views.catalogo_compras, name='catalogo_compras'),
    url(r'agregar_producto/(?P<id>.+)/$', views.agregar_producto, name='agregar_producto'),

    ]