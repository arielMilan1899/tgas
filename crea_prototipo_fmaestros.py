#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
  Script para crear automáticamente la estructura de clases "ABMC"
  clases(tablas) Maestras (ABMC) para Altas, Bajas, Modificaciones y Consultas.

  Afecta a los ficheros urls.py, fmaestros/models.py, fmaestros/forms.py, fmaestros/views.py.
  Tambien crea las plantillas list.html y nuevo-editar.html

  Editar el diccionario "d_config" para establecer los parámetros de creación.


"""
import os
nombre_proyecto = os.path.split(os.getcwd())[-1]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", nombre_proyecto+".settings")

from django.conf import settings

# settings.BASE_DIR

d_config = {
    'nombre_clase': 'Combustible',
    'nombre_inicial_url': 'combustibles',
    'titulo_clase_singular': 'Combustible',
    'titulo_clase_plural': 'Combustibles',
}

def anade_texto_a_fichero(path_completo_fichero, texto, codigo_python=True):
    with open(path_completo_fichero, "a") as f:
        if codigo_python:
            f.write('\n# _____________ INI Código añadido por crea_prototipo_fmaestros.py\n ')
        f.write(texto)
        if codigo_python:
            f.write('\n# _______________ FIN Código añadido por crea_prototipo_fmaestros.py\n ')

    print('Añadido nuevo código python a %s' % path_completo_fichero)


def crea_urls():
    global d_config, nombre_proyecto
    fichero = os.path.join(settings.BASE_DIR, nombre_proyecto +'/urls.py')
    plantilla_py = """
    url(r'^%(nombre_inicial_url)s/$',          fmaestros_views.%(nombre_inicial_url)s_listado,  name='%(nombre_inicial_url)s-list'),
    url(r'^%(nombre_inicial_url)s/list/$',     fmaestros_views.%(nombre_inicial_url)s_listado,  name='%(nombre_inicial_url)s-list'),
    url(r'^%(nombre_inicial_url)s/list/add/$', fmaestros_views.%(nombre_inicial_url)s_nuevo,    name='%(nombre_inicial_url)s-nuevo'),
    url(r'^%(nombre_inicial_url)s/add/$',      fmaestros_views.%(nombre_inicial_url)s_nuevo,    name='%(nombre_inicial_url)s-nuevo'),
    url(r'^%(nombre_inicial_url)s/edit/$',     fmaestros_views.%(nombre_inicial_url)s_editar,   name='%(nombre_inicial_url)s-editar'),
    url(r'^%(nombre_inicial_url)s/remove/$',   fmaestros_views.%(nombre_inicial_url)s_borrar,   name='%(nombre_inicial_url)s-borrar'),
    url(r'^%(nombre_inicial_url)s/print/$',    fmaestros_views.%(nombre_inicial_url)s_imprimir, name='%(nombre_inicial_url)s-imprimir'),
    """ % d_config
    anade_texto_a_fichero(fichero, plantilla_py)


######################################################################################################################

def crea_clase():
    global d_config
    fichero = os.path.join(settings.BASE_DIR, 'fmaestros/models.py')
    plantilla_py = """
    
class %(nombre_clase)s(models.Model):
    codigo = models.CharField(max_length=4, null=True, blank=True, unique=True)
    nombre = models.CharField(max_length=60)
    
    observaciones = models.TextField(null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_paso_historico = models.DateTimeField(null=True, blank=True, default=None)


    class Meta:
        verbose_name_plural = "%(titulo_clase_plural)s"
        indexes = [
            models.Index(fields=['codigo']),
        ]

    def __str__(self):
        dato = str(self.nombre) + '  ' + str(self.codigo)
        return encoding.smart_str(dato, encoding='utf8', errors='ignore')   
    
    """ % d_config
    anade_texto_a_fichero(fichero, plantilla_py)



######################################################################################################################

def crea_forms():
    global d_config
    fichero = os.path.join(settings.BASE_DIR, 'fmaestros/forms.py')

    plantilla_py = """
    
class %(nombre_clase)sForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.es_nuevo = kwargs.get('es_nuevo')
        if self.es_nuevo is not None:
            del kwargs['es_nuevo']
        super(%(nombre_clase)sForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.%(nombre_clase)s
        localized_fields = '__all__'
        exclude = ()
        widgets = {
            'nombre': forms.TextInput(attrs={'size':18}),
            'codigo': forms.TextInput(attrs={'size':18}),
            'fecha_paso_historico': forms.DateInput(attrs={'size':8}),
            'observaciones': forms.Textarea(attrs={'rows':4, 'cols':40, 'autocorrect':"off", 'autocapitalize':"off", 'spellcheck':"false"}),
            }


    def validate_unique(self, *args, **kwargs):
        if self.es_nuevo:
            super(%(nombre_clase)sForm, self).validate_unique(*args, **kwargs)
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
    
    """ % d_config
    anade_texto_a_fichero(fichero, plantilla_py)


######################################################################################################################

def crea_views():
    global d_config
    fichero = os.path.join(settings.BASE_DIR, 'fmaestros/views.py')
    plantilla_py = """
    
def %(nombre_inicial_url)s_listado(request):
    return listado_clase(request,
                titulo_pagina='Listado %(titulo_clase_plural)s',
                idp='%(nombre_inicial_url)s-list',
                formClass=None,
                modelClass=models.%(nombre_clase)s,
                pagina_listado='backoffice/fmaestros/%(nombre_inicial_url)s-list.html',
                pagina_formulario=None)

def %(nombre_inicial_url)s_nuevo(request):
    return nuevoeditar_clase(request,
                 es_nuevo=True,
                 titulo_pagina='Nuevo %(titulo_clase_singular)s',
                 idp='%(nombre_inicial_url)s-nuevo',
                 formClass=forms.%(nombre_clase)sForm,
                 modelClass=models.%(nombre_clase)s,
                 # pagina_nuevo_dato='backoffice/fmaestros/%(nombre_inicial_url)s-nuevo-editar.html')
                 pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')

def %(nombre_inicial_url)s_editar(request):
    return nuevoeditar_clase(request,
                 es_nuevo=False,
                 titulo_pagina='Editar %(titulo_clase_singular)s',
                 idp='%(nombre_inicial_url)s-editar',
                 formClass=forms.%(nombre_clase)sForm,
                 modelClass=models.%(nombre_clase)s,
                 # pagina_nuevo_dato='backoffice/fmaestros/%(nombre_inicial_url)s-nuevo-editar.html')
                 pagina_nuevo_dato='backoffice/fmaestros/fich_plantilla_nuevoeditar.html')

def %(nombre_inicial_url)s_borrar(request):
    return borrar_clase(request,
                titulo_pagina='Borrar %(titulo_clase_singular)s',
                titulo_clase='%(titulo_clase_singular)s',
                idp='%(nombre_inicial_url)s-borrar',
                modelClass=models.%(nombre_clase)s,
                pagina_html='backoffice/fmaestros/fich_plantilla_borrar.html',
                path_cancelar='/%(nombre_inicial_url)s/list/',
                success_url='/%(nombre_inicial_url)s/list/')

def %(nombre_inicial_url)s_imprimir(request):
    return None
    
    """ % d_config
    anade_texto_a_fichero(fichero, plantilla_py)


######################################################################################################################

def crea_htmls():
    global d_config, nombre_proyecto
    filename_list = nombre_proyecto + '/templates/backoffice/fmaestros/%(nombre_inicial_url)s-list.html' % d_config
    filename_list = os.path.join(settings.BASE_DIR, filename_list)
    filename_editar = nombre_proyecto + '/templates/backoffice/fmaestros/%(nombre_inicial_url)s-nuevo-editar.html' % d_config
    filename_editar = os.path.join(settings.BASE_DIR, filename_editar)

    html_list = """
{% extends "backoffice/base.html"%}

{% block contenido_ppal%}
<script>
    $(document).ready(function() {
        $("#t___nombre_inicial_url___").DataTable({
            "language": {
                "url": "/static/backoffice/plugins/datatables/plug-ins/1.10.13/i18n/Spanish.json"
                    },
            "order": [[ 1, "desc" ]],
            "bPaginate": true,
            "bFilter": true,
            "bInfo": true,
            "columnDefs": [
                { className: "text-left", "targets": [0,1] },
                { className: "text-right", "targets": [] },
                { className: "text-center", "targets": [] },
                ],
            "fnInitComplete": function (oSettings) {
              $('.dataTables_filter').each(function () {
                    $(this).append('&nbsp;<a class="btn btn-social-icon btn-linkedin" data-toggle="tooltip" title="Añadir datos" href="add"><i class="fa fa-plus"></i></a>&nbsp;<a class="btn btn-social-icon btn-linkedin" data-toggle="tooltip" title="Exportar a Excel" href="#"><i class="fa fa-file-excel-o"></i></a>');
              });
            },
        });
      }
    );
</script>

    <!-- Main content -->
    <section class="content">
      <div class="row">
        <div class="col-xs-12">

          <div class="box">
            <div class="box-body">

              <table id="t___nombre_inicial_url___" class="table table-bordered table-hover">
                <thead>
                <tr>
                  <th>Código</th>
                  <th>Nombre</th>
                </tr>
                </thead>
                <tbody>

{% for dato in l_datos%}
                <tr>
                    <td> <a href="/___nombre_inicial_url___/edit/?dato_id={{ dato.id}}">{{ dato.codigo }}</a></td>
                    <td> {{ dato.nombre }} </td>
                </tr>
{%endfor%}

                </tbody>
              </table>
            </div>            <!-- /.box-body -->
          </div>          <!-- /.box -->
        </div>        <!-- /.col -->
      </div>      <!-- /.row -->
    </section>    <!-- /.content -->


{% endblock%}
    
    """.replace('___nombre_inicial_url___',d_config['nombre_inicial_url'])


    html_editar = """
    
{% extends "backoffice/base.html"%}

{% block contenido_ppal%}

<script>
  $( function() {
    $("#id_fecha_paso_historico").datepicker();
    $("#id_fecha_paso_historico").mask("99/99/9999",{placeholder:"dd/mm/aaaa"});
    $("#id_hora_paso_historico").mask("99:99",{placeholder:"hh:mm"});

  } );
</script>

    <!-- Main content -->
    <section class="content">

	<form id="form1" action="" method="post">{% csrf_token %}
        <input type="hidden" name="dato_id" value="{{ dato_id }}">

      <div class="row">
        <div class="col-xs-12">
          <div class="box box-primary">
            <div class="box-body">
    <table class="uifmaestros"><tbody>
    <tr><td> Código: </td>
        <td>{{ formulario.codigo }}</td>
        <td>{% for error in formulario.codigo.errors %}<p style="color:red"> &nbsp; {{ error|escape }}</p>{% endfor %}</td>
    <td>  Nombre: </td>
        <td>{{ formulario.nombre }}</td>
        <td>{% for error in formulario.nombre.errors %}<p style="color:red"> &nbsp; {{ error|escape }}</p>{% endfor %}</td>
    </tr>

    </tbody></table>

                <br/><br/>

    <table> <tbody>
<tr valign="top"><td> <table class="uifmaestros"> <tbody>
<!----- Grupo de datos de la izquierda ---->

    <tr><td>  Dato 1 </td><td>&nbsp;</td>
        <td>{{ formulario.dato1 }}</td>
        <td>{% for error in formulario.dato1.errors %}<p style="color:red"> &nbsp; {{ error|escape }}</p>{% endfor %}</td>
    </tr>

<!----- FIN Grupo de datos de la izquierda ---->
</tbody></table></td>
<td> &nbsp; &nbsp; &nbsp; </td>
<td> <table class="uifmaestros"> <tbody>
<!----- Grupo de datos de la derecha ---->


    <tr><td>  Fecha Paso Historico </td><td>&nbsp;</td>
        <td>{{ formulario.fecha_paso_historico }} &nbsp; &nbsp; &nbsp;{{ formulario.hora_paso_historico }}</td>
        <td>{% for error in formulario.fecha_paso_historico.errors %}<p style="color:red"> &nbsp; {{ error|escape }}</p>{% endfor %}
            {% for error in formulario.hora_paso_historico.errors %}<p style="color:red"> &nbsp; {{ error|escape }}</p>{% endfor %}
        </td>
    </tr>
    <tr><td>  Observaciones </td><td>&nbsp;</td>
        <td>{{ formulario.observaciones }}</td>
        <td>{% for error in formulario.observaciones.errors %}<p style="color:red"> &nbsp; {{ error|escape }}</p>{% endfor %}</td>
    </tr>
<!----- FIN Grupo de datos de la derecha ---->
</tbody></table></td></tr>
    </tbody></table>


	</form>

            </div> <!-- /.box-body -->
          </div>         <!-- /.box -->
            {{ barra_botones|safe }}


        </div>        <!-- /.col -->
      </div>      <!-- /.row -->
    </section>    <!-- /.content -->


{% endblock%}
    
    """

    if not os.path.exists(filename_list):
        anade_texto_a_fichero(filename_list, html_list, codigo_python=False)
    else:
        print('NO se crea. Ya existía el fichero %s' % filename_list)

    if not os.path.exists(filename_editar):
        anade_texto_a_fichero(filename_editar, html_editar, codigo_python=False)
    else:
        print('NO se crea. Ya existía el fichero %s' % filename_editar)



if __name__ == '__main__':
    global d_config
    print('Iniciando proceso creacion ABMC de %s' % d_config['nombre_inicial_url'])
    print('__________________ crea_urls()')
    crea_urls()

    print('__________________ crea_clase()')
    crea_clase()

    print('__________________ crea_forms()')
    crea_forms()

    print('__________________ crea_views()')
    crea_views()

    print('__________________ crea_htmls()')
    crea_htmls()

    print("""
      Fin del proceso. Revisar "a mano":
      
          * urls.py: Colocar URLs en el lugar adecuado.
          
          * menu.py: Añadir nuevo apartado al menu:
      "{'tit': u'%(titulo_clase_plural)s', 'idp': '', 'url-name': '%(nombre_inicial_url)s-list',  'ico': 'fa-heart', 'submenu': []},"
      
          * fmaestros/uitools.py: Añadir la nueva clase al dict d_maestros:
       "    '%(nombre_inicial_url)s': models.%(nombre_clase)s,"   
          
          Ejecutar:  ./manage.py makemigrations  y  ./manage.py migrate
          Ejecutar:  ./crea_adminpy.py  (Para incluir la clase en Django Admin) 

    """ % d_config)
    




