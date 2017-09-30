# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogoOferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_definido', models.FloatField()),
                ('cantidad_definida', models.IntegerField()),
                ('catalogo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Catalogo')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.CharField(max_length=1000)),
                ('imagen', models.ImageField(null=True, upload_to='images')),
                ('estado', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='catalogooferta',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administrador.Producto'),
        ),
    ]
