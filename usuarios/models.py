# -*- coding: utf8 -*-
from django.db import models
from django.db import IntegrityError
from django.utils import encoding
from django.conf import settings
from django.contrib.auth.models import User

import tlalogger

from fmaestros import models as fmaestros_models
from fmaestros.models import Provincia
from tgas.base36crypt import genera_password


# -----------------------------


# class Grupo(models.Model):
#     """
#     Los grupos se utilizan para los permisos, para los menús y para los informes.
#     El usuario debe pertenecer al menos a un grupo, aunque puede pertenecer a varios a la vez.
#
#     La prioridad tiene que ser única, dos grupos no pueden tener la misma, porque
#     los informes, menús (y permisos en algunos casos) se cogerán en función de la prioridad.
#     0 es la mínima prioridad.
#     Ejemplo:
#        100 Administrador Informático
#         60 Gerente
#         50 Jefe Explotacion
#         40 Delegado
#         30 Administrativo
#         20 Recaudador
#         10 Técnico
#     """
#     nombre = models.CharField(max_length=30, unique=True)
#     descripcion = models.CharField(max_length=128, null=True, blank=True, default=None)
#     prioridad = models.PositiveSmallIntegerField(unique=True)
#
#     class Meta:
#         ordering = ('prioridad', )
#
#     def __str__(self):
#         dato="%s (%s)" % (self.nombre, self.prioridad)
#         return encoding.smart_str(dato, encoding='utf8', errors='ignore')


class Usuario(models.Model):
    """
    Algunos campos estan duplicados, guardando la informacion en
    django.contrib.auth.model.User y aqui.
    """
    # Para enlazar Usuario con los User de Django:
    dj_user = models.OneToOneField(User)
    # Campos comunes a  django.contrib.auth.model.User
    username = models.CharField(max_length=30, unique=True)  # username
    password = models.CharField(max_length=128)  # password
    nombre = models.CharField(max_length=30, null=True, blank=True, default=None)  # first_name
    apellidos = models.CharField(max_length=60, null=True, blank=True, default=None)  # last_name (0..30)
    email = models.CharField(max_length=75, null=True, blank=True, default=None)  # email
    esta_activo = models.BooleanField(default=True)  # is_active
    ultimo_acceso_correcto = models.DateTimeField(null=True, blank=True,
                                                  default=None)  # last_login                              # date_joined
    # Otros campos
    nif = models.CharField(max_length=15, unique=True)
    observaciones = models.CharField(max_length=128, null=True, blank=True, default=None)
    ultimo_acceso_incorrecto = models.DateTimeField(null=True, blank=True, default=None)
    accesos_correctos = models.PositiveSmallIntegerField(default=0)
    accesos_incorrectos = models.PositiveSmallIntegerField(default=0)
    fecha_baja = models.DateField(null=True, blank=True)

    es_admin = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

    # campos propios de tgas
    factura_mensual = models.BooleanField(default=True)
    codigo_postal = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    provincia = models.ForeignKey(Provincia)
    localidad = models.CharField(max_length=30, null=True, blank=True, default=None)
    direccion = models.CharField(max_length=60, null=True, blank=True, default=None)
    telefono = models.CharField(max_length=15, blank=True, unique=True, null=True)

    class Meta:
        verbose_name_plural = "Usuarios"

        indexes = [
            models.Index(['username']),
            models.Index(['es_admin']),
            models.Index(['fecha_paso_historico']),
        ]

    def __str__(self):
        # dato="%s (%s %s)" % (self.username, self.nombre, self.apellidos)
        dato = "%s %s" % (self.nombre, self.apellidos)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')

    # def __init__(self, username, password, *args, **kwargs):
    #     super(Usuario, self).__init__(*args, **kwargs)
    #     # Para crear un nuevo usuario, es imprescindible username y password
    #     self.username = username
    #     self.password = password
    #     print(self.username, username)
    #     print(self.password,password)

    # Sobreescribo el metodo save() para que cuando se guarde un usuario actualize
    # los datos de django.contrib.auth.model.User o lo cree si no existe.
    def save(self, *args, **kwargs):
        logger = tlalogger.dj_mylogger(__file__)
        if (self.username is None) or (self.username == ''):
            raise ValueError('Es necesario establecer "username" antes de .save()')
        elif(self.password is None) or (self.password == ''):
            self.password = genera_password(self.username)

        # No tiene asignado ningún usuario Django:
        print "Usuario.save(). Valor de self.dj_user_id: %s" % repr(self.dj_user_id)
        if self.dj_user_id is None:
            usuario_django = User.objects.filter(username=self.username).first()
            if usuario_django is None:
                # Creamos un usuario nuevo de Django.
                self.dj_user = User()
            else:
                # O utilizamos el usuario Django cuyo username ya existia
                self.dj_user = usuario_django

        # Los atributos username, first_name, last_name y email
        # son obligatorios.

        self.dj_user.username = self.username
        self.dj_user.first_name = self.nombre if self.nombre else u''
        self.dj_user.last_name = self.apellidos if self.apellidos else u''
        self.dj_user.email = self.email if self.email else u''

        self.dj_user.is_active = self.esta_activo
        self.dj_user.is_staff = False
        self.dj_user.is_super = False
        # El pass se copia encriptado de usuario_django, si lo modificamos a través
        # de usuario ni debería empezar por pbk...$ ni ser mayor de 50 caracteres
        if not (self.password.startswith('pbkdf2_sha256$') and (len(self.password) > 50)):
            self.dj_user.set_password(self.password)
        self.dj_user.save()
        self.dj_user_id = self.dj_user.id
        print "self.dj_user.save() OK"

        self.password = self.dj_user.password  # Se guarda cifrado en django y se copia cifrado para aquí
        self.ultimo_acceso_correcto = self.dj_user.last_login
        # Save original:
        super(Usuario, self).save(*args, **kwargs)
        # try:
        #     super(Usuario, self).save(*args, **kwargs)
        # except IntegrityError:
        #     raise ValueError('Ya existe el usuario "%s". No se puede crear de nuevo.' % self.username)

    def matriculas(self):
        """Devuelve las matriculas pertenecientes al usuario en forma de str"""

        return ', '.join([matricula.codigo for matricula in self.matricula_set.all()])

    def facturacion(self):
        """Devuelve el tipo de facturacion"""

        return 'mensual' if self.factura_mensual else 'por suministro'


class Matricula(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=16, unique=True)
    usuario = models.ForeignKey(Usuario)

    class Meta:
        verbose_name_plural = "Matriculas"
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        return encoding.smart_str(self.codigo, encoding='utf8', errors='ignore')


class LogAcceso(models.Model):
    fecha_hora = models.DateTimeField(null=False)
    username = models.CharField(max_length=30, null=False)
    ip = models.GenericIPAddressField()
    correcto = models.BooleanField(default=False)
    comentario = models.CharField(max_length=32, null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "Logs de Acceso por Login"

    def __str__(self):
        dato = "%s (%s)" % (self.username, self.ip)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')


class IPPermitida(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    descripcion = models.CharField(max_length=30, null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "IPs Permitidas para Login"

    def __str__(self):
        dato = '[%s] %s' % (self.ip, self.descripcion,)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')


def resetea_passwords_salvo_admin():
    """
    Genera de nuevo los passwords de todos los usuarios salvo los que son admin.
    :return: lista de usernames modificados
    """
    l_reseteados = []
    for usuario_a_modif in Usuario.objects.filter(es_admin=False):
        password = genera_password(usuario_a_modif.username)
        usuario_a_modif.password = password
        usuario_a_modif.save()
        print("Reseteando password de %s" % usuario_a_modif.username)
        l_reseteados.append(usuario_a_modif.username)
    return l_reseteados

# from usuarios import models
# l = models.resetea_passwords_salvo_admin()
