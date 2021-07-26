# -*- coding: utf8 -*-
"""
  Inserta CCAAs, Provinicias y Poblaciones.
  Orden:
>>> from docs import inserta_provincias as ip
>>> ip.inserta_ccaa()
>>> ip.inserta_prov()

"""
from fmaestros.models import ComunidadAutonoma, Provincia

# ------------------------------------------------------------------------------------------------
txt_ccaas = """01; AN ;   Andalucía
02; AR ;   Aragón
03; AS ;   Asturias, Principado de
04; IB ;   Balears, Islas
05; CN ;   Canarias
06; CB ;   Cantabria
07; CL ;   Castilla y León
08; CM ;   Castilla - La Mancha
09; CT ;   Cataluña
10; VC ;   Comunidad Valenciana
11; EX ;   Extremadura
12; GA ;   Galicia
13; MD ;   Madrid, Comunidad de
14; MC ;   Murcia, Región de
15; NC ;   Navarra, Comunidad Foral de
16; PV ;   País Vasco
17; RI ;   Rioja, La
18; CE ;   Ceuta
19; ML ;   Melilla"""
# ------------------------------------------------------------------------------------------------

txt_provs = """01  ;  Álava  ;  PV  ;  Pais Vasco
02  ;  Albacete  ;  CM  ;  Castilla La Mancha
03  ;  Alicante  ;  VC  ;  Valencia
04  ;  Almería  ;  AN  ;  Andalucía
05  ;  Ávila  ;  CL  ;  Castilla León
06  ;  Badajoz  ;  EX  ;  Extremadura
07  ;  Baleares  ;  IB  ;  Baleares
08  ;  Barcelona  ;  CT  ;  Cataluña
09  ;  Burgos  ;  CL  ;  Castilla León
10  ;  Cáceres  ;  EX  ;  Extremadura
11  ;  Cádiz  ;  AN  ;  Andalucía
12  ;  Castellón  ;  VC  ;  Valencia
13  ;  Ciudad Real  ;  CM  ;  Castilla La Mancha
14  ;  Córdoba  ;  AN  ;  Andalucía
15  ;  La Coruña  ;  GA  ;  Galicia
16  ;  Cuenca  ;  CM  ;  Castilla La Mancha
17  ;  Gerona  ;  CT  ;  Cataluña
18  ;  Granada  ;  AN  ;  Andalucía
19  ;  Guadalajara  ;  CM  ;  Castilla La Mancha
20  ;  Guipúzcoa  ;  PV  ;  Pais Vasco
21  ;  Huelva  ;  AN  ;  Andalucía
22  ;  Huesca  ;  AR  ;  Aragón
23  ;  Jaén  ;  AN  ;  Andalucía
24  ;  León  ;  CL  ;  Castilla León
25  ;  Lérida  ;  CT  ;  Cataluña
26  ;  La Rioja  ;  RI  ;  La Rioja
27  ;  Lugo  ;  GA  ;  Galicia
28  ;  Madrid  ;  MD  ;  Madrid
29  ;  Málaga  ;  AN  ;  Andalucía
30  ;  Murcia  ;  MC  ;  Murcia
31  ;  Navarra  ;  NC  ;  Navarra
32  ;  Ourense  ;  GA  ;  Galicia
33  ;  Asturias  ;  AS  ;  Asturias
34  ;  Palencia  ;  CL  ;  Castilla León
35  ;  Las Palmas  ;  CN  ;  Canarias
36  ;  Pontevedra  ;  GA  ;  Galicia
37  ;  Salamanca  ;  CL  ;  Castilla León
38  ;  Santa Cruz de Tenerife  ;  CN  ;  Canarias
39  ;  Cantabria  ;  CB  ;  Cantabria
40  ;  Segovia  ;  CL  ;  Castilla León
41  ;  Sevilla  ;  AN  ;  Andalucía
42  ;  Soria  ;  CL  ;  Castilla León
43  ;  Tarragona  ;  CT  ;  Cataluña
44  ;  Teruel  ;  AR  ;  Aragón
45  ;  Toledo  ;  CM  ;  Castilla La Mancha
46  ;  Valencia  ;  VC  ;  Valencia
47  ;  Valladolid  ;  CL  ;  Castilla León
48  ;  Vizcaya  ;  PV  ;  Pais Vasco
49  ;  Zamora  ;  CL  ;  Castilla León
50  ;  Zaragoza  ;  AR  ;  Aragón
51  ;  Ceuta  ;  CE  ;  Ceuta y Melilla
52  ;  Melilla  ;  ML  ;  Ceuta y Melilla"""


# ------------------------------------------------------------------------------------------------


def inserta_ccaa(txt=txt_ccaas, borrar_actuales=False):
    """
    """
    if borrar_actuales:
        ComunidadAutonoma.objects.all().delete()

    l_ok = []
    l_nok = []

    l_ccaas = txt.split('\n')
    for linea in l_ccaas:
        try:
            dato = linea.split(';')
            #             print dato
            #             codigo, codigo_iso, nombre = dato[0], dato[1]
            C = ComunidadAutonoma(codigo=dato[0].strip(),
                                  codigo_iso=dato[1].strip(),
                                  nombre=dato[2].strip())
            C.save()
            l_ok.append((C.nombre, C.id,))
        except Exception as e:
            l_nok.append((linea, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}


def inserta_prov(txt=txt_provs, borrar_actuales=False):
    """
    """
    if borrar_actuales:
        Provincia.objects.all().delete()

    l_ok = []
    l_nok = []

    l_provs = txt.split('\n')
    for linea in l_provs:
        try:
            dato = linea.split(';')
            # print dato
            # print dato[2].strip()
            ccaa = ComunidadAutonoma.objects.filter(codigo_iso=dato[2].strip())[0]
            print dato
            P = Provincia(codigo=dato[0].strip(),
                          nombre=dato[1].strip(),
                          ccaa=ccaa)
            P.save()
            print "Insertado: ", dato[1].strip()
            l_ok.append((P.nombre, P.id,))
        except Exception as e:
            l_nok.append((linea, e,))

    return {'l_nok': l_nok, 'l_ok': l_ok}
