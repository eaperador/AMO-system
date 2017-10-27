# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
# Create your tests here.
class ApirestTestCase(TestCase):
    # Para verificar la integracion con CodeShip
    def test_echo_for_CI(self):
        """Animals that can speak are correctly identified"""
        print ("Ejecuta el test de Apirest")
        self.assertEqual('Modulo apirest', 'Modulo apirest')