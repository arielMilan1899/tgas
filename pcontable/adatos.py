# -*- coding: utf8 -*-
"""
"""
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Min, Max

# from tpvpos.models import TicketEntrada, Tarifa, AperturaCierreCajas
from fmaestros.models import Apunte

import decimal
from decimal import Decimal
import sys
from tgas import fcomunes
from fmaestros.models import Cuenta

reload(sys)
sys.setdefaultencoding('utf8')

"""
    fecha = models.DateField()
    descripcion = models.CharField(max_length=60)
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    es_gasto = models.BooleanField()
    cuenta = models.ForeignKey(Cuenta)

    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

"""

def devuelve_query_set(desde_fecha, hasta_fecha, es_gasto, cuenta):
    """
    Devuelve el query set básico filtrando por fecha y no nulos.
    :param desde_fecha:
    :param hasta_fecha:
    :param es_gasto:  True: GASTO, False: INGRESO
    :param cuenta: Si vale None no se filtra por cuenta
    :return:
    """

    if cuenta is None:
        query_set = Apunte.objects.filter()
    else:
        query_set = Apunte.objects.filter(cuenta=cuenta)

    query_set = query_set.filter(es_gasto=es_gasto)
    query_set = query_set.filter(fecha__gte=desde_fecha)
    query_set = query_set.filter(fecha__lte=hasta_fecha)
    return query_set

def ingreso_menos_gasto(ingreso, gasto):
    """
    Devuelve la resta de ingreso - gasto según esta tabla:
      Ingreso   Gasto   Resultado
       None      None    None
       None      g       -g
       i         None    i
       i         g       i-g

    :param ingreso:
    :param gasto:
    :return:
    """
    if ingreso is None:
        if gasto is None:
            return None
        else:
            return (-1) * gasto
    else:
        if gasto is None:
            return ingreso
        else:
            return ingreso-gasto

def devuelve_d_fechas(temporada):
    """
    Devuelve las fechas de inicio y fin de cada mes para 'temporada'
    :param temporada: 2018-2019
    :return: d_fechas
    """
    t = temporada.split('-')
    a0, a1 = int(t[0]), int(t[1])
    if a1-a0 != 1:
        raise ValueError('temporada "%s" erronea. Formato: "2018-2019"')

    d_fechas = {
        1:  (datetime.date(a1, 1, 1),  datetime.date(a1, 1, 31)),
        2:  (datetime.date(a1, 2, 1),  datetime.date(a1, 3, 1) - datetime.timedelta(days=1)),
        3:  (datetime.date(a1, 3, 1),  datetime.date(a1, 3, 31)),
        4:  (datetime.date(a1, 4, 1),  datetime.date(a1, 4, 30)),
        5:  (datetime.date(a1, 5, 1),  datetime.date(a1, 5, 31)),
        6:  (datetime.date(a1, 6, 1),  datetime.date(a1, 6, 30)),

        7:  (datetime.date(a0, 7, 1),  datetime.date(a0, 7, 31)),
        8:  (datetime.date(a0, 8, 1),  datetime.date(a0, 8, 31)),
        9:  (datetime.date(a0, 9, 1),  datetime.date(a0, 9, 30)),
        10: (datetime.date(a0, 10, 1), datetime.date(a0, 10, 31)),
        11: (datetime.date(a0, 11, 1), datetime.date(a0, 11, 30)),
        12: (datetime.date(a0, 12, 1), datetime.date(a0, 12, 31))
    }

    return d_fechas


def detalle_mensual_gastos_ingresos(temporada, cuenta=None):
    """
    :return:

    {1: {'gastos': None, 'ingresos': None},
     2: {'gastos': None, 'ingresos': None},
     3: {'gastos': None, 'ingresos': None},
     4: {'gastos': None, 'ingresos': None},
     5: {'gastos': None, 'ingresos': None},
     6: {'gastos': None, 'ingresos': None},
     7: {'gastos': None, 'ingresos': None},
     8: {'gastos': None, 'ingresos': None},
     9: {'gastos': Decimal('560.25'), 'ingresos': Decimal('3043.50')},
     10: {'gastos': None, 'ingresos': None},
     11: {'gastos': None, 'ingresos': None},
     12: {'gastos': None, 'ingresos': None},
     'total': {'gastos': Decimal('560.25'), 'ingresos': Decimal('3043.50')}}

    :return:
    """

    # l_fechas = {
    #     1: (datetime.date(2019, 1, 1), datetime.date(2019, 1, 31)),
    #     2: (datetime.date(2019, 2, 1), datetime.date(2019, 2, 28)),
    #     3: (datetime.date(2019, 3, 1), datetime.date(2019, 3, 31)),
    #     4: (datetime.date(2019, 4, 1), datetime.date(2019, 4, 30)),
    #     5: (datetime.date(2019, 5, 1), datetime.date(2019, 5, 31)),
    #     6: (datetime.date(2019, 6, 1), datetime.date(2019, 6, 30)),
    #
    #     7: (datetime.date(2018, 7, 1), datetime.date(2018, 7, 31)),
    #     8: (datetime.date(2018, 8, 1), datetime.date(2018, 8, 31)),
    #     9: (datetime.date(2018, 9, 1), datetime.date(2018, 9, 30)),
    #     10: (datetime.date(2018, 10, 1), datetime.date(2018, 10, 31)),
    #     11: (datetime.date(2018, 11, 1), datetime.date(2018, 11, 30)),
    #     12: (datetime.date(2018, 12, 1), datetime.date(2018, 12, 31))
    # }

    d_r = {}
    d_fechas = devuelve_d_fechas(temporada)

    for mes, per in d_fechas.items():
        d_r[mes] = {
            'gastos' : devuelve_query_set(desde_fecha=per[0], hasta_fecha=per[1],
                                          es_gasto=True, cuenta=cuenta)\
                .aggregate(Sum('importe'))['importe__sum'],
            'ingresos' : devuelve_query_set(desde_fecha=per[0], hasta_fecha=per[1],
                                            es_gasto=False, cuenta=cuenta)\
                .aggregate(Sum('importe'))['importe__sum'],
        }
        d_r[mes]['diferencia'] = ingreso_menos_gasto(d_r[mes]['ingresos'], d_r[mes]['gastos'])

    d_r['total'] = {
        'gastos': devuelve_query_set(desde_fecha=d_fechas[7][0], hasta_fecha=d_fechas[6][1],
                                     es_gasto=True, cuenta=cuenta)\
            .aggregate(Sum('importe'))['importe__sum'],
        'ingresos': devuelve_query_set(desde_fecha=d_fechas[7][0], hasta_fecha=d_fechas[6][1],
                                       es_gasto=False, cuenta=cuenta)\
            .aggregate(Sum('importe'))['importe__sum'],
        # 'gastos': devuelve_query_set(desde_fecha=datetime.date(2018, 7, 1), hasta_fecha=datetime.date(2019, 6, 30),
        #                              es_gasto=True, cuenta=cuenta)\
        #     .aggregate(Sum('importe'))['importe__sum'],
        # 'ingresos': devuelve_query_set(desde_fecha=datetime.date(2018, 7, 1), hasta_fecha=datetime.date(2019, 6, 30),
        #                                es_gasto=False, cuenta=cuenta)\
        #     .aggregate(Sum('importe'))['importe__sum'],
    }
    d_r['total']['diferencia'] = ingreso_menos_gasto(d_r['total']['ingresos'], d_r['total']['gastos'])
    return d_r


def detalle_mensual_gastos_ingresos_por_cuenta(temporada):
    """

    :param ano:
    :return: lista con un dict por cuenta.
    [ l_det_mens_por_cuenta
 {1: {'gastos': None, 'ingresos': None},
  2: {'gastos': None, 'ingresos': None},
  3: {'gastos': None, 'ingresos': None},
  4: {'gastos': None, 'ingresos': None},
  5: {'gastos': None, 'ingresos': None},
  6: {'gastos': None, 'ingresos': None},
  7: {'gastos': None, 'ingresos': None},
  8: {'gastos': None, 'ingresos': None},
  9: {'gastos': None, 'ingresos': None},
  10: {'gastos': None, 'ingresos': None},
  11: {'gastos': None, 'ingresos': None},
  12: {'gastos': None, 'ingresos': None},
  'cuenta': <Cuenta: CAMPO>,
  'total': {'gastos': None, 'ingresos': None}},
(...)
 {1: {'gastos': None, 'ingresos': None},
  2: {'gastos': None, 'ingresos': None},
  3: {'gastos': None, 'ingresos': None},
  4: {'gastos': None, 'ingresos': None},
  5: {'gastos': None, 'ingresos': None},
  6: {'gastos': None, 'ingresos': None},
  7: {'gastos': None, 'ingresos': None},
  8: {'gastos': None, 'ingresos': None},
  9: {'gastos': None, 'ingresos': Decimal('560.00')},
  10: {'gastos': None, 'ingresos': None},
  11: {'gastos': None, 'ingresos': None},
  12: {'gastos': None, 'ingresos': None},
  'cuenta': <Cuenta: CARNETS>,
  'total': {'gastos': None, 'ingresos': Decimal('560.00')}}
  ]

    """
    l_cuentas = Cuenta.objects.all().order_by('codigo')
    l_r = []
    for cuenta in l_cuentas:
        d = detalle_mensual_gastos_ingresos(temporada, cuenta=cuenta)
        d['cuenta'] = cuenta
        l_r.append(d)
    return l_r


def total_anual_gastos_ingresos_por_cuenta(temporada):
    """

    :param ano: Si None coge el año en curso
    :return: Un dict con l_cuentas y total. l_cuentas es una lista de dicts.
In [34]: adatos.detalle_mensual_gastos_ingresos_por_cuenta()
Out[34]:
{'l_cuentas': [{'cuenta': <Cuenta: AMBIGUS>,
   'diferencia': None,
   'gastos': None,
   'ingresos': None},
   (...)
  {'cuenta': <Cuenta: FISIO>,
   'diferencia': Decimal('-560.25'),
   'gastos': Decimal('560.25'),
   'ingresos': None},
  {'cuenta': <Cuenta: E.O. EJEMPLO>,
   'diferencia': None,
   'gastos': None,
   'ingresos': None}],
 'total': {'diferencia': Decimal('2483.25'),
  'gastos': Decimal('560.25'),
  'ingresos': Decimal('3043.50')}}

    """
    d_fechas = devuelve_d_fechas(temporada)
    desde = d_fechas[7][0]
    hasta = d_fechas[6][1]

    # desde = datetime.datetime.strptime('01/07/2018', '%d/%m/%Y')
    # hasta = datetime.datetime.strptime('30/06/2019', '%d/%m/%Y')

    l_cuentas = Cuenta.objects.all().order_by('codigo')
    d_r = {}
    l_r = []
    for cuenta in l_cuentas:
        d = {
            'cuenta': cuenta,
            'gastos': devuelve_query_set(desde_fecha=desde, hasta_fecha=hasta,
                                         es_gasto=True, cuenta=cuenta) \
                .aggregate(Sum('importe'))['importe__sum'],
            'ingresos': devuelve_query_set(desde_fecha=desde, hasta_fecha=hasta,
                                           es_gasto=False, cuenta=cuenta) \
                .aggregate(Sum('importe'))['importe__sum'],
        }
        d['diferencia'] = ingreso_menos_gasto(d['ingresos'], d['gastos'])
        l_r.append(d)
    d_r['l_cuentas'] = l_r
    d_r['total'] = {
        'gastos': devuelve_query_set(desde_fecha=desde, hasta_fecha=hasta,
                                     es_gasto=True, cuenta=None)\
            .aggregate(Sum('importe'))['importe__sum'],
        'ingresos': devuelve_query_set(desde_fecha=desde, hasta_fecha=hasta,
                                       es_gasto=False, cuenta=None)\
            .aggregate(Sum('importe'))['importe__sum'],
    }
    d_r['total']['diferencia'] = ingreso_menos_gasto(d_r['total']['ingresos'], d_r['total']['gastos'])

    return d_r



