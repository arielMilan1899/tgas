# -*- coding: utf8 -*-
import json
from decimal import Decimal

from django.db.transaction import atomic
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from tgas import fcomunes, menu
import models
import forms
from views_utils import listado_clase, nuevoeditar_clase, borrar_clase, ver_mapa, listado_estaciones_no_admin
from usuarios.models import Usuario
from usuarios.forms import UsuarioForm
from tgas.base36crypt import genera_password

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuarios import models as usuarios_models
import tlalogger


# --------------  Usuarios --------------------------------------------------------
def usuarios_listado(request):
    return listado_clase(request,
                         titulo_pagina='Listado de Usuarios',
                         idp='fich-usuarios-list',
                         formClass=None,
                         modelClass=Usuario,
                         pagina_listado='backoffice/fmaestros/fich-usuarios-list.html',
                         pagina_formulario=None)


def usuarios_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Usuario',
                             idp='fich-usuarios-nuevo',
                             formClass=UsuarioForm,
                             modelClass=Usuario,
                             pagina_nuevo_dato='backoffice/fmaestros/usuario_nuevoeditar.html')


def usuarios_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Usuario',
                             idp='fich-usuarios-editar',
                             formClass=UsuarioForm,
                             modelClass=Usuario,
                             pagina_nuevo_dato='backoffice/fmaestros/usuario_nuevoeditar.html')


def usuarios_mis_datos(request):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Mis datos'
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    if request.POST.get('salvar'):
        formulario = UsuarioForm(request.POST, es_nuevo=False, instance=usuario)
    else:
        formulario = UsuarioForm(es_nuevo=False, instance=usuario)

    formulario.fields['username'].disabled = True
    formulario.fields['nif'].disabled = True

    # No existe formulario.cleaned_data hasta que se ha llamado a is_valid()
    form_is_valid = formulario.is_valid()
    try:
        datos_form = formulario.cleaned_data
    except:
        datos_form = None
    parametros['filtro_form'] = datos_form
    parametros['formulario'] = formulario

    if form_is_valid and request.POST.get('salvar'):
        for atributo, valor in datos_form.items():
            usuario.__setattr__(atributo, valor)

        usuario.esta_activo = True
        formulario.save()
        #Para mostrar toda la data nueva en caso de que el form haya sido guardado
        formulario = UsuarioForm(es_nuevo=False, instance=usuario)
        parametros['formulario'] = formulario

    else:
        print "Else (Formulario no valido)"

    return render(request, 'backoffice/fmaestros/usuario_mis_datos.html', parametros)


def usuarios_borrar(request):
    return borrar_clase(request,
                        titulo_pagina='Borrar Usuario',
                        titulo_clase='Titulares',
                        idp='fich-usuarios-borrar',
                        modelClass=Usuario,
                        pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                        path_cancelar='/usuarios/list/',
                        success_url='/usuarios/list/')


def usuarios_imprimir(request):
    return None


@login_required
def usuarios_reestablece_password(request):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Reestrablecer Password Usuario'
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    user_id = request.GET.get('user_id').replace('.', '')

    # ------------------ SOLO ADMIN ----------------
    if not usuario.es_admin:
        return render(request, 'backoffice/no_permisos_para_proceso.html', parametros)

    usuario_a_modif = Usuario.objects.filter(id=user_id).last()
    if usuario_a_modif:
        password = genera_password(usuario_a_modif.username)
        usuario_a_modif.password = password
        usuario_a_modif.save()

        parametros['usuario_a_modif'] = usuario_a_modif
        parametros['password'] = password

    else:
        parametros['msg_error'] = u'Usuario no encontrado. No es posible reestablecer el password.'

    return render(request, 'backoffice/fmaestros/usuario_cambiapassword.html', parametros)


# --------------  Empresas --------------------------------------------------------
def empresas_listado(request):
    return listado_clase(request,
                         titulo_pagina='Listado Empresas',
                         idp='fich-empresas-list',
                         formClass=None,
                         modelClass=models.Empresa,
                         pagina_listado='backoffice/fmaestros/fich-empresas-list.html',
                         pagina_formulario=None)


def empresas_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Empresa',
                             idp='fich-empresas-nuevo',
                             formClass=forms.EmpresaForm,
                             modelClass=models.Empresa,
                             pagina_nuevo_dato='backoffice/fmaestros/empresas-nuevo-editar.html')


def empresas_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Empresa',
                             idp='fich-empresas-editar',
                             formClass=forms.EmpresaForm,
                             modelClass=models.Empresa,
                             pagina_nuevo_dato='backoffice/fmaestros/empresas-nuevo-editar.html')


def empresas_borrar(request):
    return borrar_clase(request,
                        titulo_pagina='Borrar Empresa',
                        titulo_clase='Empresa',
                        idp='fich-empresas-borrar',
                        modelClass=models.Empresa,
                        pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                        path_cancelar='/empresas/list/',
                        success_url='/empresas/list/')


def empresas_imprimir(request):
    return None


# --------------  Tipos de Cuentas --------------------------------------------------------
def cuentas_listado(request):
    return listado_clase(request,
                         titulo_pagina='Listado Tipos de Cuentas',
                         idp='fich-cuentas-list',
                         formClass=None,
                         modelClass=models.Cuenta,
                         pagina_listado='backoffice/fmaestros/fich-cuentas-list.html',
                         pagina_formulario=None)


def cuentas_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Tipo de Cuenta',
                             idp='fich-cuentas-nuevo',
                             formClass=forms.CuentaForm,
                             modelClass=models.Cuenta,
                             pagina_nuevo_dato='backoffice/fmaestros/cuentas-nuevo-editar.html')


def cuentas_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Tipo de Cuenta',
                             idp='fich-cuentas-editar',
                             formClass=forms.CuentaForm,
                             modelClass=models.Cuenta,
                             pagina_nuevo_dato='backoffice/fmaestros/cuentas-nuevo-editar.html')


def cuentas_borrar(request):
    return borrar_clase(request,
                        titulo_pagina='Borrar Tipo de Cuenta',
                        titulo_clase='Empresa',
                        idp='fich-cuentas-borrar',
                        modelClass=models.Cuenta,
                        pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                        path_cancelar='/cuentas/list/',
                        success_url='/cuentas/list/')


def cuentas_imprimir(request):
    return None


# --------------  Apuntes contables --------------------------------------------------------
def apuntes_listado(request):
    return listado_clase(request,
                         titulo_pagina='Listado Apuntes Contables',
                         idp='fich-apuntes-list',
                         formClass=None,
                         modelClass=models.Apunte,
                         pagina_listado='backoffice/fmaestros/apuntes-listado.html',
                         pagina_formulario=None)


def apuntes_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Apunte Contable',
                             idp='fich-apuntes-nuevo',
                             formClass=forms.ApunteForm,
                             modelClass=models.Apunte,
                             pagina_nuevo_dato='backoffice/fmaestros/apuntes-nuevo-editar.html')


def apuntes_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Apunte Contable',
                             idp='fich-apuntes-editar',
                             formClass=forms.ApunteForm,
                             modelClass=models.Apunte,
                             pagina_nuevo_dato='backoffice/fmaestros/apuntes-nuevo-editar.html')


def apuntes_borrar(request):
    return borrar_clase(request,
                        titulo_pagina='Borrar Apunte Contable',
                        titulo_clase='Apunte Contable',
                        idp='fich-apuntes-borrar',
                        modelClass=models.Apunte,
                        pagina_html='backoffice/fmaestros/apuntes-borrar.html',
                        path_cancelar='/apuntes/list/',
                        success_url='/apuntes/list/')


def apuntes_imprimir(request):
    return None


# _____________ INI Código añadido por crea_prototipo_fmaestros.py


def provincia_listado(request):
    return listado_clase(request,
                         titulo_pagina='Listado Provincias',
                         idp='provincia-list',
                         formClass=None,
                         modelClass=models.Provincia,
                         pagina_listado='backoffice/fmaestros/provincia-list.html',
                         pagina_formulario=None)


def provincia_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Provincia',
                             idp='provincia-nuevo',
                             formClass=forms.ProvinciaForm,
                             modelClass=models.Provincia,
                             pagina_nuevo_dato='backoffice/fmaestros/provincia-nuevo-editar.html')
    # pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')


def provincia_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Provincia',
                             idp='provincia-editar',
                             formClass=forms.ProvinciaForm,
                             modelClass=models.Provincia,
                             pagina_nuevo_dato='backoffice/fmaestros/provincia-nuevo-editar.html')
    # pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')


def provincia_borrar(request):
    return borrar_clase(request,
                        titulo_pagina='Borrar Provincia',
                        titulo_clase='Provincia',
                        idp='provincia-borrar',
                        modelClass=models.Provincia,
                        pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                        path_cancelar='/provincia/list/',
                        success_url='/provincia/list/')


def provincia_imprimir(request):
    return None


# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

# _____________ INI Código añadido por crea_prototipo_fmaestros.py


def estaciones_listado(request):
    titulo_pagina = 'Listado Estaciones'
    pagina_listado = 'backoffice/fmaestros/estaciones-list.html'
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = titulo_pagina
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    # #------------------ SOLO ADMIN ----------------
    if not usuario.es_admin:
        return listado_estaciones_no_admin(request, titulo_pagina, None, None, models.Estacion, pagina_listado, None)

    parametros['l_datos'] = models.Estacion.objects.all()

    return render(request, pagina_listado, parametros)


def estaciones_nuevo(request):
    return nuevoeditar_clase(request,
                             es_nuevo=True,
                             titulo_pagina='Nuevo Estación',
                             idp='estaciones-nuevo',
                             formClass=forms.EstacionForm,
                             modelClass=models.Estacion,
                             pagina_nuevo_dato='backoffice/fmaestros/estaciones-nuevo-editar.html')
    # pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')


def estaciones_editar(request):
    return nuevoeditar_clase(request,
                             es_nuevo=False,
                             titulo_pagina='Editar Estación',
                             idp='estaciones-editar',
                             formClass=forms.EstacionForm,
                             modelClass=models.Estacion,
                             pagina_nuevo_dato='backoffice/fmaestros/estaciones-nuevo-editar.html')
    # pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')


def estaciones_borrar(request):
    return borrar_clase(request,
                        titulo_pagina='Borrar Estación',
                        titulo_clase='Estación',
                        idp='estaciones-borrar',
                        modelClass=models.Estacion,
                        pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                        path_cancelar='/estaciones/list/',
                        success_url='/estaciones/list/')


def estaciones_imprimir(request):
    return None


def estaiciones_ver(request):
    logger = tlalogger.dj_mylogger(__file__)
    parametros = {'vengo_desde': request.META.get('HTTP_REFERER')}
    # parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    parametros['titulo_pagina'] = 'Ver estación'
    parametros['subtitulo_pagina'] = ''
    usuario = usuarios_models.Usuario.objects.get(username=request.user.username)
    parametros['usuario'] = usuario
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)

    dato_id = request.GET.get('dato_id')
    parametros['estacion'] = models.Estacion.objects.get(id=dato_id)

    return render(request, 'backoffice/fmaestros/estaciones-ver.html', parametros)


def estaiciones_ver_mapa(request):
    return ver_mapa(request)


@csrf_exempt
@require_POST
def estaciones_nuevos_precios_combustibles(request):
    username = request.META.get('HTTP_USERNAME', None)
    password = request.META.get('HTTP_PASSWORD', None)

    try:
        usuario = Usuario.objects.get(username=username)

        if not (usuario.dj_user.check_password(password) and usuario.es_admin):
            raise Exception()

    except:
        return HttpResponseForbidden()

    datos = json.loads(request.body.decode('utf-8'))

    print datos

    with atomic():
        for dato in datos:
            codigo_estacion = dato.get('estacion', None)
            codigo_combustible = dato.get('combustible', None)
            precio = dato.get('precio', None)

            try:
                estacion = models.Estacion.objects.get(codigo=codigo_estacion)
                combustible = models.Combustible.objects.get(codigo=codigo_combustible)
                models.PrecioCombustible.objects.update_or_create(combustible_id=combustible.id,
                                                                  estacion_id=estacion.id,
                                                                  defaults={'precio': Decimal(precio)})
            except Exception as ex:
                print ex
                return HttpResponseServerError()

    return HttpResponse()
# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

# _____________ INI Código añadido por crea_prototipo_fmaestros.py
 
    
def combustibles_listado(request):
    return listado_clase(request,
                titulo_pagina='Listado Combustibles',
                idp='combustibles-list',
                formClass=None,
                modelClass=models.Combustible,
                pagina_listado='backoffice/fmaestros/combustibles-list.html',
                pagina_formulario=None)

def combustibles_nuevo(request):
    return nuevoeditar_clase(request,
                 es_nuevo=True,
                 titulo_pagina='Nuevo Combustible',
                 idp='combustibles-nuevo',
                 formClass=forms.CombustibleForm,
                 modelClass=models.Combustible,
                 pagina_nuevo_dato='backoffice/fmaestros/combustibles-nuevo-editar.html')
                 # pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')

def combustibles_editar(request):
    return nuevoeditar_clase(request,
                 es_nuevo=False,
                 titulo_pagina='Editar Combustible',
                 idp='combustibles-editar',
                 formClass=forms.CombustibleForm,
                 modelClass=models.Combustible,
                 pagina_nuevo_dato='backoffice/fmaestros/combustibles-nuevo-editar.html')
                 # pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')

def combustibles_borrar(request):
    return borrar_clase(request,
                titulo_pagina='Borrar Combustible',
                titulo_clase='Combustible',
                idp='combustibles-borrar',
                modelClass=models.Combustible,
                pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                path_cancelar='/combustibles/list/',
                success_url='/combustibles/list/')

def combustibles_imprimir(request):
    return None
    
    
# _______________ FIN Código añadido por crea_prototipo_fmaestros.py
 