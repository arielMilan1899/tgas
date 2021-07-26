# -*- coding: utf8 -*-
from decimal import Decimal

from django import forms
from django.utils import timezone

from fmaestros.models import Estacion, Combustible, PrecioCombustible
from repostajes.models import Repostaje
from tgas.fcomunes import decimal2str
from usuarios.models import Matricula, Usuario

meses = [
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
]


class SelecionarTemporada(forms.Form):

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super(SelecionarTemporada, self).__init__(*args, **kwargs)

        if usuario is not None:
            self.fields['matricula'] = forms.ModelChoiceField(required=False,
                                                              queryset=Matricula.objects.filter(usuario_id=usuario.id),
                                                              empty_label='Todas las matrículas',
                                                              widget=forms.Select(attrs={"onChange": 'submit()'}))

    ano = forms.ChoiceField(required=True,
                            choices=[(r, r) for r in range(timezone.now().year - 4, timezone.now().year + 5)],
                            widget=forms.Select(attrs={"onChange": 'submit()'}))
    mes = forms.ChoiceField(required=False, choices=meses, widget=forms.Select(attrs={"onChange": 'submit()'}))
    estacion = forms.ModelChoiceField(required=False, queryset=Estacion.objects.all().order_by('provincia_id'),
                                      empty_label='Todas las estaciones',
                                      widget=forms.Select(attrs={"onChange": 'submit()'}))
    combustible = forms.ModelChoiceField(required=False, queryset=Combustible.objects.all(),
                                         empty_label='Todas los combustibles',
                                         widget=forms.Select(attrs={"onChange": 'submit()'}))


class RepostajeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(RepostajeForm, self).__init__(*args, **kwargs)

        if self.data:
            usuario = self.data.get('usuario', None)
            estacion = self.data.get('estacion', None)
            combustible = self.data.get('combustible', None)
            litros = self.data.get('litros', None)
            matricula = self.data.get('matricula', None)
            precio = self.data.get('precio_combustible', None)
        else:
            usuario = self.instance.usuario_id
            estacion = self.instance.estacion_id
            combustible = self.instance.combustible_id
            litros = self.instance.litros
            matricula = self.instance.matricula_id
            precio = self.instance.precio

        litros = decimal2str(litros)
        precio = decimal2str(precio)

        if usuario:
            self.fields['usuario'].initial = usuario
            self.fields['matricula'].disabled = False
            self.fields['matricula'].initial = matricula
            self.fields['matricula'].queryset = Matricula.objects.filter(usuario_id=usuario)

        if estacion:
            self.fields['estacion'].initial = estacion
            queryset = Combustible.objects.filter(preciocombustible__estacion_id=estacion)
            self.fields['combustible'].disabled = False
            self.fields['combustible'].initial = combustible
            self.fields['combustible'].queryset = queryset

            if not precio and combustible and queryset.filter(id=combustible).exists():
                combustible = PrecioCombustible.objects.get(combustible_id=combustible, estacion_id=estacion)
                precio = decimal2str(combustible.precio)

            if precio:
                if self.es_nuevo:
                    self.fields['precio_combustible'].initial = precio
                else:
                    self.fields['precio_combustible'].initial = precio
                    self.fields['precio_combustible'].disabled = False

                if litros:
                    clean_litros = str(litros).replace('.', '').replace(',', '.')
                    clean_precio = str(precio).replace('.', '').replace(',', '.')
                    self.fields['importe'].initial = decimal2str(Decimal(clean_precio) * Decimal(clean_litros))

        self.fields['litros'].initial = litros

    class Meta:
        model = Repostaje
        localized_fields = '__all__'
        exclude = ('importe', 'matricula', 'combustible', 'usuario', 'estacion', 'precio', 'litros')
        widgets = {'albaran': forms.TextInput(attrs={'size': 18}), }

    usuario = forms.ModelChoiceField(required=True, queryset=Usuario.objects.all(),
                                     empty_label='Selecciona usuario',
                                     widget=forms.Select(attrs={"onChange": 'submit()'}))
    estacion = forms.ModelChoiceField(required=True,
                                      queryset=Estacion.objects.all().order_by('provincia_id'),
                                      empty_label='Selecciona estación',
                                      widget=forms.Select(attrs={"onChange": 'submit()'}))
    matricula = forms.ModelChoiceField(required=True, disabled=True,
                                       queryset=Matricula.objects.all(),
                                       empty_label='Selecciona matrícula',
                                       widget=forms.Select(attrs={"onChange": 'submit()'}))
    combustible = forms.ModelChoiceField(required=True, disabled=True,
                                         queryset=Combustible.objects.all(),
                                         empty_label='Selecciona combustible',
                                         widget=forms.Select(
                                             attrs={"onChange": 'submit()'}))
    precio_combustible = forms.CharField(required=True, disabled=True,
                                         widget=forms.TextInput(
                                             attrs={'size': 18, 'onBlur': 'submit()', 'style': "text-align:right;",
                                                    'class': 'moneda'}))
    importe = forms.CharField(required=False, disabled=True,
                              widget=forms.TextInput(attrs={'size': 18, 'style': "text-align:right;"}))
    litros = forms.CharField(
        widget=forms.TextInput(
            attrs={'size': 18, 'onBlur': 'submit()', 'style': "text-align:right;", 'class': 'moneda'}))

    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(RepostajeForm, self).validate_unique(*args, **kwargs)
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

    def save(self, commit=True):

        litros = self.data['litros'].replace('.', '').replace(',', '.')
        precio = self.cleaned_data['precio_combustible'].split(' ')[0].replace(',', '.')

        litros = Decimal(litros)
        precio = Decimal(precio)

        self.instance.usuario = self.cleaned_data['usuario']
        self.instance.matricula = self.cleaned_data['matricula']
        self.instance.estacion = self.cleaned_data['estacion']
        self.instance.combustible = self.cleaned_data['combustible']
        self.instance.precio = precio
        self.instance.litros = litros
        self.instance.importe = self.instance.precio * self.instance.litros

        return super(RepostajeForm, self).save(commit=commit)
