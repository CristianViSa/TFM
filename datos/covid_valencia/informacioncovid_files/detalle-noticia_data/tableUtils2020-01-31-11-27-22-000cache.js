$(document).ready(function(){
    //Funcion para cambiar los id de las tablas y poner cada id diferente
    var id = 1
    $(".container table").each(function( index, obj ){
        obj.id='tableSepe'+ id;    
        //Fuancion que cambia el tamaño de las columnas de la tabla si son menores o iguales a 4
        if ((($('#tableSepe'+id+' >tbody >tr >th').length >0 ) && ($('#tableSepe'+id+' >tbody >tr >th').length <= 4))  || $('#tableSepe'+id+' >tbody >tr >td').length <= 4){
            $('#tableSepe'+id+' >tbody >tr >th').css({'min-width':'8rem'}); 
            $('#tableSepe'+id+' >tbody >tr >td').css({'min-width':'8rem'}); 
        }
        id= id+1;
    });
    //Funcion para añadir la clase de tabla-estadisticas en municipio
    var pathname = window.location.pathname;
    if (pathname.indexOf("/datos-estadisticos/municipios/") > -1){
        $("table").addClass("tabla-estadisticas");
    } 

    //Funcion para añadir la clase de tabla-generales
    if (pathname.indexOf("datos-estadisticos/municipios.html") > -1 || pathname.indexOf("/contratos/estadisticas-nuevas.html") > -1 ||
    pathname.indexOf("empleo/estadisticas-nuevas.html") > -1 || pathname.indexOf(" datos-estadisticos/municipios-capitales.html") > -1  ||
    pathname.indexOf("datos-estadisticos/municipios-20-45.html") > -1 || pathname.indexOf("formacion/datos.html") > -1 ){
        $("table").addClass("tabla-generales");       
    }

    //Funcion para añadir la clase de tabla-datos Avance
    if (pathname.indexOf("estadisticas/datos-avance/datos") > -1 ){
        var tablaEstadistica = document.getElementsByClassName("tabla-estadisticas");
        if (tablaEstadistica.length == 0) {
            $("table").addClass("datos-avance");
        }
    }
    
    //Funcion para añadir la clase tabla-estadisticas en datos Avance
    //Para las tablas que esten dentro de datos avance pero no sea aquellas llamadas 'datos'
    if (pathname.indexOf("estadisticas/datos-avance") > -1  && !(pathname.indexOf("estadisticas/datos-avance/datos") >-1) ){
        $("table").addClass("tabla-estadisticas");
    }
});