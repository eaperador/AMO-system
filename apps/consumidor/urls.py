from django.conf.urls import url

from ..consumidor import views

urlpatterns = [
    url(r'catalogo_compras/$', views.catalogo_compras, name='catalogo_compras'),
    url(r'^listar_productos_catalogo/$', views.listar_productos_catalogo_view, name='listar_productos_catalogo'),
    url(r'^seleccionarProductos/$', views.select_productos, name="seleccionarProductos"),
    url(r'^agregar_producto/$', views.agregar_producto, name='agregar_producto'),
    url(r'^eliminar_producto/$', views.eliminar_producto, name='eliminar_producto'),
    url(r'^items_carrito/$', views.items_carrito, name='items_carrito'),
    url(r'^seleccionarProducto/(?P<id>.+)/(?P<page>.+)/$', views.select_producto, name="seleccionarProducto")]
