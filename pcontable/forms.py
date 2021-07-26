# -*- coding: utf8 -*-

from django import forms

class SelecTemporada(forms.Form):

    temporada = forms.ChoiceField(required=True,
                                  choices=[(u'2018-2019', u'2018-2019',),
                                           (u'2019-2020', u'2019-2020'),
                                          ])


