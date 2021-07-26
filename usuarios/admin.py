# -*- coding: utf8 -*-

# Fichero creado automaticamente con crea_adminpy.py

from django.contrib import admin
from usuarios.models import Usuario, LogAcceso, IPPermitida

admin.site.register(Usuario)
admin.site.register(LogAcceso)
admin.site.register(IPPermitida)


