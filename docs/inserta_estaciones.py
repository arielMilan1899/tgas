# -*- coding: utf8 -*-
"""
  Inserta Estaciones
  Orden:
>>> from docs import inserta_estaciones as ie
>>> ie.inserta_est()
>>> ie.inserta_comb()
>>> ie.inserta_precios()

"""

# ------------------------------------------------------------------------------------------------
from decimal import Decimal

from fmaestros.models import Estacion, Provincia, Combustible, PrecioCombustible

l_estaciones = [
    # codigo, nombre, codigo_provincia, geo_latitud, geo_longitud, direccion
    ('01', 'CARBUGAL COLISEUM', 15, 43.340389, -8.408833, 'CALLE FRANCISCO PEREZ CARBALLO, S/N - A CORUÑA'),
    ('02', 'HAM en ALFAJARIN', 50, 41.604500, -0.689778, 'POLIGONO EL SACO, S/N - ZARAGOZA'),
    ('03', 'CARBUGAL LARAXE', 15, 43.439417, -8.155056, 'CARRETERA N-651 KM. 25,1 - CABANAS'),
    ('04', 'CARBUGAL CORTIÑAN', 15, 43.281222, -8.237417, 'CARRETERA N-VI KM. 576 - BERGONDO'),
]

l_combustibles = [
    # codigo, nombre
    ('01', 'Diesel'),
    ('02', 'Sin plata 95'),
    ('03', 'Gasoleo Calefacción'),
]

l_precios_combustibles = [
    # codigo estacion, codigo combustible, precio
    ('01', '01', Decimal('1.9')),
    ('01', '02', Decimal('1.89')),
    ('01', '03', Decimal('1.5')),
    ('02', '01', Decimal('1.79')),
    ('02', '02', Decimal('1.8')),
    ('02', '03', Decimal('1.75')),
    ('03', '01', Decimal('1.79')),
    ('03', '02', Decimal('1.9')),
    ('03', '03', Decimal('1.55')),
    ('04', '01', Decimal('1.59')),
    ('04', '02', Decimal('1.8')),
    ('04', '03', Decimal('1.58')),
]


# ------------------------------------------------------------------------------------------------


def inserta_est(borrar_actuales=False):
    """
    """
    if borrar_actuales:
        Estacion.objects.all().delete()

    l_ok = []
    l_nok = []

    for t in l_estaciones:
        try:
            provincia = Provincia.objects.get(codigo=t[2])
            # codigo, nombre, codigo_provincia, geo_latitud, geo_longitud, direccion
            estacion = Estacion(codigo=t[0].strip(),
                                nombre=t[1].strip(),
                                provincia=provincia,
                                geo_latitud=t[3],
                                geo_longitud=t[4],
                                direccion=t[5])
            estacion.save()
            l_ok.append((estacion.nombre, estacion.id,))
        except Exception as e:
            l_nok.append((t, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}


def inserta_comb(borrar_actuales=False):
    """
    """
    if borrar_actuales:
        Combustible.objects.all().delete()

    l_ok = []
    l_nok = []

    for t in l_combustibles:
        try:
            # codigo, nombre
            combustible = Combustible(codigo=t[0].strip(),
                                      nombre=t[1].strip())
            combustible.save()
            l_ok.append((combustible.nombre, combustible.id,))
        except Exception as e:
            l_nok.append((t, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}


def inserta_precios(borrar_actuales=False):
    """
    """
    if borrar_actuales:
        PrecioCombustible.objects.all().delete()

    l_ok = []
    l_nok = []

    for t in l_precios_combustibles:
        try:
            estacion = Estacion.objects.get(codigo=t[0])
            combustible = Combustible.objects.get(codigo=t[1])
            precio = PrecioCombustible(estacion=estacion, combustible=combustible, precio=t[2])
            precio.save()
            l_ok.append(precio.id)
        except Exception as e:
            l_nok.append((t, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}
