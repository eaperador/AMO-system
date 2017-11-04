from telnetlib import EC
from time import sleep, time

from selenium.webdriver.support.wait import WebDriverWait

_author_ = 'asistente'
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class ProductorTestCase(TestCase):
    # Para verificar la integracion con CodeShip


    def setUp(self):
        #self.browser = webdriver.Chrome("C:\\Users\\Oscar Amaya\\Documents\\tmp\\delete\\chromedriver33.exe")
        self.browser = webdriver.Chrome()

        self.browser.get('http://www.google.com/xhtml');
        self.browser.implicitly_wait(2)  # Let the user actually see something!
        search_box = self.browser.find_element_by_name('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        self.browser.implicitly_wait(2)  # Let the user actually see something!
        self.browser.quit()


    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:8000/productor/ver_ofertas')
        self.assertIn('Productor', self.browser.title)