# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Producto, Productor, TipoUnidad

# Register your models here.

admin.site.register(Producto, ""),
admin.site.register(TipoUnidad, ""),
admin.site.register(Productor, "")