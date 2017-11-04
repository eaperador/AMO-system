from time import sleep
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class ProductorTestCase(TestCase):

    def setUp(self):
        #self.browser = webdriver.Chrome("C:\\Users\\CATHERIN\\Documents\\chromedriver.exe")
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_filter(self):
        self.browser.get('http://localhost:8000')

        link = self.browser.find_element_by_id('iniciar_sesion')
        link.click()

        sleep(2)

        nombreUsuario = self.browser.find_element_by_id('inputUsername')
        nombreUsuario.send_keys('prod1')
        sleep(1)

        clave = self.browser.find_element_by_id('inputPassword')
        clave.send_keys('usuarioprod1')
        sleep(1)

        botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
        botonLogin.click()
        sleep(10)

        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(5)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        opCount = len(listaProductos.find_elements_by_tag_name("option"))
        self.assertEquals('Todos...', listaProductos.find_elements_by_tag_name("option")[0].text)

    def test_filter_a_lot_of_products(self):
        self.browser.get('http://localhost:8000')

        link = self.browser.find_element_by_id('iniciar_sesion')
        link.click()

        sleep(2)

        nombreUsuario = self.browser.find_element_by_id('inputUsername')
        nombreUsuario.send_keys('prod1')
        sleep(1)

        clave = self.browser.find_element_by_id('inputPassword')
        clave.send_keys('usuarioprod1')
        sleep(1)

        botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
        botonLogin.click()
        sleep(10)

        continue_link = self.browser.find_element_by_id('id_consulatarOfertas')
        continue_link.click()
        sleep(5)

        span = self.browser.find_element(By.XPATH, '//label[text()="Producto:"]')
        self.assertIn('Producto:', span.text)

        listaProductos = self.browser.find_element_by_id('listaProductos')
        self.assertTrue(len(listaProductos.find_elements_by_tag_name("option")) > 1)
