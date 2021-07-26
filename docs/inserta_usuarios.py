# -*- coding: utf8 -*-
"""
  Inserta Usuarios
  Orden:
>>> from docs import inserta_usuarios as iu
>>> iu.inserta_usuarios()
>>> iu.inserta_matriculas()
>>> iu.inserta_repostajes()

"""
from decimal import Decimal

from fmaestros.models import Estacion, Provincia, Combustible, PrecioCombustible

# ------------------------------------------------------------------------------------------------
from repostajes.models import Repostaje
from usuarios.models import Usuario, Matricula

l_usuarios = [

    # username, nombre, apellidos, email, nif, cod_provincia, direccion, localidad, telefono
    # Al guardar el usuario debe generarle un password de manera automática y es_admin a False
    ('76500900P', 'Ramón', 'Allo Cundins', 'rallo@telemap.es', '76500900P', 15, 'Conlle S/N', 'Laxe', '600123123'),
    ('66500900P', 'Ariel', 'Barrios', 'abarrios@telemap.es', '66500900P', 16, 'Conlle S/N', 'Laxe', '58316299'),
]

l_matriculas = [
    # codigo, username
    ('QWERTY', '76500900P'),
    ('QWERTU', '76500900P'),
    ('ASDFGH', '66500900P'),
    ('ASDFGJ', '66500900P'),
]

l_repostajes = [
    # username, codigo matricula, codigo estacion, codigo combustible, albaran, litros
    ('76500900P', 'QWERTY', '01', '01', 'ASDQWS', Decimal('24')),
    ('76500900P', 'QWERTY', '01', '01', 'ASDQWA', Decimal('25')),
    ('76500900P', 'QWERTY', '01', '01', 'ASDQWC', Decimal('15')),
    ('76500900P', 'QWERTU', '01', '01', 'ASDQWZ', Decimal('11')),
    ('76500900P', 'QWERTY', '04', '02', 'ZSDQWZ', Decimal('25')),
    ('76500900P', 'QWERTY', '02', '03', 'xSDQWZ', Decimal('20')),
    ('76500900P', 'QWERTU', '02', '03', 'CSDQWZ', Decimal('18')),
    ('76500900P', 'QWERTU', '02', '03', 'SSDVFS', Decimal('10')),
    ('66500900P', 'ASDFGH', '01', '01', 'QSDEAD', Decimal('24')),
    ('66500900P', 'ASDFGH', '01', '01', 'QSDVAD', Decimal('25')),
    ('66500900P', 'ASDFGH', '01', '01', 'QSDCDA', Decimal('15')),
    ('66500900P', 'ASDFGH', '01', '01', 'QSDAZS', Decimal('11')),
    ('66500900P', 'ASDFGJ', '03', '02', 'QSDQAS', Decimal('25')),
    ('66500900P', 'ASDFGH', '02', '03', 'QSDQWD', Decimal('20')),
    ('66500900P', 'ASDFGH', '02', '03', 'QSDQWW', Decimal('18')),
    ('66500900P', 'ASDFGH', '02', '03', 'QSDQWQ', Decimal('10')),
]


# ------------------------------------------------------------------------------------------------


def inserta_usuarios(borrar_actuales=False):
    """
    """
    if borrar_actuales:
        Usuario.objects.filter(es_admin=False).delete()

    l_ok = []
    l_nok = []

    for t in l_usuarios:
        try:
            provincia = Provincia.objects.get(codigo=t[5])
            usuario = Usuario(username=t[0].strip(),
                              nombre=t[1].strip(),
                              apellidos=t[2].strip(),
                              email=t[3].strip(),
                              nif=t[4].strip(),
                              provincia=provincia,
                              direccion=t[6].strip(),
                              telefono=t[8].strip(),
                              es_admin=False
                              )
            usuario.save()
            l_ok.append((usuario.nombre, usuario.id,))
        except Exception as e:
            l_nok.append((t, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}


def inserta_matriculas(borrar_actuales=False):
    """
    """
    if borrar_actuales:
        Matricula.objects.all().delete()

    l_ok = []
    l_nok = []

    for t in l_matriculas:
        try:
            usuario = Usuario.objects.get(username=t[1])
            matricula = Matricula(usuario=usuario, codigo=t[0].strip())
            matricula.save()
            l_ok.append((matricula.codigo, matricula.id,))
        except Exception as e:
            l_nok.append((t, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}


def inserta_repostajes(borrar_actuales=False):
    """
    """
    if borrar_actuales:
        Repostaje.objects.all().delete()

    l_ok = []
    l_nok = []

    for t in l_repostajes:
        try:
            # username, codigo matricula, codigo estacion, codigo combustible, albaran, litros
            usuario = Usuario.objects.get(username=t[0])
            matricula = Matricula.objects.get(codigo=t[1])
            estacion = Estacion.objects.get(codigo=t[2])
            combustible = Combustible.objects.get(codigo=t[3])
            precio = PrecioCombustible.objects.get(combustible=combustible, estacion=estacion).precio
            litros = t[5]
            respotaje = Repostaje(usuario=usuario, matricula=matricula, estacion=estacion, combustible=combustible,
                                  albaran=t[4], litros=litros, precio=precio, importe=litros * precio)
            respotaje.save()
            l_ok.append(respotaje.id)
        except Exception as e:
            l_nok.append((t, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}
