# -*- coding: utf8 -*- 
from django import template
from tgas import fcomunes
 
register = template.Library()

@register.filter(name='moneda')
def moneda(valor):
    """
    1234567.89 -> 1.234.567,89
    """
    return fcomunes.formatea_moneda(valor)

@register.filter(name='addcss')
def addcss(field, css):
    """
    Permite hacer: {{field|addcss:"form-control"}}
    """
    return field.as_widget(attrs={"class":css})