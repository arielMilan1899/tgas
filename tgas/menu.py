# -*- coding: utf-8 -*-
"""
Created on 2017-02-13 19:06:48

@author: jrocamonde

Menú para la aplicación
"""

from django.core.urlresolvers import reverse
from usuarios.models import Usuario
# Atencion ------------------------------------
# tda_arbol importa NetworkX y da problemas con Debian 9 + Apache WSGI
# Comento las funciones devuelve_arbol_menu, devuelve_html_breadcrumb, devuelve_mapa_web
# import tda_arbol
# ------------------------


menu_solo_consulta = [
    {'tit': u'Inicio',       'url-name': 'home',      'ico': 'fa-home', 'submenu': []},
    {'tit': u'Estaciones',       'url-name': 'estaciones-list',      'ico': 'fa-industry', 'submenu': []},
    {'tit': u'Repostajes',       'url-name': 'repostajes-list',      'ico': 'fa-tint', 'submenu': []},
    {'tit': u'Consumos',  'url-name': 'consumos',      'ico': 'fa-line-chart', 'submenu': []},
    {'tit': u'Facturas',  'url-name': 'facturas-list',      'ico': 'fa-euro', 'submenu': []},
    {'tit': u'Mapa',       'url-name': 'estaciones-mapa',      'ico': 'fa-map', 'submenu': []},
    {'tit': u'Cuenta',  'url-name': 'usuarios-mis-datos', 'ico': 'fa-user', 'submenu': []},
    {'tit': u'Cambiar contraseña',  'url-name': 'cambiar_passwd', 'ico': 'fa-lock', 'submenu': []},
    {'tit': u'Salir',               'url-name': 'salir',          'ico': 'fa-sign-out', 'submenu': []},
]


# menu_eoperadora = [
#     {'tit': u'Facturas',            'url-name': None,               'ico': 'fa-eur', 'submenu': menu_facturas},
#     {'tit': u'Modelo 347',  'url-name': None, 'ico': 'fa-bar-chart', 'submenu': menu_347},
#     {'tit': u'E. Operadoras',       'url-name': 'fich-empresas-list',      'ico': 'fa-institution', 'submenu': []},
#     {'tit': u'Titulares',           'url-name': None, 'ico': 'fa-coffee', 'submenu': menu_ver_titulares},
#     {'tit': u'Usuarios',           'url-name': 'fich-usuarios-list', 'ico': 'fa-user', 'submenu': menu_usuarios},
#     {'tit': u'Modelos Documentos',  'url-name': None, 'ico': 'fa-file-text-o', 'submenu': menu_modelosdocs},
#     {'tit': u'Cambiar contraseña',  'url-name': 'cambiar_passwd', 'ico': 'fa-lock', 'submenu': []},
#     {'tit': u'Salir',               'url-name': 'salir',          'ico': 'fa-sign-out', 'submenu': []},
# ]
menu_admin = [
    {'tit': u'Estaciones',       'url-name': 'estaciones-list',      'ico': 'fa-industry', 'submenu': []},
    {'tit': u'Repostajes',       'url-name': 'repostajes-list',      'ico': 'fa-tint', 'submenu': []},
    {'tit': u'Consumos',       'url-name': 'consumos',      'ico': 'fa-line-chart', 'submenu': []},
    {'tit': u'Provincias',       'url-name': 'provincia-list',      'ico': 'fa-map-marker', 'submenu': []},
    {'tit': u'Combustibles',       'url-name': 'combustibles-list',      'ico': 'fa-fire', 'submenu': []},
    {'tit': u'Usuarios',           'url-name': 'fich-usuarios-list', 'ico': 'fa-user', 'submenu': []},
    {'tit': u'Mapa',       'url-name': 'estaciones-mapa',      'ico': 'fa-map', 'submenu': []},
    {'tit': u'Cambiar contraseña',  'url-name': 'cambiar_passwd', 'ico': 'fa-lock', 'submenu': []},
    {'tit': u'Salir',               'url-name': 'salir',          'ico': 'fa-sign-out', 'submenu': []},
]


def devuelve_html_menu_izquierdo_por_usuario(usuario):
    """
    Es necesario que exista un grupo "encargado" dentro de django-admin
    al que pertenezcan los usuarios que tengan rol de encargado.

    :param usuario:
    :return:
    """
    # if usuario.grupo.all()[0].nombre == 'eoperadora':
    #     nombre_menu = menu_solo_consulta
    # else:
    #     nombre_menu = menu_admin
    #
    if Usuario.objects.filter(username=usuario.username)[0].es_admin :
        nombre_menu = menu_admin
    else:
        nombre_menu = menu_solo_consulta
    # nombre_menu = menu_admin
    return devuelve_html_menu_izquierdo(nombre_menu)



def devuelve_html_menu_izquierdo(l_menu, nivel=0):
    """
    Devuelve codigo HTML correspondiente a la construcción del menú bootstrap izquierdo
    La primera vez debe llamarse con nivel=1 o sin el parametro nivel
    Ejemplo:
       devuelve_menu_html(menu_ppal)
    :param l_menu: lista de dicts como ppal_maquinas
    :param nivel: siempre 0
    :return:
    código html para bootstrap:
    <ul class="sidebar-menu"> ... </ul>
    """
    d_html = {}
    d_html['0_cab'] = """
      <ul class="sidebar-menu">"""
    d_html['0_cab_item'] = """
        <li class="active treeview">
          <a href="%(url)s"><i class="fa %(ico)s"></i> <span>%(tit)s</span></a>"""
    d_html['0_cab_item_submenu'] = """
        <li class="treeview">
          <a href="%(url)s">
            <i class="fa %(ico)s"></i> <span>%(tit)s</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
          </a>"""
    d_html['1_cab'] = """
          <ul class="treeview-menu">"""
    d_html['1_cab_item'] = """
            <li><a href="%(url)s"><i class="fa %(ico)s"></i>%(tit)s</a>"""
    d_html['1_cab_item_submenu'] = """
            <li>
              <a href="%(url)s"><i class="fa %(ico)s"></i>%(tit)s
                <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                </span>
              </a>"""
    d_html['2_cab'] = """
              <ul class="treeview-menu">"""
    d_html['2_cab_item'] = """
                <li><a href="%(url)s"><i class="fa %(ico)s"></i>%(tit)s</a>"""
    d_html['2_cab_item_submenu'] = """
                <li>
                  <a href="%(url)s"><i class="fa %(ico)s"></i>%(tit)s
                    <span class="pull-right-container">
                      <i class="fa fa-angle-left pull-right"></i>
                    </span>
                  </a>"""

    d_html['3_cab'] = """
                    <ul class="treeview-menu">"""
    d_html['3_cab_item'] = """
                      <li><a href="%(url)s"><i class="fa %(ico)s"></i>%(tit)s</a>"""
    d_html['3_cab_item_submenu'] = """
                      <li>
                        <a href="%(url)s"><i class="fa %(ico)s"></i>%(tit)s
                          <span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                          </span>
                        </a>"""
    d_html['3_pie_item'] = """
                      </li>"""
    d_html['3_pie'] = """
                    </ul>"""
    d_html['2_pie_item'] = """
                </li>"""
    d_html['2_pie'] = """
              </ul>"""
    d_html['1_pie_item'] = """
            </li>"""
    d_html['1_pie'] = """
          </ul>"""
    d_html['0_pie_item'] = """
        </li>"""
    d_html['0_pie'] = """
      </ul>"""

    html = d_html['%s_cab' % nivel]
    for d_menu in l_menu:
        d_vars = {'tit': d_menu['tit'],
                  'url': '#',
                  'ico': d_menu['ico']}
        try:
            d_vars['url'] = reverse(d_menu['url-name'])
        except:
            pass
        # print "="*80, d_vars
        if d_menu['submenu'] != []:
            html += d_html['%s_cab_item_submenu' % nivel] % d_vars
            html += devuelve_html_menu_izquierdo(d_menu['submenu'], nivel + 1)
        else:
            html += d_html['%s_cab_item' % nivel] % d_vars
        html += d_html['%s_pie_item' % nivel]
    html += d_html['%s_pie' % nivel]
    return html


def devuelve_html_notificaciones(l_notificaciones=[]):
    """
    Notificaciones que cuelgan de la "campana" de la barra superior,
    al lado del nombre. Bootstrap "notifications-menu"
    :return:
    """
    html = """
          <li class="dropdown notifications-menu">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
              <i class="fa fa-bell-o"></i>
              <span class="label label-danger">10</span>
            </a>
            <!--- ini notifications -->
            <ul class="dropdown-menu">
              <li class="header">You have 10 notifications</li>
              <li>
                <!-- inner menu: contains the actual data -->
                <ul class="menu">
                  <li>
                    <a href="#">
                      <i class="fa fa-users text-aqua"></i> 5 new members joined today
                    </a>
                  </li>
                  <li>
                    <a href="#">
                      <i class="fa fa-warning text-yellow"></i> Very long description here that may not fit into the
                      page and may cause design problems
                    </a>
                  </li>
                  <li>
                    <a href="#">
                      <i class="fa fa-users text-red"></i> 5 new members joined
                    </a>
                  </li>
                  <li>
                    <a href="#">
                      <i class="fa fa-shopping-cart text-green"></i> 25 sales made
                    </a>
                  </li>
                  <li>
                    <a href="#">
                      <i class="fa fa-user text-red"></i> You changed your username
                    </a>
                  </li>
                </ul>
              </li>
              <li class="footer"><a href="#">View all</a></li>
            </ul>
            <!--- fin notifications -->
          </li>
    """
    return html
