#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
  Script que recorre todos los directorios buscando ficheros de migrations.
  Y los borra. No borra los __init__.py
  Por ejemplo: ./facturas/migrations/0*.py, ./fmaestros/migrations/0*.py ...

"""
import os
nombre_proyecto = os.path.split(os.getcwd())[-1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", nombre_proyecto+".settings")

from django.conf import settings

def devuelve_lista_migrations():
    """
    Busca todos los ficheros .py correspondientes a las migraciones:
    Empiezan por 0 y terminan en .py: 0001_initial.py, 0002_auto_20180531_1934.py, ...
    :return:
    """
    l_fichs = [os.path.join(basedir, f) for basedir, dirs, fichs in os.walk(settings.BASE_DIR) \
                    for f in fichs if (f.startswith('0') and f.endswith('.py'))]

    return sorted(l_fichs)

def borra_lista_ficheros(l_fichs):
    """
    Borra los ficheros enviados en una lista.
    :param l_fichs:
    :return: {'l_ok': l_ok, 'l_err': l_err}
    """

    l_ok = []
    l_err = []

    for f in l_fichs:
        try:
            os.remove(f)
            l_ok.append(f)
        except Exception as e:
            l_err.append((f,e,))
    return {'l_ok': l_ok, 'l_err': l_err}


if __name__ == '__main__':
    l_fich = devuelve_lista_migrations()
    print("Borrando %s ficheros ..." % len(l_fich))
    r = borra_lista_ficheros(l_fich)
    if len(r['l_err']) > 0:
        print("Error borrando: %s" % str(r['l_err']))
    else:
        print("OK. Ficheros borrados")


