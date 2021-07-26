# -*- coding: utf8 -*-
"""
    Utilidades basadas en Google Maps.
"""

from decimal import Decimal

def l_posiciones2markers(l_posiciones):
    """
    Convierte una lista de dicts con marcadores en el codigo javascript
    para incrustarlo en la página HTML
    :param l_posiciones:
    l_posiciones = [
        {'pos': (42.15259833, -8.82684833),
         'icon': 'verde',
         'title': 'Hola'},
        {'pos': (42.17027333, -8.67606),
         'icon': 'rojo',
         'title': 'Que Tal'},
    ]

    :return:
    txt = \"\"\"
            {  position: [42.15259833, -8.82684833],
               icon: "https://maps.google.com/mapfiles/marker_green.png",
               title: "Hola"  },
            {  position: [42.17027333, -8.67606],
               icon: "https://maps.google.com/mapfiles/marker.png",
               title: "Que Tal"  },
    \"\"\"
    """

    jstxt = ''
    for p in l_posiciones:
        jstxt += '         {  position: [%s, %s],\n' % p['pos']
        jstxt += '            title: "%s",\n' % p['title']
        if p['icon'] == 'verde':
            jstxt += '            icon: "https://maps.google.com/mapfiles/marker_green.png"},\n'
        elif p['icon'] == 'rojo':
            jstxt += '            icon: "https://maps.google.com/mapfiles/marker.png"},\n'

    return jstxt


def centro(l_posiciones):
    """
    A partir de la lista de coordenadas GPS que viene dentro de l_posiciones,
    devuelve las coordenadas para centrar Google Maps.
    :param l_posiciones:
    :return:
    """
    l_lat = []
    l_lon = []
    for d in l_posiciones:
        if d['pos'][0] is not None:
            l_lat.append(d['pos'][0])
        if d['pos'][1] is not None:
            l_lon.append(d['pos'][1])
    l_lat.sort()
    l_lon.sort()
    # diferencia_longitudes = ultima_ordenada - primera_ordenada
    # latitude_medio = primera_ordenada - (diferencia_latitudes / 2)
    lat_mid = (l_lat[-1] + l_lat[0]) / Decimal(2)
    lon_mid = (l_lon[-1] + l_lon[0]) / Decimal(2)
    return lat_mid, lon_mid


def pinta_markers(l_posiciones, zoom=8, mapa_ancho=1400, mapa_alto=900, center_coords=None):
    """
    Devuelve el codigo HTML para embeber en modo |safe en Django con el
    mapa y los markers.

    :param l_posiciones:
    :param zoom:
    :param mapa_ancho:
    :param mapa_alto:
    :return:
    """
    # l_posiciones = [
    #     {'pos': (42.15259833, -8.82684833),
    #      'icon': 'verde',
    #      'title': 'Hola'},
    #     {'pos': (42.17027333, -8.67606),
    #      'icon': 'rojo',
    #      'title': 'Que Tal'},
    # ]

    if center_coords is None:
        center_coords = "[%s, %s]" % centro(l_posiciones)

    html = """
    <script src="https://maps.google.com/maps/api/js?key=AIzaSyB36L8WcnpDaVjZNm-dGcHA6ytPqKGkQUA"></script>
    <script src="https://cdn.jsdelivr.net/gmap3/7.2.0/gmap3.min.js"></script>
    <style>
    .gmap3{
      margin: 20px auto;
      border: 1px dashed #C0C0C0;
      max-width:  %(mapa_ancho)spx;
      height: %(mapa_alto)spx;
      display: block;
    }
    </style>
    <script>
    var lineSymbol = {
      path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
    };

      $(function () {
        $('#test')
          .gmap3({
            zoom: %(zoom)s,
            center: %(center_coords)s
          })
          .marker([      
          %(l_markers)s    
          ])
        ;
      });
    </script>
    <div id="test" class="gmap3"></div>
    """
    d = {
        'mapa_ancho': mapa_ancho,
        'mapa_alto': mapa_alto,
        'zoom': zoom,
        'center_coords':center_coords,
        'l_markers': l_posiciones2markers(l_posiciones),
    }
    return html % d


def pinta_camino(origen, destino, zoom=8, mapa_ancho=1400, mapa_alto=900):
    """
    Devuelve el codigo HTML para embeber en modo |safe en Django con el
    mapa.

    :param origen:
    :param destino:
    :param zoom:
    :param mapa_ancho:
    :param mapa_alto:
    :return:
    """
    # origen = (42.15259833, -8.82684833)
    # destino = (42.17027333, -8.67606)

    lat_mid = (origen[0] + destino[0]) / Decimal(2)
    lon_mid = (origen[1] + destino[1]) / Decimal(2)

    center_coords = "[%s, %s]" % (lat_mid, lon_mid)

    print origen
    print destino
    print center_coords

    html = """
    <script src="https://maps.google.com/maps/api/js?key=AIzaSyB36L8WcnpDaVjZNm-dGcHA6ytPqKGkQUA"></script>
    <script src="https://cdn.jsdelivr.net/gmap3/7.2.0/gmap3.min.js"></script>
    <style>
    .gmap3{
      margin: 20px auto;
      border: 1px dashed #C0C0C0;
      max-width:  %(mapa_ancho)spx;
      height: %(mapa_alto)spx;
      display: block;
    }
    </style>
    <script>
    var lineSymbol = {
      path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
    };

      $(function () {
        $('#test')
          .gmap3({
            zoom: %(zoom)s,
            center: %(center_coords)s
          })
          .route({
        origin: %(origen)s,
        destination: %(destino)s,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
      })
      .directionsrenderer(function (results) {
        if (results) {
          return {
            panel: "#box",
            directions: results
          }
        }
      });
      });
    </script>
    <div id="test" class="gmap3"></div>
    """
    d = {
        'mapa_ancho': mapa_ancho,
        'mapa_alto': mapa_alto,
        'zoom': zoom,
        'center_coords':center_coords,
        'origen': "[%s, %s]" % origen,
        'destino': "[%s, %s]" % destino,
    }
    return html % d
