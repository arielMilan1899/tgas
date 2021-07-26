# -*- coding: utf8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

from fmaestros.models import Empresa, Cuenta, Apunte, Provincia, Estacion, Combustible
import decimal

from django.forms import ModelForm

# class BaseForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(BaseForm, self).__init__(*args, **kwargs)
#         for bound_field in self:
#             if hasattr(bound_field, "field") and bound_field.field.required:
#                 bound_field.field.widget.attrs["required"] = "required"



class EmpresaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(EmpresaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Empresa
        exclude = ()
        widgets = {'observaciones': forms.Textarea(attrs={'rows':2, 'cols':40}),
            'nombre': forms.TextInput(attrs={'size':18}),
            'codigo': forms.TextInput(attrs={'size':18}),
            'cp': forms.TextInput(attrs={'size':6}),
            'cif': forms.TextInput(attrs={'size':10}),
            'razon_social': forms.TextInput(attrs={'size':50}),
            'direccion': forms.Textarea(attrs={'rows':2, 'cols':50}),
            'fecha_paso_historico': forms.DateInput(attrs={'size':8}),
            }

    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(EmpresaForm, self).validate_unique(*args, **kwargs)
        else:
            exclude = self._get_validation_exclusions()
            try:
                self.instance.validate_unique(exclude=exclude)
            except forms.ValidationError as e:
                try:
                    del e.error_dict['nombre']
                    del e.error_dict['codigo']
                except:
                    pass
                self._update_errors(e)


class CuentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(CuentaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cuenta
        exclude = ()
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
                   'nombre': forms.TextInput(attrs={'size': 18}),
                   'codigo': forms.TextInput(attrs={'size': 18}),
                   }

    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(CuentaForm, self).validate_unique(*args, **kwargs)
        else:
            exclude = self._get_validation_exclusions()
            try:
                self.instance.validate_unique(exclude=exclude)
            except forms.ValidationError as e:
                try:
                    del e.error_dict['nombre']
                    del e.error_dict['codigo']
                except:
                    pass
                self._update_errors(e)


# class ApunteForm(forms.Form):
#     fecha = forms.DateField(required=True, widget=forms.DateInput(attrs={'size': 8}))
#     descripcion = forms.CharField(required=True, max_length=16, widget=forms.TextInput(attrs={'size': 40}))
#     observaciones = forms.CharField(required=False, max_length=16, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))
#     importe = forms.CharField(required=True, max_length=16, widget=forms.TextInput(attrs={'size': 8, 'style':"text-align:right;", 'class': "moneda"}))
#     es_gasto = forms.ChoiceField(required=True, choices=[
#         (u'Gasto', u'Gasto'), (u'Ingreso', u'Ingreso'), ])
#

class ApunteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(ApunteForm, self).__init__(*args, **kwargs)
        # self.fields["importe"].validators = [self.clean_importe]

    class Meta:
        model = Apunte
        exclude = ()
        widgets = {
            'fecha': forms.DateInput(attrs={'size': 8}),
            'descripcion': forms.TextInput(attrs={'size': 40}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            # 'importe': forms.TextInput(attrs={'size': 6, 'style': "text-align:right;", 'class': "moneda"}),
            'importe': forms.TextInput(attrs={'size': 6, 'style': "text-align:right;"}),
        }

    # def clean(self, *args, **kwargs):
    #     super(ApunteForm, self).clean(*args, **kwargs)
    #     else:
    #         exclude = self._get_validation_exclusions()
    #         try:
    #             self.instance.validate_unique(exclude=exclude)
    #         except forms.ValidationError as e:
    #             try:
    #                 del e.error_dict['nombre']
    #                 del e.error_dict['codigo']
    #             except:
    #                 pass
    #             self._update_errors(e)
    #
    # def clean_importe(self):
    #     numero = self.cleaned_data['importe']
    #     print "[]"*40, numero
    #     print "\n"*8
    #     if numero == '':
    #         return numero
    #     try:
    #         decimal.Decimal(numero)
    #     except:
    #         raise forms.ValidationError("No es un importe válido")
    #     return numero


# _____________ INI Código añadido por crea_prototipo_fmaestros.py


class ProvinciaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']

        self.combustibles = Combustible.objects.all()
        super(ProvinciaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Provincia
        localized_fields = '__all__'
        exclude = ()
        widgets = {
            'nombre': forms.TextInput(attrs={'size': 18}),
            'codigo': forms.TextInput(attrs={'size': 18}),
            'observaciones': forms.Textarea(attrs={
                'class': 'observaciones',
                'rows': 4,
                'cols': 40,
                'autocorrect': "off",
                'autocapitalize': "off",
                'spellcheck': "false"}),
            }


    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(ProvinciaForm, self).validate_unique(*args, **kwargs)
        else:
            exclude = self._get_validation_exclusions()
            try:
                self.instance.validate_unique(exclude=exclude)
            except forms.ValidationError as e:
                try:
                    del e.error_dict['codigo']
                except:
                    pass
                self._update_errors(e)


# _______________ FIN Código añadido por crea_prototipo_fmaestros.py

# _____________ INI Código añadido por crea_prototipo_fmaestros.py


class EstacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(EstacionForm, self).__init__(*args, **kwargs)

        for precio in self.instance.precios():
            field_name = 'precio_%s' % (precio.combustible.codigo,)
            self.fields[field_name] = forms.CharField(max_length=30, required=False,
                                                      widget=forms.NumberInput(attrs={'size': 10}))
            self.initial[field_name] = precio.precio if precio.precio else '0'

    class Meta:
        model = Estacion
        localized_fields = '__all__'
        exclude = ('token', )
        widgets = {
            'nombre': forms.TextInput(attrs={'size':18}),
            'codigo': forms.TextInput(attrs={'size':18}),
            'observaciones': forms.Textarea(attrs={
                'class': 'observaciones',
                'rows': 4,
                'cols': 40,
                'autocorrect': "off",
                'autocapitalize': "off",
                'spellcheck': "false"}),
            'geo_latitud': forms.TextInput(attrs={'size':10}),
            'geo_longitud': forms.TextInput(attrs={'size':10}),
            }

    def clean(self):

        for precio in self.instance.precios():
            field_name = 'precio_%s' % (precio.combustible.codigo,)
            nuevo_precio = self.cleaned_data[field_name]

            if len(nuevo_precio.split('.')[0]) >= 3:
                raise ValidationError({field_name: '%s: Precio incorrecto' % precio.combustible})

    def save(self, commit=True):
        instance = super(EstacionForm, self).save(commit=commit)

        for precio in self.instance.precios():
            field_name = 'precio_%s' % (precio.combustible.codigo,)
            nuevo_precio = self.cleaned_data[field_name]
            precio.precio = nuevo_precio if nuevo_precio else decimal.Decimal(0)
            precio.save()

        return instance

    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(EstacionForm, self).validate_unique(*args, **kwargs)
        else:
            exclude = self._get_validation_exclusions()
            try:
                self.instance.validate_unique(exclude=exclude)
            except forms.ValidationError as e:
                try:
                    del e.error_dict['codigo']
                except:
                    pass
                self._update_errors(e)

    # Iterador verdadero para mostrar los inputs para precios de las estaciones y los errores que han ocurrido
    def get_precios_fields(self):
        combustibles = Combustible.objects.all()
        precios_fields = [self[field_name] for field_name in self.fields if field_name.startswith('precio_')]
        for par in zip(combustibles, precios_fields):
            yield par

    def get_precios_errors(self):
        for field_name in self.fields:
            if field_name.startswith('precio_') and self[field_name].errors:
                yield self[field_name].errors



# _____________ INI Código añadido por crea_prototipo_fmaestros.py
 
    
class CombustibleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(CombustibleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Combustible
        localized_fields = '__all__'
        exclude = ()
        widgets = {
            'nombre': forms.TextInput(attrs={'size':18}),
            'codigo': forms.TextInput(attrs={'size':18}),
            }


    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(CombustibleForm, self).validate_unique(*args, **kwargs)
        else:
            exclude = self._get_validation_exclusions()
            try:
                self.instance.validate_unique(exclude=exclude)
            except forms.ValidationError as e:
                try:
                    del e.error_dict['codigo']
                except:
                    pass
                self._update_errors(e)
    
    
# _______________ FIN Código añadido por crea_prototipo_fmaestros.py
 