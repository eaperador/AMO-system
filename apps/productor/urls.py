from django.conf.urls import url

from ..productor import views

urlpatterns = [
    url(r'listarEstados/$', views.listarEstadosOferta, name='listaEstados'),
    url(r'listarOfertas/$', views.listarOfertas, name='listaOfertas'),
    url(r'ver_ofertas/$', views.ver_ofertas, name='ver_ofertas'),
    url(r'crearOferta$', views.crearOferta, name='crearOferta'),
    url(r'editarOferta$', views.editarOferta, name='editarOferta'),
    url(r'listaProductos/$', views.ConsultarProductosaOfertar, name='productosaOfertar'),
    url(r'ver_productos/$', views.ver_productos, name='ver_productos'),
    url(r'ver_ofertas_vendidas/$', views.verOfertasVendidas, name='ver_ofertas_vendidas'),
    url(r'ofertas_por_productor/$', views.ConsultaOfertasporProductor, name='ConsultaOfertasporProductor'),
    url(r'listaOfertas/fechayProductor/$', views.ConsultaOfertasporFechayProductor, name='ofertasxFechaProductor'),
    url(r'listaOfertas/fechaProductoryProducto/$', views.ConsultaOfertasporFechaProductoyProductor, name='ofertasxFechaProductorProducto'),
    url(r'listaOfertas/productoryProducto/$', views.ConsultaOfertasporProductoyProductor, name='ofertasxProductorProducto'),
]
