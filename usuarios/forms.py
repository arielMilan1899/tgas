# -*- coding: utf8 -*-

import regex
from django import forms
from django.core.exceptions import ValidationError
from django.db.transaction import atomic

from models import Usuario, Matricula  # ,EmpresaOperadora, Delegacion

# class EmpresaOperadoraForm(forms.ModelForm):
#     """
#     """
#     # codigo_interno = forms.CharField(max_length=36, required=True)
#     class Meta:
#         model = EmpresaOperadora
#         localized_fields = '__all__'
#         exclude = ()
#
#     def validate_unique(self):
#         exclude = self._get_validation_exclusions()
#         try:
#             self.instance.validate_unique(exclude=exclude)
#         except forms.ValidationError as e:
#             try:
#                 del e.error_dict['nombre']  #if field1 unique validation occurs it will be omitted and form.is_valid() method pass
#             except:
#                 pass
#             self._update_errors(e) #if there are other errors in the form those will be returned to views and is_valid() method will fail.
#
#
# class DelegacionForm(forms.ModelForm):
#     """
#     """
#     # codigo_interno = forms.CharField(max_length=36, required=True)
#     class Meta:
#         model = Delegacion
#         localized_fields = '__all__'
#         exclude = ()
#
#     def validate_unique(self):
#         exclude = self._get_validation_exclusions()
#         try:
#             self.instance.validate_unique(exclude=exclude)
#         except forms.ValidationError as e:
#             try:
#                 del e.error_dict['nombre']  #if field1 unique validation occurs it will be omitted and form.is_valid() method pass
#             except:
#                 pass
#             self._update_errors(e) #if there are other errors in the form those will be returned to views and is_valid() method will fail.
from usuarios.validador import Validador

"""
    dj_user = models.OneToOneField(User)
    # Campos comunes a  django.contrib.auth.model.User
    username = models.CharField(max_length=30, unique=True)        # username
    password = models.CharField(max_length=128)                    # password
    nombre = models.CharField(max_length=30, null=True, blank=True, default=None)                       # first_name
    apellidos = models.CharField(max_length=60, null=True, blank=True, default=None)                    # last_name (0..30)
    email = models.CharField(max_length=75, null=True, blank=True, default=None)                        # email
    esta_activo = models.BooleanField(default=True)                # is_active
    ultimo_acceso_correcto = models.DateTimeField(null=True, blank=True, default=None) #last_login                              # date_joined
    # Otros campos
    nif = models.CharField(max_length=15, null=True, blank=True, default=None, unique=True)
    observaciones = models.CharField(max_length=128, null=True, blank=True, default=None)
    ultimo_acceso_incorrecto = models.DateTimeField(null=True, blank=True, default=None)
    accesos_correctos = models.PositiveSmallIntegerField(default=0)
    accesos_incorrectos = models.PositiveSmallIntegerField(default=0)
    fecha_baja = models.DateField(null=True, blank=True)
    # Relacionado con los permisos
    # Si el titular es None, el usuario es "Superusuario", es decir,
    # pertenece a la operadora y lleva un menu distinto.
    titular = models.ForeignKey(fmaestros_models.Titular, null=True, blank=True)
    # El usuario debe pertenecer al menos a un grupo
    grupo = models.ManyToManyField(Grupo)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)

"""


class UsuarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(UsuarioForm, self).__init__(*args, **kwargs)

        #Veamos todas las matriculas asociadas
        matriculas = Matricula.objects.filter(usuario_id=self.instance.id)
        #Agregamos esos campos dinamicamente al form como matriculas editables
        for i in range(len(matriculas)):
            field_name = 'matricula_editable_%s' % (matriculas[i].codigo,)
            self.fields[field_name] = forms.CharField(max_length=30, required=False,
                                      widget=forms.TextInput(attrs={'size': 30, 'placeholder': "Matricula previa: %s" %matriculas[i].codigo, 'class': "matricula_input"}))
            try:
                self.initial[field_name] = matriculas[i].codigo
            except:
                self.initial[field_name] = ""
        #Si se trata de un request.POST    
        if(self.data):
            i = 0
            field_name = 'nueva_matricula_%s' %(i,)
            while field_name in self.data.keys():
                #Al crear el form, se ingresan todos los campos dinámicos creados por el usuario para devolver el mismo form
                #Recordemos que no sabemos cuantos campos dinamicos ha creado el usuario
                self.fields[field_name] = forms.CharField(max_length=30, required=False,
                                   widget=forms.TextInput(attrs={'size': 30, 'placeholder':  'Agregar matrícula.', 'class': "matricula_input"}))
                self.initial[field_name] = self.data[field_name]
                i += 1
                field_name = 'nueva_matricula_%s' %(i,)
            #Sobrescribimos la ultima para agregar la clase matricula_input_new
            self.fields["nueva_matricula_%s" %(i-1)] = forms.CharField(max_length=30, required=False,
                                  widget=forms.TextInput(attrs={'size': 30, 'placeholder':  'Agregar matrícula.', 'class': "matricula_input matricula_input_new"}))
        #En caso contrario, se trata de un GET y devolvemos el form normal
        else:
            field_name = "nueva_matricula_0"
            self.fields[field_name] = forms.CharField(max_length=30, required=False,
                                   widget=forms.TextInput(attrs={'size': 30, 'placeholder':  'Agregar matrícula.', 'class': "matricula_input matricula_input_new"}))

    class Meta:
        model = Usuario
        localized_fields = '__all__'
        # fields = ('username', 'nombre', 'apellidos', 'titular', 'fecha_paso_historico', 'observaciones')
        exclude = ('accesos_correctos', 'password', 'dj_user', 'accesos_incorrectos', 'grupo',)
        # exclude = ('fecha_creacion', 'fecha_modificacion', 'fecha_paso_historico')
        widgets = {
            'observaciones': forms.Textarea(attrs={
                'class': 'observaciones',
                'rows': 4,
                'cols': 40,
                'autocorrect': "off",
                'autocapitalize': "off",
                'spellcheck': "false"}),
            'username': forms.TextInput(attrs={'size': 16}),
            'nombre': forms.TextInput(attrs={'size': 16}),
            'nif': forms.TextInput(attrs={'size': 16}),
            'apellidos': forms.TextInput(attrs={'size': 30}),
            'email': forms.TextInput(attrs={'size': 30}),
            'localidad': forms.TextInput(attrs={'size': 16}),
            'direccion': forms.Textarea(attrs={
                'class': 'observaciones',
                'rows': 4,
                'cols': 40,
                'autocorrect': "off",
                'autocapitalize': "off",
                'spellcheck': "false"}),
            'codigo_postal': forms.TextInput(attrs={'size': 10}),
        }

   
    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(UsuarioForm, self).validate_unique(*args, **kwargs)
        else:
            exclude = self._get_validation_exclusions()
            try:
                self.instance.validate_unique(exclude=exclude)
            except forms.ValidationError as e:
                try:
                    del e.error_dict['username']
                except:
                    pass
                self._update_errors(e)

    def clean_nif(self):

        nif = self.cleaned_data['nif']
        if not Validador().validar(nif):
            raise ValidationError('NIF es incorrecto.')

        return nif

    def clean(self):
        #Obtenemos todas las posibles matriculas editables del usuario
        editables = Matricula.objects.filter(usuario_id = self.instance.id)
        
        matriculas_editables = []
        matriculas = set()
        #Inicializamos el valord el primer campo en nueva_matricula_0
        i = 0
        field_name = 'nueva_matricula_%s' %(i,)
        #Buscamos en orden, mientras la clave se encuentre en el diccionario del POST
        while field_name in self.data.keys():
            if self.data.get(field_name):
                matricula = self.data[field_name]

                text = regex.sub(r'[^0-9\p{L}]', ' ', matricula.decode('ASCII'))
                text = regex.sub(r'\s\s+', ' ', text)
                # remove spaces between numbers
                text = regex.sub(r'(?<=\d)\s(?=\d)', '', text)

                matricula = text.replace(' ', '').upper()
                if Matricula.objects.filter(codigo=matricula).exclude(usuario_id=self.instance.id).exists():
                    mensaje = '"%s" ya encuentra registrada con otro usuario' % matricula
                   
                    raise ValidationError({'nueva_matricula_%s' %i: mensaje})
                if not(matricula):
                  mensaje = 'Debe agregar algun valor de la matricula, no debe contener símbolos'                     
                  raise ValidationError({'nueva_matricula_%s' %i: mensaje})

                matriculas.add(matricula)
            i += 1
            field_name = 'nueva_matricula_%s' %(i,)

        #Para cada matricula editable
        for editable in editables:
            try:
                field_name = 'matricula_editable_%s' %(editable.codigo,)
                matricula_editable = self.data[field_name]
            except: continue
            text = regex.sub(r'[^0-9\p{L}]', ' ', matricula_editable.decode('ASCII'))
            text = regex.sub(r'\s\s+', ' ', text)
            # remove spaces between numbers
            text = regex.sub(r'(?<=\d)\s(?=\d)', '', text)
            matricula_editable = text.replace(' ', '').upper()

            #Buscamos si no existia ya previamente en otro usuario
            if Matricula.objects.filter(codigo=matricula_editable).exclude(usuario_id=self.instance.id).exists():
                mensaje = '"%s" ya encuentra registrada con otro usuario' % matricula_editable                    
                raise ValidationError({'matricula_editable_%s' %editable.codigo: mensaje})
            #Si la matricula esta en blanco, tenemos un error. El usuario debe ingresar algun valor
            if not(matricula_editable):
                mensaje = 'Debe agregar algun valor de edicion de la matricula: %s. No debe contener símbolos' %editable.codigo                     
                raise ValidationError({'matricula_editable_%s' %editable.codigo: mensaje})
            #Finalmente, ingresamos en un arreglo matriz con la matricula editable(el nuevo valor ya procesado), y el codigo original(que debemos editar)
            matriculas_editables.append([matricula_editable, editable.codigo])
                      
        #Guardamos todo en cleaned_data
        self.cleaned_data['nueva_matricula'] = matriculas
        self.cleaned_data['matriculas_editables'] = matriculas_editables
        
        return super(UsuarioForm, self).clean()

    def save(self, commit=True):
        
        nueva_matricula = self.cleaned_data['nueva_matricula']
        matriculas_editables = self.cleaned_data['matriculas_editables']
        #Para cada nueva matricula, la guardamos en la base de datos
        with atomic():
            for matricula in nueva_matricula:
                Matricula.objects.get_or_create(codigo = matricula, usuario = self.instance)
            #Para todas las editables
            for matricula in matriculas_editables:
            #Si la matricula cambio
                if(matricula[0] != matricula[1]):
                    #Entonces intentamos editarla
                    editando = Matricula.objects.get(codigo = matricula[1], usuario=self.instance)
                    #Unicamente si no existia previamente en la base de datos
                    if not(Matricula.objects.filter(codigo=matricula[0], usuario=self.instance).exists()):
                        editando.codigo = matricula[0]                   
                        editando.save()
            return super(UsuarioForm, self).save(commit=commit)

    #Iterador verdadero para mostrar las matriculas y los errores que hayan ocurrido
    def get_matricula_fields(self):
        for field_name in self.fields:
            if field_name.startswith('nueva_matricula_') or field_name.startswith('matricula_editable_'):
                yield self[field_name]
    
    def get_matricula_errors(self):
        for field_name in self.fields:
             if field_name.startswith('nueva_matricula_') or field_name.startswith('matricula_editable_'):
                yield self[field_name].errors
