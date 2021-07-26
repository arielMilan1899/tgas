# -*- coding: utf8 -*-
import urlparse

from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.conf import settings

import time, datetime

from usuarios.models import Usuario, LogAcceso, IPPermitida

import tlalogger

from django.conf import settings

from tgas import menu

@csrf_protect
@never_cache
def my_login(request, redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """
    Displays the login form and handles the login action.
    """
    logger = tlalogger.dj_mylogger(__file__)
    logger.debug('Formulario de Login mostrado')
    
    #redirect_to = request.REQUEST.get(redirect_field_name, '')
    redirect_to = request.POST.get(redirect_field_name, '')
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            login_log(request.POST.get('username'),request.META['REMOTE_ADDR'],True)
            
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL
            # No permitir el login desde ips no permitidas:
            if settings.RESTRINGIR_LOGIN_POR_IP:
                l_ips_permitidas = list(IPPermitida.objects.all().values_list('ip', flat=True))
                print l_ips_permitidas
                if request.META['REMOTE_ADDR'] not in l_ips_permitidas:
                    login_log(request.POST.get('username'), request.META['REMOTE_ADDR'],
                              correcto = True,
                              comentario = 'IP no permitida')
                    parametros={'error_msg': "Error 550. No permitido"}
                    return render(request, 'publica/login_error.html', parametros)

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())


            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
        # Por jose (24/09/2012). Esto registra los intentos fallidos
        else:
            login_log(request.POST.get('username'),request.META['REMOTE_ADDR'],False)
        # /jose.
            
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    #current_site = get_current_site(request)
    current_site=''

    parametros = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': '',#current_site,
        'site_name': '',#current_site.name,
        'servidor_propio' : settings.SERVIDOR_PROPIO,
    }
    # 
    return render(request, 'publica/login.html', parametros)
    # return render(request, 'publica/login.html', parametros)

@login_required
def my_logout(request):
    """
    """
    parametros={}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO

    if request.user.is_authenticated():
        auth_logout(request)
        
        return render(request, 'publica/logout.html', parametros)
    else:
        
        return render(request, "publica/no_identificado.html", parametros)
        

def login_log(username,ip_acceso,correcto, comentario = None):
    """
    Registra en la BD los accesos, correcto e incorrectos.
    """
  
    logger = tlalogger.dj_mylogger(__file__)
  
    ahora=datetime.datetime.now()
    log=LogAcceso()
    log.fecha_hora=ahora
    log.username=username
    log.ip=ip_acceso
    log.correcto=correcto
    log.comentario = comentario
    log.save()
    
    l_trab = Usuario.objects.filter(username=username)
    logger.debug('Resultado de Usuario.objects.filter(username="%s"): %s',username, repr(l_trab))
    if l_trab:
        trab=l_trab[0]
#        Actualizo datos
        if correcto:
            trab.ultimo_acceso_correcto = ahora
            trab.accesos_correctos += 1
            logger.debug('Acceso correcto. Nuevo valor de accesos_correctos: %s', trab.accesos_correctos)
        else:
            trab.ultimo_acceso_incorrecto = ahora
            trab.accesos_incorrectos += 1
            logger.debug('ERROR: Acceso incorrecto. Nuevo valor de accesos_incorrectos: %s', trab.accesos_incorrectos)
        trab.save()
#    logger.debug('El username "%s" existe en Usuarios?: %s',username, trab_encontrado)
        


class PasswordForm(forms.Form):
    password1 = forms.CharField(label=_(u"Contraseña nueva"),max_length=20,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_(u"Repita contraseña nueva"),max_length=20,
                                widget=forms.PasswordInput)

@login_required
def Change_Password(request):
    """
    Permite cambiar el password a un usuario.
    """
    parametros={}
    parametros['servidor_propio'] = settings.SERVIDOR_PROPIO
    usuario = Usuario.objects.filter(username=request.user.username)[0]
    parametros['usuario'] = usuario
    parametros['html_notificaciones'] = menu.devuelve_html_notificaciones()
    parametros['html_menu_izquierdo'] = menu.devuelve_html_menu_izquierdo_por_usuario(usuario)
    # parametros['html_breadcrumb'] = menu.devuelve_mapa_web(con_pagina_inicio=True, con_iconos=True)['ppal-config-usuarios_listado']['breadcrumb-html']
    parametros['titulo_pagina'] = 'Cambiar contraseña'
    parametros['subtitulo_pagina'] = "%s" % parametros['usuario'].nombre

    pForm = PasswordForm()
    parametros['pForm'] = pForm

    if request.method == 'POST':
        if request.POST['submit'] == 'Cambiar':
            postDict = request.POST.copy()
            pForm = PasswordForm(postDict)
            if pForm.is_valid():
                uPass1 = request.POST['password1']
                uPass2 = request.POST['password2']
                if (uPass1 == '') or (uPass2 == ''):
                    parametros['error_message'] = 'ERROR: No se permiten contraseñas en blanco.'
                elif uPass1 == uPass2:
                    user = request.user
                    user.set_password(uPass1)
                    user.save()
                    return render(request, 'backoffice/password_changed_ok.html', parametros)
                else:
                    parametros['error_message'] = 'ERROR: Las contraseñas no coinciden.'

    return render(request, 'backoffice/password_change_form.html', parametros)
   
