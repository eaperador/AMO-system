# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from time import sleep


from datetime import datetime
from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from selenium.webdriver.common.by import By

from .models import CatalogoProductos


def login(self):
    link = self.browser.find_element_by_id('iniciar_sesion')
    link.click()
    sleep(1)

    nombreUsuario = self.browser.find_element_by_id('inputUsername')
    nombreUsuario.send_keys('administrador')
    sleep(1)

    clave = self.browser.find_element_by_id('inputPassword')
    clave.send_keys('usuarioA')
    sleep(1)

    botonLogin = self.browser.find_element_by_id('btn_iniciarSesion')
    botonLogin.click()
    sleep(2)

class AdministradorTestCase(TestCase):

    def setUp(self):
        #self.browser = webdriver.Chrome("C:\\Users\\Oscar Amaya\\Documents\\tmp\delete\\chromedriver31.exe")
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_menu_available(self):
        self.browser.get('http://localhost:8000')

        sleep(2)
        login(self)
        sleep(5)
        a = self.browser.find_element(By.XPATH, '//a[text()="Cerrar semana"]')
        self.assertIn('CERRAR SEMANA', a.text)

    def test_cierre_catalogo(self):
        self.browser.get('http://localhost:8000')
        sleep(2)
        login(self)
        menuCerrar = self.browser.find_element(By.XPATH, '//a[text()="Cerrar semana"]')
        menuCerrar.click()
        sleep(5)
        mensajeCierre = self.browser.find_element_by_id('cierreMsj')
        today = datetime.now().date()
        sleep(3)
        catalogo = CatalogoProductos.objects.filter(fecha_inicio__lte=today).\
                                             filter(fecha_fin__gte=today).\
                                             filter(activo=True).first()
        self.assertIsNone(catalogo)

    def test_sin_catalogo(self):
        self.browser.get('http://localhost:8000')
        sleep(2)
        login(self)
        menuCerrar = self.browser.find_element(By.XPATH, '//a[text()="Cerrar semana"]')
        menuCerrar.click()
        sleep(5)
        mensajeCierre = self.browser.find_element_by_id('cierreMsj')
        self.assertEquals(mensajeCierre.text, 'No hay catalogo para cerrar')

