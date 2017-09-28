# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EstadoOferta

class EstadoOfertaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', )
# Register your models here.

admin.site.register(EstadoOferta, EstadoOfertaAdmin)