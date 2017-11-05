from time import sleep
from unittest import TestCase

from django.contrib.auth import authenticate

from ..comun.models import Usuario, Cooperativa, Rol
from ..administrador.models import Producto, Categoria, TipoUnidad
from ..productor.models import Oferta, EstadoOferta, CatalogoOfertas
from django.contrib.auth.models import User

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def createUser(self):
    self.browser.get('http://localhost:8000/admin')
    nombreUsuario = self.browser.find_element_by_id('id_username')
    nombreUsuario.send_keys('admin')
    #sleep(1)

    clave = self.browser.find_element_by_id('id_password')
    clave.send_keys('useradmin')
    #sleep(1)

    #botton = self.browser.find_element_by_tag_name('input')
    botton = self.browser.find_element_by_xpath("//input[@type='submit' and @value='Identificarse']")
    botton.click()
    #sleep(1)
    '''
    # AuthUser
    link = self.browser.find_element_by_partial_link_text('/admin/auth/user/')
    link.click()
    sleep(1)

    add = self.browser.find_element_by_partial_link_text('/admin/auth/user/add')
    add.click()
    sleep(1)
    '''
    self.browser.get('http://localhost:8000/admin/auth/user/add/')
    nombreUsuario = self.browser.find_element_by_id('id_username')
    nombreUsuario.send_keys('prodT')
    clave = self.browser.find_element_by_id('id_password1')
    clave.send_keys('testuserprod1')
    clave2 = self.browser.find_element_by_id('id_password2')
    clave2.send_keys('testuserprod1')
    save1 = self.browser.find_element_by_xpath("//input[@type='submit' and @value='Guardar y continuar editando']")
    save1.click()
    nombre = self.browser.find_element_by_id('id_first_name')
    nombre.send_keys('Productor')
    clave = self.browser.find_element_by_id('id_last_name')
    clave.send_keys('Test')
    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    save2 = self.browser.find_element_by_xpath("//input[@type='submit' and @value='Guardar']")
    save2.click()

    #self.browser.get('http://localhost:8000/admin/comun/usuario/add/')
    #self.browser.execute_script(" $('#pagination').val(test.jpg)")


class ProductorTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("C:\\Users\\Oscar Amaya\\Documents\\tmp\\delete\\chromedriver31.exe")
        #self.browser = webdriver.Chrome()
        '''self.browser.implicitly_wait(2)
        createUser(self)
        self.browser.get('http://localhost:8000/admin/logout')
        #Usuario
        #self.user = User(username="prodTest",first_name="Roberto",last_name="Perez",email="cl.santana@uniandes.edu.co")
        #self.user.set_password('userprodtest')
        #self.user.save()
        self.usuario = Usuario(foto="images/user/photo1.jpg",descripcion="Productor Test",telefono="3432345",auth_user_id=user,id_cooperativa=self.cooperativa, id_rol=self.rol)
        self.usuario.save()
        #Productos
        #Ofertas
        self.oferta = Oferta(precio=5000,cantidad=1000,cantidad_disponible=100,fecha=datetime.datetime.today(),id_catalogo_oferta=self.catalogo,id_producto=self.producto1,id_productor=self.usuario,id_estado_oferta=self.estadoOferta)
        self.oferta.save()'''
    def tearDown(self):
        '''self.oferta.delete()
        self.catalogo.delete()
        self.estadoOferta.delete()
        self.producto1.delete()
        self.tipoUnidad.delete()
        self.categoria.delete()
        self.usuario.delete()
        self.user.delete()
        self.rol.delete()
        self.cooperativa.delete()'''
        self.browser.quit()

    def test_filter(self):
        self.browser.get('http://localhost:8000')

        link = self.browser.find_element_by_id('iniciar_sesion')
        link.click()

        sleep(2)

        nombreUsuario = self.browser.find_element_by_id('inputUsername')
        nombreUsuario.send_keys('prod1')
       # sleep(2)

        clave = self.browser.find_element_by_id('inputPassword')
        clave.send_keys('usuarioprod1')
       # sleep(2)

        botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
        botonLogin.click()
        print(self.browser.current_url)
        sleep(2)

        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        span = self.browser.find_element(By.XPATH, '//label[text()="Productos:"]')
        self.assertIn('Productos:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        opCount = len(listaProductos.find_elements_by_tag_name("option"))
        self.assertEquals('Todos...', listaProductos.find_elements_by_tag_name("option")[0].text)

    '''
    def test_filter_a_lot_of_products(self):
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
        sleep(20)

        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(5)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        self.assertTrue(len(listaProductos.find_elements_by_tag_name("option")) > 1)'''


