# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-15 01:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0002_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='comun.Rol'),
            preserve_default=False,
        ),
    ]
