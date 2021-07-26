# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from decimal import Decimal

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from fmaestros.models import Estacion, Combustible, PrecioCombustible
from fmaestros.views_utils import nuevoeditar_clase
from repostajes.adatos import obtener_resumen, obtener_factura_mensual
from repostajes.forms import SelecionarTemporada, RepostajeForm
from repostajes.models import Repostaje, Factura
from tgas import menu
from tgas.fcomunes import formatea_fecha
from usuarios.models import Usuario, Matricula


@csrf_exempt
@require_POST
def repostaje_nuevo_rest(request):
    datos = json.loads(request.body.decode('utf-8'))

    codigo_estacion = datos.get('estacion', None)
    nombre_usuario = datos.get('usuario', None)
    codigo_matricula = datos.get('matricula', None)
    litros = Decimal(datos.get('litros', 0))
    codigo_combustible = datos.get('combustible', None)
    albaran = datos.get('albaran', None)
    token = request.META.get('HTTP_AUTHORIZATION', None)

    try:
        estacion = Estacion.objects.get(codigo=codigo_estacion)

        if not estacion.comprobar_token(token):
            return HttpResponseForbidden()

        usuario = Usuario.objects.get(username=nombre_usuario)
        matricula = Matricula.objects.get(codigo=codigo_matricula, usuario_id=usuario.id)
        combustible = Combustible.objects.get(codigo=codigo_combustible)

        precio_combustible = PrecioCombustible.objects.get(combustible_id=combustible.id, estacion_id=estacion.id)

        precio = precio_combustible.precio
        importe = precio * litros

        repostaje = Repostaje(estacion=estacion, usuario=usuario, matricula=matricula, litros=litros,
                              combustible=combustible, albaran=albaran, precio=precio, importe=importe)
        repostaje.save()

        codigo_factura = get_random_string(length=10) + str(repostaje.id)
        factura = Factura(es_mensual=False, usuario=usuario, importe=importe, codigo=codigo_factura.upper())
        factura.save()

    except Exception as ex:
        print ex
        return HttpResponseServerError()

    return HttpResponse()


def repostaje_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Repostaje',
                             idp='repostajes-nuevo',
                             formClass=RepostajeForm,
                             modelClass=Repostaje,
                             pagina_nuevo_dato='backoffice/repostajes/repostajes-nuevo-editar.html')


def repostaje_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Repostaje',
                             idp='repostajes-editar',
                             formClass=RepostajeForm,
                             modelClass=Repostaje,
                             pagina_nuevo_dato='backoffice/repostajes/repostajes-nuevo-editar.html')


def repostaje_listado(request):
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Repostajes'
    parametros['subtitulo_pagina'] = ''
    usuario = Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    if request.method == 'GET':
        now = timezone.now()
        ano = now.year
        mes = now.month
        matricula = None

        if usuario.es_admin:
            formulario = SelecionarTemporada(initial={'ano': ano, 'mes': mes})
        else:
            formulario = SelecionarTemporada(initial={'ano': ano, 'mes': mes}, usuario=usuario)

        parametros['formulario'] = formulario
    else:
        if usuario.es_admin:
            formulario = SelecionarTemporada(request.POST)
        else:
            formulario = SelecionarTemporada(request.POST, usuario=usuario)

        parametros['formulario'] = formulario
        if formulario.is_valid():
            datos_form = formulario.cleaned_data
            ano = datos_form['ano']
            mes = datos_form['mes']
            matricula = datos_form.get('matricula', None)
        else:
            parametros['msg_error'] = u'Temporada no válida'
            return render(request, 'backoffice/pcontable/relacion_gastos_ingresos.html', parametros)

    repostajes = Repostaje.objects.filter(fecha_creacion__year=ano, fecha_creacion__month=mes)

    if not usuario.es_admin:
        repostajes = repostajes.filter(usuario_id=usuario.id)

    if matricula is not None:
        repostajes = repostajes.filter(matricula_id=matricula.id)

    parametros['repostajes'] = repostajes

    return render(request, 'backoffice/repostajes/repostajes-list.html', parametros)


def consumos(request):
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Resumenes de consumo'
    parametros['subtitulo_pagina'] = ''
    usuario = Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)
    parametros['titulo'] = 'total'

    if request.method == 'GET':
        now = timezone.now()
        ano = now.year
        estacion = None
        matricula = None
        combustible = None

        if usuario.es_admin:
            formulario = SelecionarTemporada(initial={'ano': ano})
        else:
            formulario = SelecionarTemporada(initial={'ano': ano}, usuario=usuario)

        parametros['formulario'] = formulario
    else:
        if usuario.es_admin:
            formulario = SelecionarTemporada(request.POST)
        else:
            formulario = SelecionarTemporada(request.POST, usuario=usuario)

        parametros['formulario'] = formulario
        if formulario.is_valid():
            datos_form = formulario.cleaned_data
            ano = datos_form['ano']
            estacion = datos_form.get('estacion', None)
            matricula = datos_form.get('matricula', None)
            combustible = datos_form.get('combustible', None)
        else:
            parametros['msg_error'] = u'Temporada no válida'
            return render(request, 'backoffice/pcontable/relacion_gastos_ingresos.html', parametros)

    query_set = Repostaje.objects.filter(fecha_creacion__year=ano)

    if not usuario.es_admin:
        query_set = query_set.filter(usuario_id=usuario.id)

    if estacion:
        query_set = query_set.filter(estacion_id=estacion.id)

    if matricula:
        query_set = query_set.filter(matricula_id=matricula.id)

    if combustible:
        query_set = query_set.filter(combustible_id=combustible.id)
        parametros['titulo'] = combustible.nombre

    resumen = obtener_resumen(query_set)

    parametros['resumen'] = resumen

    return render(request, 'backoffice/repostajes/consumos.html', parametros)


def facturas_listado(request):
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Facturas'
    parametros['subtitulo_pagina'] = ''
    usuario = Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    if request.method == 'GET':
        now = timezone.now()
        ano = now.year
        mes = now.month

        formulario = SelecionarTemporada(initial={'ano': ano, 'mes': mes})
        parametros['formulario'] = formulario
    else:
        formulario = SelecionarTemporada(request.POST)

        parametros['formulario'] = formulario
        if formulario.is_valid():
            datos_form = formulario.cleaned_data
            ano = datos_form['ano']
            mes = datos_form['mes']
        else:
            parametros['msg_error'] = u'Temporada no válida'
            return render(request, 'backoffice/pcontable/relacion_gastos_ingresos.html', parametros)

    es_mensual = usuario.factura_mensual

    if es_mensual:
        factura = obtener_factura_mensual(usuario=usuario, ano=int(ano), mes=int(mes))

        if not factura:
            parametros['msg_error'] = u'Temporada no válida'
            return render(request, 'backoffice/pcontable/relacion_gastos_ingresos.html', parametros)

        facturas = [factura]
    else:
        facturas = Factura.objects.filter(usuario_id=usuario.id, fecha_creacion__year=ano, fecha_creacion__month=mes,
                                          es_mensual=es_mensual)

    parametros['facturas'] = facturas

    return render(request, 'backoffice/repostajes/facturas-list.html', parametros)


def descargar_factura(request):
    dato_id = int(request.GET.get('dato_id').replace('.', ''))
    factura = Factura.objects.get(id=dato_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=factura-%s.pdf' % factura.codigo

    elements = []

    doc = SimpleDocTemplate(response)

    data = [
        ('Fecha', 'Número', 'Importe'),
        (formatea_fecha(factura.fecha_creacion), factura.codigo,
         '%s€' % str(factura.importe).encode('utf-8').replace('.', ','))
    ]

    table = Table(data, colWidths=150, rowHeights=30)
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    return response
