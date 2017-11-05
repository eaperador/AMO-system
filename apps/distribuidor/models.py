# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from ..comun.models import Usuario

class Ruta(models.Model):
    descripcion = models.CharField(max_length=1000)
    id_usuario_distribuidor = models.ForeignKey(Usuario, null=False)

class Entrega(models.Model):
    estado = models.CharField(max_length=1000)
    id_ruta = models.ForeignKey(Ruta, null=False)