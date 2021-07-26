#!/usr/bin/env python
# -*- coding: utf8 -*- 
"""
  Script que recorre todas nuestras apps, abre el fichero models.py
  y extrae los nombres de las clases para permitir el acceso a los datos
  que contienen desde el área reservada de Django.
"""
import os
import sys
nombre_proyecto = os.path.split(os.getcwd())[-1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", nombre_proyecto+".settings")
from django.conf import settings


#l_apps=['alumnos', 'csb19', 'filemaker']
# Asumimos que nuestras aplicaciones no empiezan por 'django.'
l_apps = [a for a in settings.INSTALLED_APPS if not a.startswith('django.')]

print l_apps

base_path=os.getcwd()


def crea_adminpy(base_path,nombre_app):
    """
    Abre el fichero models.py, extrae los nombres de clases y
    crea la linea admin.site.register(nombre_clase)
    """
    base_clase='%s.models' % nombre_app
    f_out_filename=os.path.join(base_path,nombre_app,'admin.py')
    f_out=open(f_out_filename,'w')
    l_clases=[]
    for linea in open(os.path.join(base_path,nombre_app,'models.py'),'r').readlines():
        if linea.startswith('class '):
            nombre_clase=linea.split()[1].split('(')[0]
            l_clases.append(nombre_clase)

    f_out.write("""# -*- coding: utf8 -*-\n
# Fichero creado automaticamente con crea_adminpy.py

from django.contrib import admin\n""")
    if l_clases == []:
        print "  Warning: No se han encontrado clases en el fichero models.py"
        f_out.write('# No se han encontrado clases en el fichero models.py\n')
    else:
        print "  Clases: %s" % repr(l_clases)
        f_out.write("from %s import %s\n\n" % (base_clase,', '.join(l_clases)))
        for nombre_clase in l_clases:
                f_out.write('admin.site.register(%s)\n' % nombre_clase)
    f_out.write('\n\n')
    f_out.close()
    print "  Grabado: ",f_out_filename
    
if __name__ == '__main__':
    for nombre_app in sorted(l_apps):
        print "Pocesando %s ..." % nombre_app
        try:
            crea_adminpy(base_path, nombre_app)
        except:
            print " ---> ERROR creando admin.py del app: %s" % nombre_app
