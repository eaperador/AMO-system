from time import sleep
from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.common.by import By


def login(self):
    link = self.browser.find_element_by_id('iniciar_sesion')
    link.click()
    sleep(1)

    nombreUsuario = self.browser.find_element_by_id('inputUsername')
    nombreUsuario.send_keys('prod1')
    sleep(1)

    clave = self.browser.find_element_by_id('inputPassword')
    clave.send_keys('usuarioprod1')
    sleep(1)

    botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
    botonLogin.click()
    sleep(2)


class ProductorTestCase(TestCase):
    def setUp(self):
        #self.browser = webdriver.Chrome("C:\\Users\\Oscar Amaya\\Documents\\tmp\\delete\\chromedriver31.exe")
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
        
    def test_filter(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        opCount = len(listaProductos.find_elements_by_tag_name("option"))
        self.assertEquals('Todos...', listaProductos.find_elements_by_tag_name("option")[0].text)

    def test_filter_a_lot_of_products(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        self.assertTrue(len(listaProductos.find_elements_by_tag_name("option")) > 1)

    def test_filter_a_lot_of_products(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        self.browser.find_element_by_xpath("//select[@id='listaProductos']/option[text()='Naranja']").click()
        sleep(1)

        offer_list = self.browser.find_element_by_id('listaOfertas')
        otherProds = 0
        for offer in offer_list.find_elements_by_tag_name('tr'):
            self.assertEquals(offer.find_elements_by_tag_name('td')[1].text, 'Naranja')

class ProductorEditOfertaTestCase(TestCase):
    def setUp(self):
        # self.browser = webdriver.Chrome("C:\\Users\\Oscar Amaya\\Documents\\tmp\\delete\\chromedriver31.exe")
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()


    def test_edit_available(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        edit_link = self.browser.find_element_by_id('to_edit_1')
        self.assertIsNotNone(edit_link)

    def test_edit_modal(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        edit_link = self.browser.find_element_by_id('to_edit_1')
        edit_link.click()
        sleep(1)

        labelCant = self.browser.find_element(By.XPATH, '//h4[text()="Editar oferta producto"]')
        self.assertIn('Editar oferta producto', labelCant.text)

    def test_edit_modal(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        edit_link = self.browser.find_element_by_id('to_edit_1')
        edit_link.click()
        sleep(1)

        labelCant = self.browser.find_element(By.XPATH, '//h4[text()="Editar oferta producto"]')
        self.assertIn('Editar oferta producto', labelCant.text)

    def test_edit_function(self):
        self.browser.get('http://localhost:8000')
        login(self)
        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(1)

        edit_link = self.browser.find_element_by_id('to_edit_1')
        edit_link.click()
        sleep(1)

        precio = self.browser.find_element_by_id('inputPrecio')
        precio.send_keys('9999')
        sleep(1)

        cant = self.browser.find_element_by_id('inputCantidad')
        cant.send_keys('5555')
        sleep(1)

        botonEdit = self.browser.find_element_by_id('editOferBtn')
        botonEdit.click()
        sleep(1)

        labelPrecio = self.browser.find_element_by_id('precio_1')
        self.assertIn('9999', labelPrecio.text)

        labelCant = self.browser.find_element_by_id('cant_1')
        self.assertIn('5555', labelCant.text)
