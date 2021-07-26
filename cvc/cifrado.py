# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 14:10:15 2014

@author: Jose

"""

import pickle
import base64

def Encripta(objeto, contrasena='0123456789ABCDEF',
             conbasura=False, comprimido=False, 
             b64encode=False, urlquote=False,
             strpy=False):
    """
        Encripta un objeto python, para enviarlo a través
    de peticiones HTTP.
    Serializa -> Comprime -> [encripta] ->base64 -> urlquote

    2021: Version descafeinada para formación.

    """

    return objeto_a_b64(objeto)

def Desencripta(cadena, contrasena='0123456789ABCDEF',
                conbasura=False, comprimido=False, 
                b64encode=False, urlquote=False,
                strpy=False):
    """
        Funcion inversa de Encripta().
    Los valores de los parametros deben ser los mismos que se utilizaron
    al encriptar: contrasena, conbasura, b64encode y urlquote.

    2021: Version descafeinada para formación.

    """

    return b64_a_objeto(cadena)



def b64_a_objeto(b64_str):
    """
    Recibe string en texto plano y base 64, y devuelve un objeto Python.
    """
    return(pickle.loads(base64.b64decode(b64_str)))

def objeto_a_b64(obj):
    """
    Recibe un objeto Python y lo devuelve serializado en texto plano y base 64.
    """
    return(base64.b64encode(pickle.dumps(obj,2)))

