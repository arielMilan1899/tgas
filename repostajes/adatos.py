# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from django.utils.crypto import get_random_string

from repostajes.models import Factura, Repostaje
from tgas.fcomunes import decimal2str, ultimo_dia_mes


def obtener_resumen(query_set):
    """
     Devuelve los acumulados por mes del total y por tipo de combustible de importes y litros consumidos.
     """

    resumenes = {}

    for mes in range(1, 13):
        resumen_mes = query_set \
            .filter(fecha_creacion__month=mes) \
            .aggregate(total_importe=Sum('importe'), total_litros=Sum('litros'))
        total_importe = resumen_mes['total_importe'] if resumen_mes['total_importe'] else Decimal(0)
        total_litros = resumen_mes['total_litros'] if resumen_mes['total_litros'] else Decimal(0)
        resumenes[mes] = {'importe': total_importe, 'litros': total_litros}

    resumenes['total'] = reduce(lambda acumulado, actual: {'importe': acumulado['importe'] + actual['importe'],
                                                           'litros': acumulado['litros'] + actual['litros']},
                                resumenes.values())

    return resumenes


def obtener_factura_mensual(usuario, ano, mes):
    """
    Devuelve la factura mensual de un usuario.
    :return:
    """

    now = timezone.now()
    dia_actual = now.day
    ano_actual = now.year
    mes_actual = now.month

    try:
        factura = Factura.objects.get(usuario_id=usuario.id, fecha_creacion__year=ano, fecha_creacion__month=mes,
                                      es_mensual=True)

        if ano_actual == ano and mes_actual == mes:
            importe = Repostaje.objects.filter(usuario_id=usuario.id, fecha_creacion__year=ano,
                                               fecha_creacion__month=mes).aggregate(importe=Sum('importe'))['importe']

            if factura.importe != importe:
                factura.importe = importe if importe else Decimal(0.000)
                factura.save()

    except Factura.DoesNotExist:
        codigo_factura = '%s%s%s' % (get_random_string(length=10), ano, mes)
        factura = Factura(codigo=codigo_factura.upper(), usuario=usuario, es_mensual=True)

        fecha = datetime.datetime(ano, mes, dia_actual)

        if ano > ano_actual or (ano_actual == ano and mes > mes_actual):
            return None

        if ano_actual > ano or (ano_actual == ano and mes_actual > mes):
            fecha = ultimo_dia_mes(fecha)

        importe = Repostaje.objects.filter(usuario_id=usuario.id,
                                           fecha_creacion__year=ano,
                                           fecha_creacion__month=mes).aggregate(importe=Sum('importe'))['importe']

        factura.importe = importe if importe else Decimal(0)

        factura.save()

        factura.fecha_creacion = fecha

        factura.save()

    return factura
