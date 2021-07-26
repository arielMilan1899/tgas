# -*- coding: utf-8 -*-
"""

    root@superkol:/home/desarrollo/telemap/tgas# ./manage.py shell

    In [1]: from docs import inserta_iniciales
    In [2]: inserta_iniciales.inserta_iniciales()

"""
from docs.inserta_estaciones import inserta_precios, inserta_comb, inserta_est
from docs.inserta_provincias import inserta_prov, inserta_ccaa
from docs.inserta_usuarios import inserta_repostajes, inserta_usuarios, inserta_matriculas


def inserta_iniciales(borrar_actuales=False):
    """
    """

    l_ok = []
    l_nok = []

    try:
        inserta_ccaa(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_ccaa')
        inserta_prov(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_prov')
        inserta_est(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_est')
        inserta_comb(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_comb')
        inserta_precios(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_precios')
        inserta_usuarios(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_usuarios')
        inserta_matriculas(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_matriculas')
        inserta_repostajes(borrar_actuales=borrar_actuales)
        l_ok.append('inserta_repostajes')
    except Exception as e:
        l_nok.append(e)

    return {'l_nok': l_nok, 'l_ok': l_ok}
