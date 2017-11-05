# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 06:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrador', '0001_initial'),
        ('comun', '0001_initial'),
        ('consumidor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogoOfertas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('activo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CompraOfertado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('id_item_compra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='consumidor.ItemCompra')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoOferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('cantidad_disponible', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('id_catalogo_oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productor.CatalogoOfertas')),
                ('id_estado_oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productor.EstadoOferta')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrador.Producto')),
                ('id_productor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comun.Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='compraofertado',
            name='id_oferta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productor.Oferta'),
        ),
    ]
