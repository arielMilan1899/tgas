# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from fmaestros.models import Estacion, Combustible
from usuarios.models import Usuario, Matricula


class Repostaje(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    usuario = models.ForeignKey(Usuario)
    matricula = models.ForeignKey(Matricula)
    estacion = models.ForeignKey(Estacion)
    albaran = models.CharField(max_length=16, unique=True)
    combustible = models.ForeignKey(Combustible)
    litros = models.DecimalField(max_digits=10, decimal_places=3)
    precio = models.DecimalField(max_digits=5, decimal_places=3)
    importe = models.DecimalField(max_digits=10, decimal_places=3)


class Factura(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    codigo = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(Usuario)
    importe = models.DecimalField(max_digits=10, decimal_places=3)
    es_mensual = models.BooleanField()
