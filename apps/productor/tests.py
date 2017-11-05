from time import sleep
from unittest import TestCase
from ..comun.models import Usuario, Cooperativa, Rol
from ..administrador.models import Producto, Categoria, TipoUnidad
from ..productor.models import Oferta, EstadoOferta, CatalogoOfertas
from django.contrib.auth.models import User

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


class ProductorTestCase(TestCase):

    def setUp(self):
        #self.browser = webdriver.Chrome("C:\\Users\\CATHERIN\\Documents\\chromedriver.exe")
        #Usuario
        self.cooperativa = Cooperativa(ciudad="Cali")
        self.cooperativa.save()
        self.userDjango = User(username="prodTest",first_name="Roberto",last_name="Perez",email="cl.santana@uniandes.edu.co",password="userprodtest")
        self.userDjango.save()
        self.rol = Rol(nombre="Productor",descripcion="usuario productor")
        self.rol.save()
        self.usuario = Usuario(foto="images/user/photo1.jpg",descripcion="Productor Test",telefono="3432345",auth_user_id=self.userDjango,id_cooperativa=self.cooperativa, id_rol=self.rol)
        self.usuario.save()
        #Productos
        self.categoria = Categoria(nombre="Frutas")
        self.categoria.save()
        self.tipoUnidad = TipoUnidad(nombre="Libra",abreviatura="LB")
        self.tipoUnidad.save()
        self.producto1 = Producto(nombre="Naranja",descripcion="Futa dulce",foto="images/producto/photo1.jpg",activo=True,id_categoria=self.categoria,id_tipo_unidad=self.tipoUnidad)
        self.producto1.save()
        #Ofertas
        self.estadoOferta = EstadoOferta(nombre="Pendiente por Aprobacion")
        self.estadoOferta.save()
        self.catalogo = CatalogoOfertas(fecha_inicio=datetime.datetime.today(),fecha_fin=datetime.datetime.today(),activo=True)
        self.catalogo.save()
        self.oferta = Oferta(precio=5000,cantidad=1000,cantidad_disponible=100,fecha=datetime.datetime.today(),id_catalogo_oferta=self.catalogo,id_producto=self.producto1,id_productor=self.usuario,id_estado_oferta=self.estadoOferta)
        self.oferta.save()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def test_loguin(self):
        self.browser.get('http://localhost:8000')

        link = self.browser.find_element_by_id('iniciar_sesion')
        link.click()

        sleep(2)

        nombreUsuario = self.browser.find_element_by_id('inputUsername')
        nombreUsuario.send_keys('prodTest')
        sleep(1)

        clave = self.browser.find_element_by_id('inputPassword')
        clave.send_keys('userprodtest')
        sleep(1)

        botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
        botonLogin.click()
        sleep(10)

        self.browser.get('http://localhost:8000#id_consulatarOfertas')
        sleep(5)

        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        sleep(5)
        continue_link.click()
        sleep(5)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        opCount = len(listaProductos.find_elements_by_tag_name("option"))
        self.assertEquals('Todos...', listaProductos.find_elements_by_tag_name("option")[0].text)


    #def test_filter(self):
    #    self.browser.get('http://localhost:8000')
#
    #    link = self.browser.find_element_by_id('iniciar_sesion')
    #    link.click()
#
    #    sleep(2)
#
    #    nombreUsuario = self.browser.find_element_by_id('inputUsername')
    #    nombreUsuario.send_keys('prodTest')
    #    sleep(1)
#
    #    clave = self.browser.find_element_by_id('inputPassword')
    #    clave.send_keys('userprodtest')
    #    sleep(1)
#
    #    botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
    #    botonLogin.click()
    #    sleep(20)
#
    #    continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
    #    continue_link.click()
    #    sleep(5)
#
    #    span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
    #    self.assertIn('Producto:', span.text)
#
    #    listaProductos = self.browser.find_element_by_id('listaProductos')
    #    opCount = len(listaProductos.find_elements_by_tag_name("option"))
    #    self.assertEquals('Todos...', listaProductos.find_elements_by_tag_name("option")[0].text)
#
    #def test_filter_a_lot_of_products(self):
    #    self.browser.get('http://localhost:8000')
#
    #    link = self.browser.find_element_by_id('iniciar_sesion')
    #    link.click()
#
    #    sleep(2)
#
    #    nombreUsuario = self.browser.find_element_by_id('inputUsername')
    #    nombreUsuario.send_keys('prodTest')
    #    sleep(1)
#
    #    clave = self.browser.find_element_by_id('inputPassword')
    #    clave.send_keys('userprodtest')
    #    sleep(1)
#
    #    botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
    #    botonLogin.click()
    #    sleep(20)
#
    #    continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
    #    continue_link.click()
    #    sleep(5)
#
    #    span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
    #    self.assertIn('Producto:', span.text)
#
    #    listaProductos = self.browser.find_element_by_id('listaProductos')
    #    self.assertTrue(len(listaProductos.find_elements_by_tag_name("option")) > 1)

    def tearDown(self):
        self.oferta.delete()
        self.catalogo.delete()
        self.estadoOferta.delete()
        self.producto1.delete()
        self.tipoUnidad.delete()
        self.categoria.delete()
        self.usuario.delete()
        self.userDjango.delete()
        self.rol.delete()
        self.cooperativa.delete()
        self.browser.quit()