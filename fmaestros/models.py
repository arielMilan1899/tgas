# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from django.db import models
from django.utils import encoding
from django.utils.crypto import constant_time_compare, get_random_string
from tgas.fcomunes import decimal2str


# Create your models here.
class Empresa(models.Model):
    codigo = models.CharField(max_length=16, unique=True)
    nombre = models.CharField(max_length=60, unique=True)
    razon_social = models.CharField(max_length=60, null=True, blank=True)
    cif = models.CharField(max_length=16, null=True, blank=True)
    cp = models.CharField(max_length=11, null=True, blank=True)
    direccion =  models.CharField(max_length=70, null=True, blank=True)
    poblacion = models.CharField(max_length=70, null=True, blank=True)
    provincia = models.CharField(max_length=70, null=True, blank=True)
    telefono = models.CharField(max_length=70, null=True, blank=True)
    pais = models.CharField(max_length=70, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        dato='%s' % (self.nombre,)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')

    class Meta:
        verbose_name_plural = "Empresas"


class Cuenta(models.Model):
    """
    ambigus, taquilla, futbol_base, primer_equipo ...
    """
    codigo = models.CharField(max_length=16, unique=True)
    nombre = models.CharField(max_length=60, unique=True)

    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        dato='%s' % (self.nombre,)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')

    class Meta:
        verbose_name_plural = "Tipos de Gastos e Ingresos"


class Apunte(models.Model):
    """
    Fecha de la anotación.
    Número que hace el asiento a lo largo del ejercicio. (vamos a usar el ID)
    Cuenta que intervienen (no en el sentido del PGC).
    Importe
    Breve descripción de la operación.
    Gasto o Ingreso
    """
    fecha = models.DateField()
    descripcion = models.CharField(max_length=60)
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    es_gasto = models.BooleanField()
    cuenta = models.ForeignKey(Cuenta)

    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        dato='%s %s %s %s' % (self.fecha, self.descripcion, self.importe, self.es_gasto)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')

    class Meta:
        verbose_name_plural = "Apunte Contable"

        indexes = [
            models.Index(['fecha']),
            models.Index(['es_gasto']),
            models.Index(['cuenta']),
        ]

# _____________ INI Código añadido por crea_prototipo_fmaestros.py

class ComunidadAutonoma(models.Model):
    """
    """
    codigo = models.CharField(max_length=2, unique=True)
    codigo_iso = models.CharField(max_length=4, unique=True)
    nombre = models.CharField(max_length=32)

    def __str__(self):
        dato = '%s - %s' % (self.codigo, self.nombre)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')


class Provincia(models.Model):
    codigo = models.CharField(max_length=16, unique=True)
    nombre = models.CharField(max_length=60, unique=True)
    ccaa = models.ForeignKey(ComunidadAutonoma, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Provincias"
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        dato = "%s (%s)" % (self.nombre, self.ccaa.nombre)
        return encoding.smart_str(dato.encode('utf-8'), encoding='utf8', errors='ignore')


# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

# _____________ INI Código añadido por crea_prototipo_fmaestros.py


class Estacion(models.Model):
    codigo = models.CharField(max_length=16, unique=True)
    nombre = models.CharField(max_length=60, unique=True)

    observaciones = models.TextField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

    provincia = models.ForeignKey(Provincia)
    geo_latitud = models.DecimalField(max_digits=22, decimal_places=16)
    geo_longitud = models.DecimalField(max_digits=22, decimal_places=16)
    direccion = models.CharField(max_length=70)

    token = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Estaciones"
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        dato = self.nombre.encode('utf-8')
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')

    def save(self, *args, **kwargs):
        modo_creacion = self.id is None

        super(Estacion, self).save(*args, **kwargs)

        if modo_creacion:
            self.generar_token()
            super(Estacion, self).save()

    def precios(self):
        """Retorna los precios de los combustibles para esta Estacion"""

        precios = []

        for combustible in Combustible.objects.all():
            try:
                precio = PrecioCombustible.objects.get(combustible_id=combustible.id, estacion_id=self.id)
            except:
                precio = PrecioCombustible(combustible=combustible, estacion=self)

            precios.append(precio)

        return precios

    def posicion_gmaps(self):
        """Retorna la posicion GPS para ser usada en Google Maps"""

        return "%.6f,%.6f" % (self.geo_latitud, self.geo_longitud)

    def generar_token(self):
        """Genera un nuevo token de acceso aleatorio"""

        salt = get_random_string(length=64)
        unique_salt = salt + str(self.id)
        encoded = hashlib.md5(unique_salt.encode('utf-8')).hexdigest()

        self.token = encoded

    def comprobar_token(self, token):
        """Comprueba si el token de acceso es correcto"""
        return constant_time_compare(self.token, token)

# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

# _____________ INI Código añadido por crea_prototipo_fmaestros.py


class Combustible(models.Model):
    codigo = models.CharField(max_length=16, unique=True)
    nombre = models.CharField(max_length=60)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Combustibles"
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        dato = self.nombre.encode('utf-8')
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')


# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

class PrecioCombustible(models.Model):
    estacion = models.ForeignKey(Estacion)
    combustible = models.ForeignKey(Combustible)
    precio = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        unique_together = ('estacion', 'combustible')

    def __str__(self):
        dato = ('%s €' % decimal2str(self.precio)) if self.precio is not None else 'No disponible'
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')
