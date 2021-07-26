# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
plenoil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import usuarios.views as usuarios_views
import usuarios.login_tools as usuarios_login_tools
import fmaestros.views as fmaestros_views
import repostajes.views as repostajes_views


urlpatterns = [
# ('^my_page/$', csrf_exempt(direct_to_template), {'template': 'my_page.html'})
    url(r'^admin/', admin.site.urls),
    url(r'^$', usuarios_views.bienvenido, name='home'),

    # url(r'^password_change/$', usuarios_login_tools.Change_Password),
    # url(r'^forgotten_password/$', usuarios_views.forgotten_password),
    url(r'^login/$', usuarios_login_tools.my_login),
    url(r'^logout/$', usuarios_login_tools.my_logout),
    url(r'^accounts/login/$', usuarios_login_tools.my_login),
    url(r'^accounts/logout/$', usuarios_login_tools.my_logout),

    url(r'^accounts/profile/$', usuarios_views.bienvenido),
    url(r'^profile/$', usuarios_views.bienvenido),

    # url(r'^profile/$', usuarios_views.bienvenido, name='facturas'),
    # url(r'^profile/$', usuarios_views.bienvenido, name='resumen'),
    url(r'^accounts/password_change/$', usuarios_login_tools.Change_Password, name='cambiar_passwd'),
    url(r'^accounts/logout/$', usuarios_login_tools.my_logout, name='salir'),

    url(r'^usuarios/$', fmaestros_views.usuarios_listado, name='fich-usuarios-list'),
    url(r'^usuarios/list/$', fmaestros_views.usuarios_listado, name='fich-usuarios-list'),
    url(r'^usuarios/list/add/$', fmaestros_views.usuarios_nuevo, name='fich-usuarios-nuevo'),
    url(r'^usuarios/add/$', fmaestros_views.usuarios_nuevo, name='fich-usuarios-nuevo'),
    url(r'^usuarios/edit/$', fmaestros_views.usuarios_editar, name='fich-usuarios-editar'),
    url(r'^usuarios/mydata/$', fmaestros_views.usuarios_mis_datos, name='usuarios-mis-datos'),
    url(r'^usuarios/remove/$', fmaestros_views.usuarios_borrar, name='fich-usuarios-borrar'),
    url(r'^usuarios/reestablece_password/$', fmaestros_views.usuarios_reestablece_password,
        name='fich-usuarios-reestablece_password'),

# _____________ INI Código añadido por crea_prototipo_fmaestros.py

    url(r'^provincia/$',          fmaestros_views.provincia_listado,  name='provincia-list'),
    url(r'^provincia/list/$',     fmaestros_views.provincia_listado,  name='provincia-list'),
    url(r'^provincia/list/add/$', fmaestros_views.provincia_nuevo,    name='provincia-nuevo'),
    url(r'^provincia/add/$',      fmaestros_views.provincia_nuevo,    name='provincia-nuevo'),
    url(r'^provincia/edit/$',     fmaestros_views.provincia_editar,   name='provincia-editar'),
    url(r'^provincia/remove/$',   fmaestros_views.provincia_borrar,   name='provincia-borrar'),

# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

# _____________ INI Código añadido por crea_prototipo_fmaestros.py

    url(r'^estaciones/$',          fmaestros_views.estaciones_listado,  name='estaciones-list'),
    url(r'^estaciones/list/$',     fmaestros_views.estaciones_listado,  name='estaciones-list'),
    url(r'^estaciones/list/add/$', fmaestros_views.estaciones_nuevo,    name='estaciones-nuevo'),
    url(r'^estaciones/add/$',      fmaestros_views.estaciones_nuevo,    name='estaciones-nuevo'),
    url(r'^estaciones/edit/$',     fmaestros_views.estaciones_editar,   name='estaciones-editar'),
    url(r'^estaciones/remove/$',   fmaestros_views.estaciones_borrar,   name='estaciones-borrar'),
    url(r'^estaciones/ver/$',      fmaestros_views.estaiciones_ver, name='estaciones-ver'),
    url(r'^estaciones/ver_mapa/$', fmaestros_views.estaiciones_ver_mapa, name='estaciones-mapa'),
    url(r'^estaciones/nuevos_precios', fmaestros_views.estaciones_nuevos_precios_combustibles, name='estaciones-nuevos-precios'),

    # _______________ FIN Código añadido por crea_prototipo_fmaestros.py

    url(r'^repostajes/$', repostajes_views.repostaje_listado, name='repostajes-list'),
    url(r'^repostajes/list/$', repostajes_views.repostaje_listado, name='repostajes-list'),
    url(r'^repostajes/nuevo', repostajes_views.repostaje_nuevo_rest, name='repostajes-nuevo'),
    url(r'^repostajes/add/$', repostajes_views.repostaje_nuevo, name='repostajes-nuevo'),
    url(r'^repostajes/list/add/$', repostajes_views.repostaje_nuevo, name='repostajes-nuevo'),
    url(r'^repostajes/edit/$', repostajes_views.repostaje_editar, name='repostajes-editar'),
    url(r'^consumos/$', repostajes_views.consumos, name='consumos'),
    url(r'^facturas/$', repostajes_views.consumos, name='facturas-list'),
    url(r'^facturas/list/$', repostajes_views.facturas_listado, name='facturas-list'),
    url(r'^facturas/download/$', repostajes_views.descargar_factura, name='facturas-download'),


# _____________ INI Código añadido por crea_prototipo_fmaestros.py
 
    url(r'^combustibles/$',          fmaestros_views.combustibles_listado,  name='combustibles-list'),
    url(r'^combustibles/list/$',     fmaestros_views.combustibles_listado,  name='combustibles-list'),
    url(r'^combustibles/list/add/$', fmaestros_views.combustibles_nuevo,    name='combustibles-nuevo'),
    url(r'^combustibles/add/$',      fmaestros_views.combustibles_nuevo,    name='combustibles-nuevo'),
    url(r'^combustibles/edit/$',     fmaestros_views.combustibles_editar,   name='combustibles-editar'),
    url(r'^combustibles/remove/$',   fmaestros_views.combustibles_borrar,   name='combustibles-borrar'),

# _______________ FIN Código añadido por crea_prototipo_fmaestros.py
]
