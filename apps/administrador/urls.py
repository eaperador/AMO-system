from django.conf.urls import url

from ..administrador import views

urlpatterns = (
    url(r'^armarCatalogo$', views.index, name="index"),
    url(r'^addCatalogo/$', views.add_catalogo, name="addCatalogo"),
    url(r'^numeroCatalogo/$', views.numero_nuevo_catalogo, name="numeroCatalogo"),
    url(r'^seleccionarCatalogos/$', views.select_catalogos, name="seleccionarCatalogos"),
    url(r'^seleccionarProductos/$', views.select_productos, name="seleccionarProductos"),
    url(r'^seleccionarProducto/(?P<id>[0-9]+)/$', views.select_producto, name="seleccionarProducto"),
    url(r'^listarOfertas/(?P<productoId>.+)/(?P<filtro>[0-9]+)/$', views.listarOfertas, name="listarOfertas"),
    url(r'^evaluarOfertas/$', views.evaluarOfertas, name="evaluarOfertas"),
    url(r'^catalogoProductos/$', views.catalogoProductos, name="catalogoProductos"),
    url(r'^guardarOferta/$', views.guardarOferta, name="guardarOferta"),
    url(r'^guardarEstadoProducto/$', views.guardarEstadoProducto, name="guardarEstadoProducto"),
    url(r'^guardarCatalogoOferta/$', views.ingresarCatalogoOferta, name="guardarCatalogoOferta"),
    url(r'^getCatalogoOfertaActivo/$', views.get_CatalogoOfertaActivo, name="getCatalogoOfertaActivo"),
    url(r'^getCatalogoProducto/$', views.getCatalogoProducto, name="getCatalogoProducto"),
    url(r'listarProductos/(?P<page>.+)/$', views.listar_productos, name='listarProductos'),
    url(r'crearProducto/$', views.crearProducto, name='crearProducto'),
    url(r'listarTiposUnidad/$', views.tiposUnidad, name='listarTiposUnidad'),
    url(r'listarCategorias/$', views.Categorias, name='listarCategorias'),
    url(r'ingresarProducto/$', views.ingresar_producto, name='ingresarProducto'),
)