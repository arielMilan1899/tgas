#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
  Script para crear automáticamente el fichero  telemap.css
  según el esquema de colores deseado.

    Cambiar el dict d_colors para establecer nuevos colores.

"""
import os
import shutil
import datetime


#   Esquema del Interfaz de Usuario de las aplicaciones 'TAF'
#
#    +------------------------+---+--------------------------------------------+
#    |  [main-header-logo]    |(=)|    [main-header-navbar]+[center-navbar]    |
#    +------------------------+---+--------------------------------------------+
#    |    [user-panel]        |                                                |
#    |                        |    (=) : sidebar-toggle                        |
#    +------------------------+                                                |
#    |   [left-side-navbar]   |                                                |
#    |                        |                                                |
#    |  Menu Nivel 1          |                                                |
#    |      Menu Nivel 2      |                                                |
#    |                        |                                                |
#    |                        |                                                |
#    |                        +------------------------------------------------+
#    |                        |             [main-footer]                      |
#    +------------------------+------------------------------------------------+
#

d_colors_skinblue = {
    # Barra superior (derecha)
    'main-header-navbar-fondo':  '#3c8dbc',
    'center-navbar-texto':  '#ffffff',
    # Barra superior (sidebar-toggle)
    'sidebar-toggle-fondo': '#3c8dbc',
    'sidebar-toggle-texto': '#ffffff',
    'sidebar-toggle-hover-fondo': '#367fa9',
    'sidebar-toggle-hover-texto': '#f6f6f6',
    # Barra superior (Parte superior barra lateral)
    'main-header-logo-fondo': '#367fa9',
    'main-header-logo-texto': '#ffffff',
    'main-header-logo-hover-fondo': '#357ca5',
    # Barra lateral (logo circular y usuario)
    'user-panel-fondo': '#222d32',
    'user-panel-texto': '#ffffff',
    # Barra lateral
    'left-side-navbar-fondo': '#222d32',
    # Barra lateral (menú en árbol - nivel 1)
    'menu-nivel1-texto': '#b8c7ce',
    'menu-nivel1-hover-and-selected-fondo': '#1e282c',
    'menu-nivel1-hover-and-selected-texto': '#ffffff',
    # Barra lateral (menú en árbol - nivel 2)
    'menu-nivel2-texto': '#8aa4af',
    'menu-nivel2-fondo': '#2c3b41',
    'menu-nivel2-hover-texto': '#ffffff',
    # Barra inferior
    'main-footer-fondo': '#ffffff',
    'main-footer-texto': '#444444',
}

d_colors_ino_ice = {
    # Barra superior (derecha)
    'main-header-navbar-fondo':  '#000000',
    'center-navbar-texto':  '#ffffff',
    # Barra superior (sidebar-toggle)
    'sidebar-toggle-fondo': '#000000',
    'sidebar-toggle-texto': '#ffffff',
    'sidebar-toggle-hover-fondo': '#367fa9',
    'sidebar-toggle-hover-texto': '#f6f6f6',
    # Barra superior (Parte superior barra lateral)
    'main-header-logo-fondo': '#000000',
    'main-header-logo-texto': '#ffffff',
    'main-header-logo-hover-fondo': '#357ca5',
    # Barra lateral (logo circular y usuario)
    'user-panel-fondo': '#0079C8',
    'user-panel-texto': '#ffffff',
    # Barra lateral
    'left-side-navbar-fondo': '#0079C8',
    # Barra lateral (menú en árbol - nivel 1)
    'menu-nivel1-texto': '#b8c7ce',
    'menu-nivel1-hover-and-selected-fondo': '#357ca5',
    'menu-nivel1-hover-and-selected-texto': '#ffffff',
    # Barra lateral (menú en árbol - nivel 2)
    'menu-nivel2-texto': '#E6E6FA',
    'menu-nivel2-fondo': '#3c8dbc',
    'menu-nivel2-hover-texto': '#ffffff',
    # Barra inferior
    'main-footer-fondo': '#ffffff',
    'main-footer-texto': '#444444',
}


css_template = """
/*
 *  ----- Fichero %(filename)s creado en fecha %(fechahora)s  -------- 
 */

/* main-header-navbar-fondo */
.skin-blue .main-header .navbar {
  background-color: %(main-header-navbar-fondo)s;
}
.skin-blue .main-header .navbar .nav > li > a {
  color: #f00;
}
.skin-blue .main-header .navbar .nav > li > a:hover,
.skin-blue .main-header .navbar .nav > li > a:active,
.skin-blue .main-header .navbar .nav > li > a:focus,
.skin-blue .main-header .navbar .nav .open > a,
.skin-blue .main-header .navbar .nav .open > a:hover,
.skin-blue .main-header .navbar .nav .open > a:focus,
.skin-blue .main-header .navbar .nav > .active > a {
  background: rgba(0, 0, 0, 0.1);
  color: #f6f6f6;
}

/* sidebar-toggle-fondo */
.skin-blue .main-header .navbar .sidebar-toggle {
  color: %(sidebar-toggle-texto)s;
  background: %(sidebar-toggle-fondo)s;
  
}

/* sidebar-toggle-hover-texto */
.skin-blue .main-header .navbar .sidebar-toggle:hover {
  color: %(sidebar-toggle-hover-texto)s;
  background: rgba(0, 0, 0, 0.1);
}

/* sidebar-toggle-hover-fondo */
.skin-blue .main-header .navbar .sidebar-toggle:hover {
  background-color: %(sidebar-toggle-hover-fondo)s;
}

@media (max-width: 767px) {
  .skin-blue .main-header .navbar .dropdown-menu li.divider {
    background-color: rgba(255, 255, 255, 0.1);
  }
  .skin-blue .main-header .navbar .dropdown-menu li a {
    color: #fff;
  }
  .skin-blue .main-header .navbar .dropdown-menu li a:hover {
    background: #367fa9;
  }
}

/* main-header-logo (fondo y texto) */
.skin-blue .main-header .logo {
  background-color: %(main-header-logo-fondo)s;
  color: %(main-header-logo-texto)s;
  border-bottom: 0 solid transparent;
}

/* main-header-logo-hover-fondo */
.skin-blue .main-header .logo:hover {
  background-color: %(main-header-logo-hover-fondo)s;
}
.skin-blue .main-header li.user-header {
  background-color: #3c8dbc;
}
.skin-blue .content-header {
  background: transparent;
}

/* left-side-navbar-fondo */
.skin-blue .wrapper,
.skin-blue .main-sidebar,
.skin-blue .left-side {
  background-color: %(left-side-navbar-fondo)s;
}

/* user-panel (fondo y texto) */
.skin-blue .user-panel {
    background-color: %(user-panel-fondo)s;
    color: %(user-panel-texto)s;
}

.skin-blue .user-panel > .info,
.skin-blue .user-panel > .info > a {
  color: #fff;
}
.skin-blue .sidebar-menu > li.header {
  color: #4b646f;
  background: #1a2226;
}
.skin-blue .sidebar-menu > li > a {
  border-left: 3px solid transparent;
}

/* menu-nivel1-hover-and-selected (fondo y texto)*/
.skin-blue .sidebar-menu > li:hover > a,
.skin-blue .sidebar-menu > li.active > a {
  color: %(menu-nivel1-hover-and-selected-texto)s;
  background: %(menu-nivel1-hover-and-selected-fondo)s;
  border-left-color: #3c8dbc;
}

/* menu-nivel2-fondo */
.skin-blue .sidebar-menu > li > .treeview-menu {
  margin: 0 1px;
  background: %(menu-nivel2-fondo)s;
}

/* menu-nivel1-texto */
.skin-blue .sidebar a {
  color: %(menu-nivel1-texto)s;
}
.skin-blue .sidebar a:hover {
  text-decoration: none;
}

/* menu-nivel2-texto*/
.skin-blue .treeview-menu > li > a {
  color: %(menu-nivel2-texto)s;
}

/* menu-nivel2-hover-texto */
.skin-blue .treeview-menu > li.active > a,
.skin-blue .treeview-menu > li > a:hover {
  color: %(menu-nivel2-hover-texto)s;
}
.skin-blue .sidebar-form {
  border-radius: 3px;
  border: 1px solid #374850;
  margin: 10px 10px;
}
.skin-blue .sidebar-form input[type="text"],
.skin-blue .sidebar-form .btn {
  box-shadow: none;
  background-color: #374850;
  border: 1px solid transparent;
  height: 35px;
}
.skin-blue .sidebar-form input[type="text"] {
  color: #666;
  border-top-left-radius: 2px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 2px;
}
.skin-blue .sidebar-form input[type="text"]:focus,
.skin-blue .sidebar-form input[type="text"]:focus + .input-group-btn .btn {
  background-color: #fff;
  color: #666;
}
.skin-blue .sidebar-form input[type="text"]:focus + .input-group-btn .btn {
  border-left-color: #fff;
}
.skin-blue .sidebar-form .btn {
  color: #999;
  border-top-left-radius: 0;
  border-top-right-radius: 2px;
  border-bottom-right-radius: 2px;
  border-bottom-left-radius: 0;
}
.skin-blue.layout-top-nav .main-header > .logo {
  background-color: #3c8dbc;
  color: #ffffff;
  border-bottom: 0 solid transparent;
}
.skin-blue.layout-top-nav .main-header > .logo:hover {
  background-color: #3b8ab8;
}

/* main-footer (fondo y texto) */
.main-footer {
  background: %(main-footer-fondo)s;
  color: %(main-footer-texto)s;
}

/* center-navbar-texto */
.center-navbar {
  color: %(center-navbar-texto)s;  
}

/********************************************************/

.table > tbody > tr > td,
.table > tbody > tr > th,
.table > tfoot > tr > td,
.table > tfoot > tr > th,
.table > thead > tr > td,
.table > thead > tr > th {
  padding: 2px;
}

table.uifmaestros {
  border-collapse: separate;
  border-spacing: 10px;
}

.input_decimal {text-align: right;}

/* input.error */
input.error
{
 /* border:1px solid red; */
 box-shadow: 0px 2px 6px rgba(255, 0, 0, .7);
}

select.error
{
 /* border:1px solid red; */
 box-shadow: 0px 2px 6px rgba(255, 0, 0, .7);
}

.fieldContainer {
    position: relative;
    margin-bottom: 20px;
}

label.error {
    position: relative;
    right: 143px;
    top: -25px;
    border: solid 1px #000;
/*    color: white;
    background: #333;
*/    color: black;
    background: white;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, .7);
    padding: 2px 5px;
    border-radius: 5px;
}


"""

def graba_css(filename, css_template, d_colors):
    """
    Crea el fichero CSS según la plantilla (css_template) y las variables (d_colors).
    Si ya existía crea primero una copia del actual.
    :param filename:
    :return:
    """
    nombre_proyecto = os.path.split(os.getcwd())[-1]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", nombre_proyecto + ".settings")
    from django.conf import settings
    django_static_files_path = settings.STATICFILES_DIRS[0]
    # '/mnt/debian_9/home/desarrollo/telemap/crmta/crmta/staticfiles'

    base_path = os.path.join(django_static_files_path, 'backoffice/css_js_propios/')
    filename_full_path = os.path.join(base_path, filename)
    filename_bak = filename + datetime.datetime.now().strftime('_%Y%m%d_%H%M%S.bak')

    if os.path.isfile(filename_full_path):
        print('Ya existía "%s" realizando backup a "%s"\n en "%s".' % (filename, filename_bak, base_path))
        shutil.copy2(filename_full_path, os.path.join(base_path, filename_bak))

    d_colors['filename'] = filename
    d_colors['fechahora'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(filename_full_path, 'w') as f:
        f.write(css_template % d_colors)

    return True


if __name__ == '__main__':
    graba_css(filename='telemap.css', css_template=css_template, d_colors=d_colors_skinblue)
