# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import tlalogger

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.db.models import Max

from django.http import HttpResponse

import datetime
from usuarios import models as usuarios_models
from tgas import menu, fcomunes
from pcontable import adatos
from fmaestros.models import Cuenta

from forms import SelecTemporada

import decimal


# Create your views here.

@login_required
def relacion_gastos_ingresos(request):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Relación de Gastos e Ingresos Mensual'
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)
    # # ------------------ SOLO ADMIN ----------------
    # if not usuario.es_admin:
    #     return render(request, 'backoffice/no_permisos_para_proceso.html', parametros)

    if request.method == 'GET':
        temporada = "2019-2020"
        parametros['formulario'] = SelecTemporada(initial={'temporada': temporada})
    else:
        formulario = SelecTemporada(request.POST)
        parametros['formulario'] = formulario
        if formulario.is_valid() and request.POST.get('aplicar_filtros'):
            datos_form = formulario.cleaned_data
            temporada = datos_form['temporada']
        else:
            parametros['msg_error'] = u'Temporada no válida'
            return render(request, 'backoffice/pcontable/relacion_gastos_ingresos.html', parametros)

    # Detalle Mensual de Gastos e Ingresos  (dict de 12 meses y total)
    d_fechas = adatos.devuelve_d_fechas(temporada)
    desde = d_fechas[7][0]
    hasta = d_fechas[6][1]
    parametros['a0'] = desde.year #'2019'
    parametros['a1'] = hasta.year #'2020'

    parametros['d_det_mens'] = adatos.detalle_mensual_gastos_ingresos(temporada)

    # Resumen de Gastos e Ingresos  (dict de n-elementos por codigo y total)
    parametros['d_tot_por_cuenta'] = adatos.total_anual_gastos_ingresos_por_cuenta(temporada)

    # Detalle por cada tipo de Cuenta (lista con un dict por cuenta)
    parametros['l_det_mens_por_cuenta'] = adatos.detalle_mensual_gastos_ingresos_por_cuenta(temporada)


    return render(request, 'backoffice/pcontable/relacion_gastos_ingresos.html', parametros)

