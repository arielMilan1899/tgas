# -*- coding: utf8 -*-
"""
 Utilidades para construir las vistas de los ficheros maestros.
     listado_clase()
     nuevoeditar_clase()
     borrar_clase()
"""
# Create your views here.
import math
from decimal import Decimal

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from fmaestros.googlemaps import pinta_markers
from fmaestros.models import Provincia, Estacion, Combustible
from usuarios import models as usuarios_models

import uitools
import tlalogger
from tgas import menu
from base64 import b64encode

@login_required
def listado_clase(request, titulo_pagina, idp, formClass, modelClass, pagina_listado, pagina_formulario, listado_no_admin=None):
    """
    Función genérica para listar el contenido de una clase.
    Cada vista específica de cada clase la llama para generar
    la página listado correspondiente.

    :param request: request
    :param titulo_pagina:  str Titulo de la página
    :param idp: str Identificador único de la página (para menu.py y breadcrumb)
    :param formClass: Clase del Formulario inicial de filtrado. None si no se usa.
    :param modelClass:  Calse del modelo
    :param pagina_listado:  str con el path y nombre de la plantilla del listado
    :param pagina_formulario: str con el path y nombre de la plantilla del formulario
      inicial que filtra los resultados. Si formClass=None no se utiliza.
    :return:

    Ejemplo:
    listado_clase(request,
                titulo_pagina='Listado Maquinas',
                idp='ppal-maquinas-listado',
                # formClass=tbdata_forms.FiltroMaquinasForm,
                formClass=None,
                modelClass=tbdata_models.Maquina,
                pagina_listado='backoffice/ppal-maquinas-listado.html',
                # pagina_formulario='backoffice/ppal-maquinas-listado_form.html')
                pagina_formulario=None)
    """

    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = titulo_pagina
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    # #------------------ SOLO ADMIN ----------------
    if not usuario.es_admin:
        if listado_no_admin:
            return listado_no_admin(request, titulo_pagina, idp, formClass, modelClass, pagina_listado, pagina_formulario)
        return render(request, 'backoffice/no_permisos_para_proceso.html', parametros)

    if formClass is not None:
        print "formClass no es None"
        formulario = formClass(request.POST)
        if formulario.is_valid() and request.POST.get('continuar'):
            datos_form = formulario.cleaned_data
            parametros['filtro_form'] = datos_form
            print datos_form
            # Hacer este filtro: --------------
            print datos_form['provincia']
            parametros['l_datos'] = modelClass.objects.filter(provincia=datos_form['provincia'])
            # Hacer este filtro: --------------///////////
            parametros['formulario'] = formulario

            return render(request, pagina_listado, parametros)
        else:
            parametros['formulario'] = formulario

        return render(request, pagina_formulario, parametros)
    else:
        parametros['l_datos'] = modelClass.objects.all()

        return render(request, pagina_listado, parametros)

@login_required()
def borrar_clase(request, titulo_pagina, titulo_clase, idp, modelClass, pagina_html, path_cancelar, success_url):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = titulo_pagina
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    #------------------ SOLO ADMIN ----------------
    if not usuario.es_admin:
        return render(request, 'backoffice/no_permisos_para_proceso.html', parametros)

    if request.POST.get('cancelar'):
        vengo_desde = request.POST.get('vengo_desde')
        # Por alguna extraña razón devuelve 'None' en vez de None
        if str(vengo_desde) != u'None':
            path_cancelar = vengo_desde
        return redirect(path_cancelar)

    if request.POST.get('borrado_finalizado'):
        return redirect(success_url)

    if request.method == 'GET':
        try:
            dato_id = int(request.GET.get('dato_id').replace('.',''))
        except:
            dato_id = None
    else:
        try:
            dato_id = int(request.POST.get('dato_id').replace('.',''))
        except:
            dato_id = None
    parametros['dato_id'] = dato_id
    dato_leido = modelClass.objects.get(id=dato_id)
    parametros['dato'] = dato_leido

    print dato_leido

    if request.POST.get('confirmar_borrado'):
        dato_leido.delete()
        parametros['ya_eliminado'] = 'SI'


    return render(request, pagina_html, parametros)


@login_required()
def nuevoeditar_clase(request, es_nuevo, titulo_pagina, idp, formClass, modelClass, pagina_nuevo_dato):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = titulo_pagina
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    #------------------ SOLO ADMIN ----------------
    if not usuario.es_admin:
        return render(request, 'backoffice/no_permisos_para_proceso.html', parametros)

    parametros['barra_botones'] = uitools.barra_botones('visualizar', request)
    # ------------ Vamos a editar un valor de la BD ---------------------------
    if request.method == 'GET':
        print "-------> GET"

        try:
            dato_id = int(request.GET.get('dato_id').replace('.',''))
        except:
            dato_id = None
        print type(dato_id), dato_id
        parametros['dato_id'] = dato_id
        if dato_id is not None:
            dato_leido = modelClass.objects.get(id=dato_id)
            formulario = formClass(es_nuevo=es_nuevo, instance=dato_leido)
            # Convierte todos los campos a solo-lectura
            for campo in sorted(formulario.fields.keys()):
                formulario.fields[campo].widget.attrs['disabled'] = True
            parametros['modo_sololectura'] = 'SI'
            # Para descargar las facturas en PDF en id va encriptado
            if (modelClass.__name__ == 'Factura'):
                parametros['dato_id_enc'] = dato_leido.id2cod()
        else: #---- Datos nuevos, no estamos editando un valor de la BD ---------
            formulario = formClass(es_nuevo=es_nuevo)
            parametros['barra_botones'] = uitools.barra_botones('nuevo', request)
    else:
        print "-------> POST"
        try:
            dato_id = int(request.POST.get('dato_id').replace('.',''))
        except:
            dato_id = None
        parametros['dato_id'] = dato_id
        print type(dato_id), dato_id
        if request.POST.get('nuevo'): #---- Datos nuevos, no estamos editando un valor de la BD ---------
            print "--- Botón NUEVO "
            formulario = formClass(es_nuevo=es_nuevo)
            parametros['barra_botones'] = uitools.barra_botones('editar', request)
        elif request.POST.get('editar'):
            dato_leido = modelClass.objects.get(id=dato_id)
            formulario = formClass(es_nuevo=es_nuevo, instance=dato_leido)
            parametros['barra_botones'] = uitools.barra_botones('editar', request)
        elif dato_id:
            dato_leido = modelClass.objects.get(id=dato_id)
            formulario = formClass(request.POST, es_nuevo=es_nuevo, instance=dato_leido)
            parametros['barra_botones'] = uitools.barra_botones('editar', request)
        else: #---- Datos nuevos, no estamos editando un valor de la BD ---------
            formulario = formClass(request.POST, es_nuevo=es_nuevo)
            parametros['barra_botones'] = uitools.barra_botones('nuevo', request)

    # No existe formulario.cleaned_data hasta que se ha llamado a is_valid()
    form_is_valid = formulario.is_valid()
    try:
        datos_form = formulario.cleaned_data
    except:
        datos_form = None
    parametros['filtro_form'] = datos_form
    parametros['formulario'] = formulario

    if form_is_valid and request.POST.get('continuar'):
        print "continuar"
        parametros['datos_comprobados'] = 'SI'
        parametros['barra_botones'] = uitools.barra_botones('editar', request)
    elif form_is_valid and request.POST.get('grabar_recalcular'):
        print "grabar_recalcular", dato_id
        # print datos_form
        # Si el dato estaba guardo en la BD: actualizamos.
        try:
            nuevo_dato = modelClass.objects.get(id=dato_id)
        except:
            nuevo_dato = modelClass()

        for atributo,valor in datos_form.items():
            nuevo_dato.__setattr__(atributo,valor)
        # Caso especial de las Factura cargada en un PDF
        if request.FILES.has_key('fichero_pdf'):
            print "\n\n -----> Cargando un nuevo fichero PDF \n\n"
            f_in_pdf = request.FILES['fichero_pdf']
            nuevo_dato.rawPDFb64 = b64encode(f_in_pdf.read())
        # /
        nuevo_dato = formulario.save()
        parametros['dato_id'] = nuevo_dato.id
        parametros['grabado_recalculado'] = 'SI'
        # Convierte todos los campos a solo-lectura
        for campo in sorted(formulario.fields.keys()):
            formulario.fields[campo].widget.attrs['disabled'] = True
        parametros['modo_sololectura'] = 'SI'
        # Para descargar las facturas en PDF en id va encriptado
        if (modelClass.__name__ == 'Factura'):
            parametros['dato_id_enc'] = nuevo_dato.id2cod()
        parametros['barra_botones'] = uitools.barra_botones('visualizar', request)
        parametros['formulario'] = formulario
    else:
        print "Else (Formulario no valido)"

    # print "=="*40, request
    print "-"*40, type(formClass), type(modelClass)
    import pprint; pprint.pprint(parametros)


    return render(request, pagina_nuevo_dato, parametros)



@login_required()
def editar1solodato_clase(request, titulo_pagina, idp, formClass, modelClass, pagina_nuevo_dato):
    """
    Lógica para una vista genérica que permita editar datos en la BD cuando sólo
    hay un único dato. Por ejemplo configuraciones.

    :param request:
    :param titulo_pagina:
    :param idp:
    :param formClass:
    :param modelClass:
    :param pagina_nuevo_dato:
    :return:
    """
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO

    parametros['titulo_pagina'] = titulo_pagina
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    #------------------ SOLO ADMIN ----------------
    if not usuario.es_admin:
        return render(request, 'backoffice/no_permisos_para_proceso.html', parametros)

    parametros['barra_botones'] = uitools.barra_botones('visualizar1solodato', request)
    # ------------ Vamos a editar un valor de la BD ---------------------------
    if request.method == 'GET':
        print "-------> GET"
        try:
            dato_leido = modelClass.objects.get(id=1)
            dato_id = 1
        except:
            dato_id = None
        parametros['dato_id'] = dato_id
        if dato_id is not None:
            dato_leido = modelClass.objects.get(id=dato_id)
            formulario = formClass(instance=dato_leido)
            # Convierte todos los campos a solo-lectura
            for campo in sorted(formulario.fields.keys()):
                formulario.fields[campo].widget.attrs['disabled'] = True
            parametros['modo_sololectura'] = 'SI'
        else: #---- Datos nuevos, no estamos editando un valor de la BD ---------
            formulario = formClass()
            parametros['barra_botones'] = uitools.barra_botones('nuevo', request)
    else:
        print "-------> POST"
        try:
            dato_id = int(request.POST.get('dato_id'))
        except:
            dato_id = None
        parametros['dato_id'] = dato_id
        print type(dato_id), dato_id
        if request.POST.get('nuevo'): #---- Datos nuevos, no estamos editando un valor de la BD ---------
            print "--- Botón NUEVO "
            formulario = formClass()
            parametros['barra_botones'] = uitools.barra_botones('editar1solodato', request)
        elif request.POST.get('editar'):
            dato_leido = modelClass.objects.get(id=dato_id)
            formulario = formClass(instance=dato_leido)
            parametros['barra_botones'] = uitools.barra_botones('editar1solodato', request)
        else: #---- Datos nuevos, no estamos editando un valor de la BD ---------
            formulario = formClass(request.POST)
            parametros['barra_botones'] = uitools.barra_botones('nuevo', request)

    # No existe formulario.cleaned_data hasta que se ha llamado a is_valid()
    form_is_valid = formulario.is_valid()
    try:
        datos_form = formulario.cleaned_data
    except:
        datos_form = None
    parametros['filtro_form'] = datos_form
    parametros['formulario'] = formulario

    if form_is_valid and request.POST.get('continuar'):
        print "continuar"
        parametros['datos_comprobados'] = 'SI'
        parametros['barra_botones'] = uitools.barra_botones('editar1solodato', request)
    elif form_is_valid and request.POST.get('grabar_recalcular'):
        print "grabar_recalcular", dato_id
        print datos_form
        # Si el dato estaba guardo en la BD: actualizamos.
        try:
            nuevo_dato = modelClass.objects.get(id=dato_id)
        except:
            nuevo_dato = modelClass()

        for atributo,valor in datos_form.items():
            nuevo_dato.__setattr__(atributo,valor)
        nuevo_dato.save()
        parametros['dato_id'] = nuevo_dato.id
        parametros['grabado_recalculado'] = 'SI'
        # Convierte todos los campos a solo-lectura
        for campo in sorted(formulario.fields.keys()):
            formulario.fields[campo].widget.attrs['disabled'] = True
        parametros['modo_sololectura'] = 'SI'
        parametros['barra_botones'] = uitools.barra_botones('visualizar1solodato', request)
        parametros['formulario'] = formulario
    else:
        print "Else (Formulario no valido)"

    print "=="*40, request
    print "-"*40, type(formClass), type(modelClass)
    import pprint; pprint.pprint(parametros)


    return render(request, pagina_nuevo_dato, parametros)

@login_required
def ver_mapa(request):
    """
    """
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Ver estaciones'
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    center_coords = None

    try:
        dato_id = request.GET.get('dato_id').replace('.', '')
        estacion = Estacion.objects.get(id=dato_id)
        center_coords = "[%s, %s]" % (estacion.geo_latitud, estacion.geo_longitud)
        zoom = 16
    except:
        zoom = 8

    estaciones = Estacion.objects.all()

    l_posiciones = [{
        'pos': (estacion.geo_latitud, estacion.geo_longitud),
        'icon': 'verde',
        'title': estacion.nombre
    } for estacion in estaciones]

    try:
        parametros['html_gmap3'] = pinta_markers(l_posiciones, zoom=zoom, center_coords=center_coords)
    except:
        parametros['html_gmap3'] = '<h4>No se han encontrado datos de coordenadas GPS</h4>'

    return render(request, 'backoffice/fmaestros/estaciones-mapa.html', parametros)

@login_required
def listado_estaciones_no_admin(request, titulo_pagina, idp, formClass, modelClass, pagina_listado, pagina_formulario):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = titulo_pagina
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    if formClass is not None:
        print "formClass no es None"
        formulario = formClass(request.POST)
        if formulario.is_valid() and request.POST.get('continuar'):
            datos_form = formulario.cleaned_data
            parametros['filtro_form'] = datos_form
            print datos_form
            # Hacer este filtro: --------------
            print datos_form['provincia']
            parametros['l_datos'] = modelClass.objects.filter(provincia=datos_form['provincia'])
            # Hacer este filtro: --------------///////////
            parametros['formulario'] = formulario

            return render(request, pagina_listado, parametros)
        else:
            parametros['formulario'] = formulario

        return render(request, pagina_formulario, parametros)
    else:
        parametros['l_datos'] = Estacion.objects.all()

        return render(request, pagina_listado, parametros)

