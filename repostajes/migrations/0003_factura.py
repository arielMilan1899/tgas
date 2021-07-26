# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-03-04 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20210302_2054'),
        ('repostajes', '0002_auto_20210302_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('importe', models.DecimalField(decimal_places=3, max_digits=10)),
                ('es_mensual', models.BooleanField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
        ),
    ]