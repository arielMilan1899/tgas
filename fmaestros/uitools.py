# -*- coding: utf8 -*-
import models
from repostajes.models import Repostaje
from usuarios.models import Usuario

# from poblaciones import models as poblaciones_models
# import config.models as config_models

def dime_lista_ids_navegacion(apartado, id_actual):
    """

    :param apartado:
    :param id_actual:
    :return:
    """

    print apartado, id_actual


    d_maestros = {

        'empresas': models.Empresa,
        'cuentas': models.Cuenta,
        'apuntes': models.Apunte,
        'usuarios': Usuario,
        'provincia': models.Provincia,
        'estaciones': models.Estacion,
        'combustibles': models.Combustible,
        'repostajes': Repostaje,
    }

    if id_actual is None:
        id_primero = id_anterior = id_siguiente = id_ultimo = None

    else:
        l_ids = d_maestros[apartado].objects.filter().values_list('id', flat=True)

        print l_ids

        pos_id_actual = None
        for i, dato in enumerate(l_ids):
            if dato == id_actual:
                pos_id_actual = i

        pos_id_ultimo = len(l_ids)-1
        # print l_ids, pos_id_actual, pos_id_ultimo

        if pos_id_actual == 0 :
            id_primero = None
            id_anterior = None
        else:
            id_primero = l_ids[0]
            id_anterior = l_ids[pos_id_actual - 1]

        if pos_id_actual == pos_id_ultimo :
            id_siguiente = None
            id_ultimo = None
        else:
            id_siguiente = l_ids[pos_id_actual + 1]
            id_ultimo = l_ids[pos_id_ultimo]

    return (id_primero, id_anterior, id_siguiente, id_ultimo)


def barra_botones(accion, request):
    """
    accion= 'editar' o 'visualizar'
    Devuelve el código html para pintar la barra de botones
    :return:
    """
    l_path = request.get_full_path().split('/')
    apartado = l_path[1]
    try:
        proceso = l_path[2]
    except IndexError:
        proceso = None

    l_full_path = request.get_full_path().split('=')
    path_sin_id = l_full_path[0]
    try:
        id_actual = int(l_full_path[1].replace('.',''))
    except IndexError:
        id_actual = None
    # print(request.path) #u'/emplazamientos/editar/'
    # print(request.get_full_path()) #u'/emplazamientos/editar/?dato_id=2'
    # print(request.build_absolute_uri()) #'http://localhost:8000/emplazamientos/editar/?dato_id=2'

    (id_primero, id_anterior, id_siguiente, id_ultimo) = dime_lista_ids_navegacion(apartado, id_actual)
    # print (id_primero, id_anterior, id_siguiente, id_ultimo)

    l_botones = [
        {'tit': u'Primero',   'href': '%s=%s' % (path_sin_id, id_primero), 'onclick': "", 'ico': 'fa-fast-backward'},
        {'tit': u'Anterior',  'href': '%s=%s' % (path_sin_id, id_anterior), 'onclick': "", 'ico': 'fa-arrow-left'},
        {'tit': u'Siguiente', 'href': '%s=%s' % (path_sin_id, id_siguiente), 'onclick': "", 'ico': 'fa-arrow-right'},
        {'tit': u'Último',    'href': '%s=%s' % (path_sin_id, id_ultimo), 'onclick': "", 'ico': 'fa-fast-forward'},
        {'tit': u'Añadir',    'href': "/%s/add" % apartado, 'onclick': "", 'ico': 'fa-plus'},
        {'tit': u'Eliminar',  'href': "/%s/remove/?dato_id=%s" % (apartado, id_actual), 'onclick': "", 'ico': 'fa-trash-o'},
        {'tit': u'Modificar', 'href': '#', 'onclick': "barra_botones('editar');", 'ico': 'fa-pencil'},
        {'tit': u'Guardar',   'href': '#', 'onclick': "barra_botones('grabar_recalcular');", 'ico': 'fa-floppy-o'},
        {'tit': u'Cancelar',  'href': request.get_full_path(), 'onclick': "", 'ico': 'fa-remove'},
        {'tit': u'Salir',     'href': "/%s/list" % apartado, 'onclick': "", 'ico': 'fa-sign-out'},
    ]

    d_acciones = {
        'nuevo' : {   # Button Enabled ?
            u'Primero'   : False,
            u'Anterior'  : False,
            u'Siguiente' : False,
            u'Último'    : False,
            u'Añadir'    : False,
            u'Eliminar'  : False,
            u'Modificar' : False,
            u'Guardar'   : True,
            u'Cancelar'  : False,
            u'Salir'     : True,
            },
        'editar' : {   # Button Enabled ?
            u'Primero'   : False,
            u'Anterior'  : False,
            u'Siguiente' : False,
            u'Último'    : False,
            u'Añadir'    : False,
            u'Eliminar'  : False,
            u'Modificar' : False,
            u'Guardar'   : True,
            u'Cancelar'  : True,
            u'Salir'     : False,
            },
        'visualizar': {
            u'Primero'   : True,
            u'Anterior'  : True,
            u'Siguiente' : True,
            u'Último'    : True,
            u'Añadir'    : True,
            u'Eliminar'  : True,
            u'Modificar' : True,
            u'Guardar'   : False,
            u'Cancelar'  : False,
            u'Salir'     : True,
            },
        'editar1solodato' : {   # Button Enabled ?
            u'Primero'   : False,
            u'Anterior'  : False,
            u'Siguiente' : False,
            u'Último'    : False,
            u'Añadir'    : False,
            u'Eliminar'  : False,
            u'Modificar' : False,
            u'Guardar'   : True,
            u'Cancelar'  : True,
            u'Salir'     : False,
            },
        'visualizar1solodato': {
            u'Primero'   : False,
            u'Anterior'  : False,
            u'Siguiente' : False,
            u'Último'    : False,
            u'Añadir'    : False,
            u'Eliminar'  : False,
            u'Modificar' : True,
            u'Guardar'   : False,
            u'Cancelar'  : False,
            u'Salir'     : False,
        }}


    html_template = """
        <a title="%(tit)s" class="btn btn-social-icon btn-linkedin %(disabled)s" data-toggle="tooltip"
           href="%(href)s" onclick="%(onclick)s"> <i class="fa %(ico)s"></i></a>
        """
    html_botones = ""
    for boton in l_botones:
        # Se activan o desactivan los botones dependiendo de si se edita o se visualiza
        boton['disabled'] = '' if d_acciones[accion][boton['tit']] else 'disabled'
        # Se activan o desactivan los botones de primero, anterior, siguiente y
        # ultimo dependiendo de la si es el primero o el ultimo
        if (id_primero is None) and (boton['tit'] == u'Primero'):
            boton['disabled'] = 'disabled'
        elif (id_anterior is None) and (boton['tit'] == u'Anterior'):
            boton['disabled'] = 'disabled'
        elif (id_siguiente is None) and (boton['tit'] == u'Siguiente'):
            boton['disabled'] = 'disabled'
        elif (id_ultimo is None) and (boton['tit'] == u'Último'):
            boton['disabled'] = 'disabled'

        html_botones += html_template % boton


    return html_botones
