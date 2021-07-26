# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 18:05:05 2014

@author: jrocamonde
"""

import datetime
import decimal
import pickle,zlib,base64,urllib
import pytz
import psycopg2
from decimal import Decimal, ROUND_HALF_UP

import pprint

from django.conf import settings
from cvc.cifrado import Encripta, Desencripta


def devuelve_lista_periodos(tipo, desde, hasta):
    """

    :param tipo: ['dias', 'semanas', 'meses', 'trimestres', 'anos']
    :param desde:
    :param hasta:
    :return:
    """
    l_tipos = ['dias', 'semanas', 'meses', 'trimestres', 'anos']
    if tipo not in l_tipos:
        raise ValueError('Tipo "%s" no valido. Tipos validos: "%s"' % (tipo, str(l_tipos)))
    desde = str_o_datetime_a_date(desde)
    hasta = str_o_datetime_a_date(hasta)
    if tipo in ['semanas', 'meses', 'trimestres']:
        if desde.year != hasta.year:
            raise ValueError('desde y hasta deben pertenecer al mismo año')
    #---- Empezamos los cálculos:
    l_datos = []
    actual = desde
    while actual <= hasta:
        if tipo == 'dias':
            l_datos.append(actual)
        elif tipo == 'semanas':
            l_datos.append(int(actual.strftime("%W")) + 1)
        elif tipo == 'meses':
            l_datos.append(actual.month)
        elif tipo == 'trimestres':
            if actual.month < 4:
                l_datos.append(1)
            elif actual.month < 7:
                l_datos.append(2)
            elif actual.month < 10:
                l_datos.append(3)
            else:
                l_datos.append(4)
        elif tipo == 'anos':
            l_datos.append(actual.year)
        actual = actual + datetime.timedelta(days=1)

    return sorted(list(set(l_datos)))


def devuelve_fechas_inicio_y_fin(periodo, ano=None):
    """
    devuelve: {'mes': (f_ini,f_fin)}
    """
    l_periodos = ['mes', 'trimestre', 'semana']
    if periodo not in l_periodos:
        raise ValueError('periodo "%s" no valido. Periodos válidos: %s' % (periodo, l_periodos))

    if ano is None:
        ano = datetime.datetime.now().year

    if periodo == 'semana':
        l_semanas = devuelve_semanas_aux(ano)
        l_datos = {}
        for semana in l_semanas.keys():
            l_datos[int(semana[-2:])] = l_semanas[semana]
        return l_datos

    # Else:
    desde = datetime.date(ano, 1, 1)
    hasta = datetime.date(ano, 12, 31)
    l_meses = {}
    for mes in range(1, 13):
        primer_dia = desde.day if mes == desde.month else 1
        if mes == hasta.month:
            ultimo_dia = hasta.day
        elif mes == 12:
            ultimo_dia = 31
        else:
            fecha = datetime.datetime(ano, mes + 1, 1) - datetime.timedelta(days=1)
            ultimo_dia = fecha.day
        l_meses[mes] = (datetime.date(ano, mes, primer_dia), datetime.date(ano, mes, ultimo_dia))
    if periodo == 'trimestre':
        l_trimestres = {
            1: (l_meses[1][0], l_meses[3][1]),
            2: (l_meses[4][0], l_meses[6][1]),
            3: (l_meses[7][0], l_meses[9][1]),
            4: (l_meses[10][0], l_meses[12][1]),
        }
        l_datos = l_trimestres
    elif periodo == 'mes':
        l_datos = l_meses

    return l_datos

def devuelve_codigo_semana(fecha):
    """
    Nos devuelve un str con la clave de la semana de esa fecha.
    por ejempo devuelve_semana(datetime.datetime(2014,1,8))=='2014-02'
    fecha.strftime("%Y-%W") devolveria '2014-01', las semanas empiezan en 00,
    y yo necesito que empiecen en 01.
    """
    semana = int(fecha.strftime("%W")) + 1

    return "%s-%02d" % (fecha.strftime("%Y"), semana)


def devuelve_codigos_semana(desde, hasta):
    """
    Devuelve una lista con los códigos de semana desde hasta fecha.
>>> devuelve_codigos_semana(datetime.datetime(2014,10,1),datetime.datetime(2014,10,30))
['2014-40', '2014-41', '2014-42', '2014-43', '2014-44']
    """
    if desde > hasta:
        raise ValueError("desde(%s) debe ser mayor o igual que hasta(%s)" % (desde, hasta))
    serie = []
    actual = desde
    while actual <= hasta:
        serie.append(devuelve_codigo_semana(actual))
        actual = actual + datetime.timedelta(days=1)
    return sorted(list(set(serie)))


def devuelve_fecha(codigo_semana, codigo_dia):
    """
    codigo_semana='2014-41'
    codigo_dia='mar' | codigo_dia='todos' --> Devuelve una lista
    Qué fecha fue el jueves de la semana 41 del 2014?
    devuelve_fecha('2014-41','jue')==datetime.date(2014, 10, 9)

    """
    try:
        ano, semana = codigo_semana.split('-')
        ano = int(ano)
        semana = int(semana)
        if semana < 1 or semana > 53:
            int('a')  # Para que salta una excepcion
    except:
        raise ValueError("Formato de semana incorrecto. Formato 'aaaa-ss', ss:1..53")

    if codigo_dia not in l_dias_lun_dom + ['todos']:
        raise ValueError("dia debe ser: %s" % l_dias_lun_dom + ['todos'])
    primer_dia_semana = devuelve_semanas(ano)[codigo_semana][0]
    if codigo_dia == 'todos':
        l_fechas = []
        for dias_desplazamiento in range(0, 7):
            l_fechas.append(primer_dia_semana + datetime.timedelta(days=dias_desplazamiento))
        return l_fechas
    else:
        dias_desplazamiento = {d: i for i, d in enumerate(l_dias_lun_dom)}[codigo_dia]
        fecha = primer_dia_semana + datetime.timedelta(days=dias_desplazamiento)
        return fecha


def devuelve_semanas(ano=None, para_form=False):
    """
    Wrapper de devuelve_semanas_aux para devolver 2 años de semanas
    en vez de uno.
    """
    if not ano:
        hoy = datetime.date.today()
        ano_actual = int(hoy.strftime("%Y"))
    else:
        ano_actual = int(ano)
    if not para_form:
        r = devuelve_semanas_aux(ano=ano_actual - 1, para_form=para_form)
        r.update(devuelve_semanas_aux(ano=ano_actual, para_form=para_form))
    else:
        r = devuelve_semanas_aux(ano=ano_actual - 1, para_form=para_form) + \
            devuelve_semanas_aux(ano=ano_actual, para_form=para_form)
    return r


def devuelve_semanas_aux(ano=None, para_form=False):
    """
    De momento desde, hasta no se utilizan

    Devuelve un dict con las semanas y sus fechas de lunes/domingo,
    o bien una lista para cargar como choice en el form.

{'2014-01': (datetime.date(2013, 12, 30), datetime.date(2014, 1, 5)),
 '2014-02': (datetime.date(2014, 1, 6), datetime.date(2014, 1, 12)),
  ...
 '2014-52': (datetime.date(2014, 12, 22), datetime.date(2014, 12, 28)),
 '2014-53': (datetime.date(2014, 12, 29), datetime.date(2015, 1, 4))}

 si para_form: (Los asteriscos separan los meses.

[('2014-01', '01 - 30/12/2013 al 05/01/2014'),
 ('*', ''),
 ('2014-02', '02 - 06/01/2014 al 12/01/2014'),
 ('2014-03', '03 - 13/01/2014 al 19/01/2014'),
 ('2014-04', '04 - 20/01/2014 al 26/01/2014'),
 ('2014-05', '05 - 27/01/2014 al 02/02/2014'),
 ('*', ''),
...
 ('2014-52', '52 - 22/12/2014 al 28/12/2014'),
 ('2014-53', '53 - 29/12/2014 al 04/01/2015')]

    """
    if not ano:
        hoy = datetime.date.today()
        ano_actual = int(hoy.strftime("%Y"))
    else:
        ano_actual = int(ano)
    primer_dia_del_ano = datetime.date(ano_actual, 1, 1)
    primer_dia_sem = primer_dia_del_ano - datetime.timedelta(days=primer_dia_del_ano.weekday())
    ultimo_dia_sem = primer_dia_sem + datetime.timedelta(days=6)
    semanas_ano = {}
    for sem in range(1, 54):
        semanas_ano['%s-%02d' % (ano_actual, sem)] = (primer_dia_sem, ultimo_dia_sem)
        primer_dia_sem = ultimo_dia_sem + datetime.timedelta(days=1)
        ultimo_dia_sem = primer_dia_sem + datetime.timedelta(days=6)
    if para_form:
        form_choices = []
        l_semanas_ordenada = sorted(semanas_ano.keys())
        mes_actual = semanas_ano[l_semanas_ordenada[0]][0].month
        for sem in sorted(semanas_ano.keys()):
            desde, hasta = semanas_ano[sem]
            mes = semanas_ano[sem][0].month
            if mes <> mes_actual:
                mes_actual = mes
                form_choices.append(('*', ''))

            txt = '%s - %s al %s' % (sem[-2:], desde.strftime('%d/%m/%Y'), hasta.strftime('%d/%m/%Y'))
            form_choices.append((sem, txt))
        return form_choices
    else:
        return semanas_ano


def ultimo_dia_mes(fecha):
    """
    Recibe una fecha y devuelve la fecha correspondiente
    al último día del mes de la fecha que se le envía.
    """
    mes = fecha.month
    anno = fecha.year
    if mes < 12:
        resultado = datetime.datetime(anno, mes + 1, 1) - datetime.timedelta(days=1)
    else:
        resultado = datetime.datetime(anno, 12, 31)

    return resultado.date()


def utc_a_localtz(utc_dt, str_timezone):
    """
    Convierte un datetime UTC a datetime TimeZone Local

    :param utc_dt: <utc datetime>
    :param str_timezone: 'Europe/Madrid' por ejemplo. En Django: settings.TIME_ZONE
    :return:
    """
    local_tz = pytz.timezone(str_timezone)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


def punto_fijo(importe,num_decimales=2):
    """
    Convierte un Decimal a un numero fijo de decimales.
    Por defecto:2.
    Sujeto a las restricciones del modulo 'decimal'.
    Siempre devuelve decimales:
    punto_fijo(80)=='80.00'
    punto_fijo(80,4)=='80.0000'

    Idea copiada de https://gist.github.com/jackiekazil/6201722
    2: Round decimal with super rounding powers

    from decimal import Decimal, ROUND_HALF_UP
    # Here are all your options for rounding:
    # This one offers the most out of the box control
    # ROUND_05UP       ROUND_DOWN       ROUND_HALF_DOWN  ROUND_HALF_UP
    # ROUND_CEILING    ROUND_FLOOR      ROUND_HALF_EVEN  ROUND_UP

    our_value = Decimal(16.0/7)
    output = Decimal(our_value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))

    print output
    """
    num_ceros = num_decimales - 1
    redondeo = "0" * num_ceros
    redondeo = ".%s1" % redondeo
    # print redondeo
    try:
        importe = Decimal(importe)
        resultado = Decimal(importe.quantize(Decimal(redondeo),rounding=ROUND_HALF_UP))
    except:
        resultado=None
    return resultado

def formularios_tienen_mismo_contenido(formulario1, formulario2):
    """
    Comprueba si el contenido de dos formularios es el mismo
    """
    try:
        formulario1.is_valid()
        datos1 = formulario1.cleaned_data
    except AttributeError:
        datos1 = None

    try:
        formulario2.is_valid()
        datos2 = formulario2.cleaned_data
    except AttributeError:
        datos2 = None

    iguales = (datos1 == datos2)
    print ">>>>>>> dict 1: "
    pprint.pprint(datos1)
    print ">>>>>>> dict 2: "
    pprint.pprint(datos2)
    print("Iguales:" ,iguales)
    return datos1 == datos2


def devuelve_Decimal_o_None(txt):
    """
    """
    try:
        valor=punto_fijo(txt)
    except:
        valor=None
#
#    print 'devuelve_Decimal_o_None(), IN:',txt,'type',type(txt),'OUT:',valor
    return valor

def decimal2str(numero):
    """
    Elimina los decimales si son 0.
    Por ejemplo Devuelve 3 si 3.0.
    Devuelve la entrada sin modificar si numero no es float o decimal 
    """
    resultado=None
    if isinstance(numero,decimal.Decimal) or isinstance(numero,float):
        p_entera=int(numero)
        p_decimal=int(str(numero % 1).replace('0.',''))
        if p_decimal==0:
            resultado=str(p_entera)
        else:
            resultado=str(numero).replace('.',',')  
#        print "He convertido"      
    else:
        resultado=numero
    
#    print "IN:",type(numero),numero,' OUT:',type(resultado),resultado
    return resultado


def numero_a_letras(d,moneda=False):
    """
    Modificación realizada por jrocamonde para que permita decimales,
    el programa original number_to_letter.to_word no lo permitía.
    """
    from number_to_letter import to_word
    try:
        numero=punto_fijo(d)
    except:
        raise ValueError("%s no es un numero válido" % d)
    
    p_entera=int(numero)
    p_decimal=int(str(numero % 1).replace('0.',''))
    num_entero=to_word(p_entera).strip() if p_entera <> 0 else 'Cero'
    num_decimal=to_word(p_decimal).strip() if p_decimal <> 0 else None
    v={'num_entero':num_entero,
       'num_decimal':num_decimal}
    v['moneda']='Euro' if p_entera==1 else 'Euros'
    v['centimo']='Céntimo' if p_decimal==1 else 'Céntimos'
    
    if moneda:
        if num_decimal:
            resultado="%(num_entero)s %(moneda)s con %(num_decimal)s %(centimo)s"
        else:
            resultado="%(num_entero)s %(moneda)s"
    else:
        if num_decimal:
            resultado="%(num_entero)s con %(num_decimal)s"
        else:
            resultado="%(num_entero)s"
        
    return resultado % v


def devuelve_lista_errores_formulario(formulario):
    """
    Recorre un formulario devolviendo los errores de verificacion
    por cada campo: formulario[campo].errors
    """
    l_errores=[]
    l_campos=sorted(formulario.fields.keys())
    for campo in l_campos:
        if formulario[campo].errors:
            l_errores.append('Campo: %s, Errores: %s' % (campo,str(formulario[campo].errors)))
    return l_errores

def convierte_formulario_a_sololectura(formulario,tipo_widget='disabled'):
    """
    Convierte todos los widgets de un formulario a readonly.
    ---> OJO CON EL WIDGET 'disabled', si está activado no envia los datos por POST !!!
    El tipo de widget puede ser 'disabled','readonly'
    """
    if tipo_widget not in ['disabled','readonly']:
        raise ValueError("tipo_widget debe ser 'disabled' o 'readonly'")
    
    for campo in sorted(formulario.fields.keys()):
        formulario.fields[campo].widget.attrs[tipo_widget] = True
#        
    print 'Formulario convertido a SoloLectura con widget %s' % tipo_widget
        

def cambia_formato_fecha(str_fecha, formato_in='%d/%m/%Y', formato_out='%Y-%m-%d'):
    """
    Cambia el formato de representacion de fecha de un string,
    pasándolo de formato_in a formato_out
>>> d=datetime.datetime.strptime('12/04/2014','%d/%m/%Y')
>>> d.strftime('%Y/%m/%d')
    """
    return datetime.datetime.strptime(str_fecha, formato_in).strftime(formato_out)
    
def codifica(objeto):
    """
    Serializa un objeto python, para enviarlo a través
    de peticiones HTTP.
    Serializa -> Comprime -> [encripta] ->base64 -> urlquote
    Pendiente de realizar la encriptacion.
    """
    cadena=pickle.dumps(objeto)
    cadena=zlib.compress(cadena)
    cadena=base64.b64encode(cadena)
    cadena=urllib.quote(cadena)
    return cadena

def descodifica(cadena):
    """
    Funcion inversa de codifica(),
    devuelve None si hubo algún error.
    """
    try:
        cadena=urllib.unquote(cadena)
        cadena=base64.b64decode(cadena)
        cadena=zlib.decompress(cadena)
        objeto=pickle.loads(cadena)
    except:
        objeto=None
    return objeto
    

def formatea_moneda(valor, fuerza2decimales=True, none_a_blanco=False):
    """
    1234567.89 -> 1.234.567,89
    """
    if valor in ['',None]:
        if none_a_blanco:
            return ''
        else:
            return valor
        
    valor=str(valor)
    if valor[0]=='-':
        negativo=True
        valor=valor[1:]
    else:
        negativo=False 
    try:
        parte_decimal=valor.split('.')[1][:2]
        if fuerza2decimales:
            if len(parte_decimal) == 1:
                parte_decimal += '0'
        pe=valor.split('.')[0][::-1] #7654321        
    except:
        pe=valor[::-1]
        if fuerza2decimales:
            parte_decimal = '00'
        else:
            parte_decimal=None
    l=[(0,3), (3,6), (6,9), (9,12)]
    v=''
    for i,j in l:
        v+=pe[i:j]+'.'
    v=v[::-1]
    if parte_decimal:
        v=v+','+parte_decimal
    v=v.replace('....','').replace('...','').replace('..','')
    if v[0]=='.':
        v=v[1:]
    if negativo:
        v='-'+v

    return v

def formatea_fecha(fecha):
    """
    """
    if not fecha:
        return ''
    return fecha.strftime('%d/%m/%Y')

    
def b64_a_objeto(b64_str, urlquote=False):
    """
    Recibe string en texto plano y base 64, y devuelve un objeto Python.
    """
    if urlquote:
        cadena = urllib.unquote(b64_str)
    else:
        cadena = b64_str
    cadena = base64.b64decode(cadena)
    objeto = pickle.loads(cadena)

    return objeto
    # return(pickle.loads(base64.b64decode(b64_str)))

def objeto_a_b64(obj, urlquote=False):
    """
    Recibe un objeto Python y lo devuelve serializado en texto plano y base 64.
    """
    cadena = pickle.dumps(obj,2)
    cadena=base64.b64encode(cadena)
    if urlquote:
        cadena=urllib.quote(cadena)

    return cadena
    # return(base64.b64encode(pickle.dumps(obj,2)))


def str_o_datetime_a_date(fecha_in):
    """
    Recibe un datetime.date, un datetime.datetime ou un txt con formato
    aaaa/mm/dd, aaaa-mm-dd, dd/mm/aaaa, dd-mm-aaaa y devuelve un datetime.date

    Funcion util para no preocuparse de comprobar el formato de entrada de una fecha.
    :return: datetime.date
    """
    if isinstance(fecha_in, str) or isinstance(fecha_in, unicode):
        fecha_in = fecha_in.strip().replace('-', '/')
        try:
            # Para las fechas en formato dd/mm/aa:
            if len(fecha_in) == 8:
                dia, mes, ano = fecha_in.split('/')
                fecha_in = "%s/%s/20%s" % (dia, mes, ano)
            fecha_in = datetime.datetime.strptime(fecha_in, "%Y/%m/%d")
        except ValueError:
            try:
                fecha_in = datetime.datetime.strptime(fecha_in, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Formatos fecha string validos: aaaa/mm/dd, aaaa-mm-dd, dd/mm/[aa]aa, dd-mm-[aa]aa")
        fecha_in = datetime.date(fecha_in.year, fecha_in.month, fecha_in.day)
    elif isinstance(fecha_in, datetime.datetime):
        fecha_in = datetime.date(fecha_in.year, fecha_in.month, fecha_in.day)
    elif isinstance(fecha_in, datetime.date):
        pass
    else:
        raise ValueError("fecha_in: %s (%s) no valida. Formatos validos: string, datetime.date y datetime.datetime"
                         % (fecha_in, type(fecha_in)))

    return fecha_in

def str_o_datetime_a_datetime(fecha_in):
    """
    Recibe un datetime.date, un datetime.datetime ou un txt con formato
    aaaa/mm/dd, aaaa-mm-dd, dd/mm/aaaa, dd-mm-aaaa y devuelve un datetime.date

    Funcion util para no preocuparse de comprobar el formato de entrada de una fecha.
    :return: datetime.date
    """
    if isinstance(fecha_in, str):
        fecha_in = fecha_in.replace('-', '/')
        try:
            fecha_in = datetime.datetime.strptime(fecha_in, "%Y/%m/%d %H:%M")
        except ValueError:
            try:
                fecha_in = datetime.datetime.strptime(fecha_in, "%d/%m/%Y %H:%M")
            except ValueError:
                raise ValueError("Formatos fecha string validos: aaaa/mm/dd hh:mm, aaaa-mm-dd hh:mm, dd/mm/aaaa hh:mm, dd-mm-aaaa hh:mm")
        #fecha_in = datetime.date(fecha_in.year, fecha_in.month, fecha_in.day)
    elif isinstance(fecha_in, datetime.datetime):
        #fecha_in = datetime.date(fecha_in.year, fecha_in.month, fecha_in.day)
        pass
    elif isinstance(fecha_in, datetime.date):
        pass
    else:
        raise ValueError("fecha_in: %s (%s) no valida. Formatos validos: string, datetime.date y datetime.datetime"
                         % (fecha_in, type(fecha_in)))

    return fecha_in

def ConectaPostgreSQL():
    """
    Devuelve un objeto psycopg2._psycopg.connection con la conexion directa
    a la BD de Django.

    """
    host = settings.DATABASES['default']['HOST']
    user = settings.DATABASES['default']['USER']
    passwd = settings.DATABASES['default']['PASSWORD']
    db = settings.DATABASES['default']['NAME']
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        pg_conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (host, db, user, passwd)
    else:
        raise ValueError("Motor de BD no soportado: %s" % settings.DATABASES['default']['ENGINE'])

    dbconn = psycopg2.connect(pg_conn_string)
    dbconn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    return dbconn

def id2cod(i):
    """
    Convierte i en un string encriptado. Se usa en los modelos, para
    evitar el webscraping por ids correlativos.
    :param i:
    :return:
    """
    return Encripta(i, contrasena='', urlquote=True)

def cod2id(cod):
    """
    Funcion inversa de id2cod
    :param cod:
    :return:
    """
    return Desencripta(cod, contrasena='', urlquote=True)

