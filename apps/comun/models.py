# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    def __unicode__(self):
       return "%s" % (self.nombre)

class Cooperativa(models.Model):
    ciudad = models.CharField(max_length=50)

    def __unicode__(self):
       return "%s" % (self.ciudad)

class Usuario(models.Model):
    foto = models.ImageField(upload_to='images/user',null=True)
    descripcion = models.CharField(max_length=1000,null=True)
    telefono = models.IntegerField(null=True)
    auth_user_id = models.ForeignKey(User, null = False)
    id_rol = models.ForeignKey(Rol,null = False)
    id_cooperativa = models.ForeignKey(Cooperativa, null=True)

    def __unicode__(self):
       return "%s" % (self.auth_user_id.first_name +  " " + self.auth_user_id.last_name)

    def natural_key(self):
        return (self.auth_user_id.first_name +  " " + self.auth_user_id.last_name)

class Direccion(models.Model):
    direccion = models.CharField(max_length=200)
    id_usuario_comprador = models.ForeignKey(Usuario, null=False)

class Finca(models.Model):
    nombre = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='images/user',null=True)
    descripcion = models.CharField(max_length=1000,null=True)
    municipio = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=50)
    id_usuario_productor = models.ForeignKey(Usuario, null=True)