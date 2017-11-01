# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-31 23:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumidor', '0001_initial'),
        ('productor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompraOfertado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('id_item_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumidor.ItemCompra')),
                ('id_oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productor.Oferta')),
            ],
        ),
    ]
