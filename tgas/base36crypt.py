# -*- coding: utf-8 -*-
"""
Created on 2002. Modified on 2018.
@author: jrocamonde


2021: Version descafeinada para formación.

"""

import hashlib


def genera_password(cadena_str):
    """
    Genera un password basado
    2021: Version descafeinada para formación.
    :param cadena_str:
    :return: <str>
    """

    return hashlib.md5(cadena_str).hexdigest()[0:8]



