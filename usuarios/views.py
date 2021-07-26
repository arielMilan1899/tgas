# -*- coding: utf8 -*- 
# Create your views here.
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import tlalogger
from fmaestros.models import Estacion, Combustible
from tgas import menu
from usuarios import models as usuarios_models


# from backoffice import adatos

@login_required
def bienvenido(request):
    """
    Página inicio. 
    Controla tanto la bienvenida una vez registrado (home),
    como si se trata del servidor propio del cliente o nuestra
    web corporativa de Internet. (settings.SERVIDOR_PROPIO)
    Tambien crea o lee ContextoUsuario, que es el que define
    en que empresa_operadora y delegacion va a trabajar, y con
    qué permisos.
    """
    logger = tlalogger.dj_mylogger(__file__)
    logger.info("El usuario %s acaba de acceder al sistema", request.user.username)
    parametros = {}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    usuario = usuarios_models.Usuario.objects.filter(username=request.user.username).last()

    if usuario is None:
        parametros['error_msg'] = 'Usuario "%s" no dado de alta en el sistema' % request.user.username
        return render(request, "publica/login_error.html", parametros)

    parametros['usuario'] = usuario
    parametros['html_notificaciones'] = menu.devuelve_html_notificaciones()
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)
    # parametros['html_breadcrumb'] = menu.devuelve_mapa_web(con_pagina_inicio=True, con_iconos=True)['ppal-config-usuarios_listado']['breadcrumb-html']
    parametros['titulo_pagina'] = 'Bienvenido'

    if not usuario.es_admin:
        estaciones = Estacion.objects.all()
        datos = []

        for estacion in estaciones:
            estacion_datos = {
                'id': estacion.id,
                'nombre': estacion.nombre,
                'direccion': estacion.direccion,
                'geo_latitud': float(estacion.geo_latitud),
                'geo_longitud': float(estacion.geo_longitud),
                'provincia': str(estacion.provincia),
                'precios': [{'combustible': precio.combustible.id, 'precio': str(precio)} for precio in
                            estacion.precios()]
            }

            datos.append(estacion_datos)

        json_datos = json.dumps(datos)

        parametros['datos'] = json_datos
        parametros['combustibles'] = Combustible.objects.all()

    # print('Parametros iniciales: %s' % repr(parametros))
    # print request
    # print request.user
    return render(request, "backoffice/bienvenido.html", parametros)

    # if request.user.is_authenticated():
    #     return redirect('/csalones/incidencias/listar-pendientes/')
    # else:
    #     return redirect('/csalones/login')


def forgotten_password(request):
    """
    """
    parametros = {}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    return render(request, "publica/forgotten_password.html", parametros)
