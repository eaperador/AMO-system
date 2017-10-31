from django.conf.urls import url

from ..consumidor import views

urlpatterns = [
    url(r'catalogo_compras/$', views.catalogo_compras, name='catalogo_compras'),
    url(r'catalogo_compras/agregar_producto/$', views.agregar_producto, name='agregar_producto'),

    ]