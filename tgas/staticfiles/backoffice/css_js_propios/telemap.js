//// ----------------------------  Barra de botones de desplazamiento entre registros + grabar, salir, ...

function barra_botones(boton)
{
var input = $("<input>")
               .attr("type", "hidden")
               .attr("name", boton).val("bla");
    $('#form1').append($(input));
    if ( document.getElementById( "contador_segs" )) {
       /* Para que muestre "Progresando" y un spin */
       pagina_recargada();
       proceso_llamado();
    };

  document.getElementById('form1').submit();
};

//// ----------------------------  Tabla DataTable por defecto para la mayoría de listados

$(document).ready(function() {
    $("#tlistados1").DataTable({
      "language": {
          "url": "/static/backoffice/plugins/datatables/plug-ins/1.10.13/i18n/Spanish.json"
      },
      "buttons": [
        'csv'
    ],
      'fnInitComplete': function (oSettings) {
          $('.dataTables_filter').each(function () {
                $(this).append('&nbsp;<a class="btn btn-social-icon btn-linkedin" data-toggle="tooltip" title="Añadir datos" href="add"><i class="fa fa-plus"></i></a>&nbsp;<a class="btn btn-social-icon btn-linkedin" data-toggle="tooltip" title="Exportar a Excel" href="#"><i class="fa fa-file-excel-o"></i></a>');
          });
      }
    });
  }
);


//// --------------------------------Valores por defecto del datepicker para no tener que incluirlos en cada instancia.
$(function() {
    $.datepicker.setDefaults({
      showButtonPanel: true,
      dateFormat: "dd/mm/yy",
      firstDay: 1, /* Set the first day of the week: Sunday is 0, Monday is 1, etc. */
      dayNamesMin: [ "Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa" ],
      monthNames: [ "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                    "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre" ],
      currentText: "Hoy",
      closeText: "Aceptar",
      showOn: "button",
      buttonText: '<span class="fa fa-calendar">'
    });
} );

//// ----------------Para formatear los input numero de 12345 => 12.340,00 El input debe pertenecer a la clase "moneda"
function formatea_moneda(str) {
    var parts = (str + "").split(","),
        main = parts[0],
        len = main.length,
        output = "",
        first = main.charAt(0),
        i;
    // Si ya existe un punto no procesar, ya ha sido procesado.
    if (str.indexOf('.') !== -1) {
        return str;
    }

    if (first === '-') {
        main = main.slice(1);
        len = main.length;
    } else {
    	  first = "";
    }
    i = len - 1;
    // Si introducimos ,05 lo convierte a 0,05
    if (len === 0) {
        output += "0";
    }
    while(i >= 0) {
        output = main.charAt(i) + output;
        if ((len - i) % 3 === 0 && i > 0) {
            output = "." + output;
        }
        --i;
    }
    // put sign back
    output = first + output;
    // put decimal part back
    if (parts.length > 1) {
        if (parts[1].length >= 2) {
            output += "," + parts[1].slice(0, 2);
        } else {
            output += "," + parts[1] + "0";
        }
    } else {
        output += ",00"
    }
    return output;
};

/// En los campos numéricos sólo permite numeros 0-9 punto, coma y signo - AL perder el foco llama a la función "formatea_numero"
$(document).ready(function() {
    $('.moneda').keyup(function(){
       var self = $(this);
       var removedText = self.val().replace(/[^0-9.,\-]+/, '');
       self.val(removedText);
    });
    $(".moneda").blur(function(){
        $(this).val(formatea_moneda($(this).val()));
    });
});

//// ----------------Para formatear los input numero de 12345 => 12.340 El input debe pertenecer a la clase "numero"
function formatea_numero(str) {
    var parts = (str + "").split(","),
        main = parts[0],
        len = main.length,
        output = "",
        first = main.charAt(0),
        i;
    // Si ya existe un punto no procesar, ya ha sido procesado.
    if (str.indexOf('.') !== -1) {
        return str;
    }

    if (first === '-') {
        main = main.slice(1);
        len = main.length;
    } else {
    	  first = "";
    }
    i = len - 1;
    // Si introducimos ,05 lo convierte a 0,05
    if (len === 0) {
        output += "0";
    }
    while(i >= 0) {
        output = main.charAt(i) + output;
        if ((len - i) % 3 === 0 && i > 0) {
            output = "." + output;
        }
        --i;
    }
    // put sign back
    output = first + output;
    // put decimal part back
/*    if (parts.length > 1) {
        if (parts[1].length >= 2) {
            output += "," + parts[1].slice(0, 2);
        } else {
            output += "," + parts[1] + "0";
        }
    } else {
        output += ",00"
    }
*/    return output;
};

/// En los campos numéricos sólo permite numeros 0-9 punto y signo - AL perder el foco llama a la función "formatea_numero"
$(document).ready(function() {
    $('.numero').keyup(function(){
       var self = $(this);
       var removedText = self.val().replace(/[^0-9.\-]+/, '');
       self.val(removedText);
    });
    $(".numero").blur(function(){
        $(this).val(formatea_numero($(this).val()));
    });
});

//----------------------------------------------------- Evita que la pulsación de enter envíe (submit) el formulario
/*
$(document).ready(function() {
    $("form").keypress(function(e) {
        if (e.which == 13) {
            return false;
        }
    });
});
*/

// ----------------------------------------------------------------------  Cambia la pulsacion del punto por una coma:
$(document).ready(function() {
 // All decimal input fields must have a class named 'number'
    $('input.numero').each(function () {
        $(this).keypress(function(e){
            // '46' is the keyCode for '.'
            if(e.keyCode == '46' || e.charCode == '46'){
              // IE
              if(document.selection){
                    // Determines the selected text. If no text selected,
                    // the location of the cursor in the text is returned
                    var range = document.selection.createRange();
                    // Place the comma on the location of the selection,
                    // and remove the data in the selection
                    range.text = ',';
              // Chrome + FF
              }else if(this.selectionStart || this.selectionStart == '0'){
                    // Determines the start and end of the selection.
                    // If no text selected, they are the same and
                    // the location of the cursor in the text is returned
                    // Don't make it a jQuery obj, because selectionStart
                    // and selectionEnd isn't known.
                    var start = this.selectionStart;
                    var end = this.selectionEnd;
                    // Place the comma on the location of the selection,
                    // and remove the data in the selection
                    $(this).val($(this).val().substring(0, start) + ','
                     + $(this).val().substring(end, $(this).val().length));
                    // Set the cursor back at the correct location in
                    // the text
                    this.selectionStart = start + 1;
                    this.selectionEnd = start +1;
                }else{
                    // if no selection could be determined,
                    // place the comma at the end.
                    $(this).val($(this).val() + ',');
                }
                return false;
            }
        });
    });
  }
);

// ------------ Reloj Contador que muestra segs y la palabra "Procesando ..." -------------------

/* "Procesando ..." */
var n = 0;
var mytimer = 0;
var msg = ["P", "Pr", "Pro", "Proc", "Proce", "Proces", "Procesa",
           "Procesan", "Procesand", "Procesando", "Procesando .",
           "Procesando ..", "Procesando ..."];
var spinner = '<i class="fa fa-spinner fa-spin" style="font-size:24px; color:red"></i>'

function muestraReloj() {
    txt = spinner + n + " " + msg[n % 13]
    document.getElementById("contador_segs").innerHTML = txt;
    n++;
};

function proceso_llamado() {
    mytimer = setInterval(muestraReloj, 1000);
};

function pagina_recargada() {
    clearInterval(mytimer);
    document.getElementById("contador_segs").innerHTML = '';
}

/* $(document).ready(function(){ pagina_recargada();}) */

/*

  Uso:
    <div id="contador_segs"></div>      ---> Dónde queramos poner el contador
    onclick="proceso_llamado();"    ---> En el <a href= ... o en el <submit ...
    onsubmit="proceso_llamado();"   ---> En el <form>
*/

// -------------------------------------------------------  p r u e b a s --------------------------------------------

//------------- Fuerza que el Intro actúe como un tab (Saltando al siguiente campo y evitando el submit
/*
$(document).ready(function() {
    $('input').keypress(function(e) {
        if (e.which == 13) {
//            alert($(this).next('input'));
//            $(this).next('input').focus();
            $(this).nextAll('input').first().focus();
//            return false;
            e.preventDefault();
        }
    });
});
*/
//---------------------------------- Permite ordenar correctamente las cantidades en formato -1.234.567,00 ----
//--- Dentro de las DataTable.
//--  Usando 'formatted-num' en  "columnDefs"
//--
//--   $("#tclientes").DataTable({
//--               "language": {
//--                   "url": "/static/backoffice/plugins/datatables/plug-ins/1.10.13/i18n/Spanish.json"
//--                       },
//--               "order": [[ 3, "asc" ]],
//--               "bPaginate": true,
//--               "bFilter": true,
//--               "bInfo": true,
//--               "columnDefs": [
//--                   { className: "text-left", "targets": [0] },
//--                   { className: "text-right", "targets": [1,2,3,4,5] },
//--                   { className: "text-center", "targets": [] },
//--                   { targets: [1,2,3,4,5], type: 'moneda' },
//--                   { targets: [0], type: 'fecha' },      /* formato dd/mm/aaaa  */
//--               /*  { targets: [0], type: 'fechahora' },  /* formato dd/mm/aaaa hh:mm */
//--                   ],
//--           });

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "moneda-pre": function ( a ) {
        var m = a.replace(/<[^>]*>/g, '');
        m = m.replace(/\./g, "");
        m = m.replace(",", ".");

        return parseFloat( m );
    },

    "moneda-asc": function ( a, b ) {
        return a - b;
    },

    "moneda-desc": function ( a, b ) {
        return b - a;
    }
} );


jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "fecha-pre": function ( a ) {
        var peso = 0;
        var fecha = a.replace(/<[^>]*>/g, '');
        fecha = fecha.split('/');
        if (fecha.length == 3) { peso = (fecha[2] + fecha[1] + fecha[0]) * 1 };

        return peso;
    },

    "fecha-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "fecha-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
} );

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "fechahora-pre": function ( a ) {
        var peso = 0;
        var fh = a.replace(/<[^>]*>/g, '');
        fh = fh.replace(':','/');
        fh = fh.replace(' ','/');
        fh = fh.split('/');
        // 01/11/1976 12:45  -> 01/11/1976/12/45
        // 0  1   2    3  4
        if (fh.length == 5) { peso = (fh[2] + fh[1] + fh[0] + fh[3] + fh[4]) * 1 };

        return peso;
    },

    "fechahora-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "fechahora-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
} );
