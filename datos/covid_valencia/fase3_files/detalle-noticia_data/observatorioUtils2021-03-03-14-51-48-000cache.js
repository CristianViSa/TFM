//Funcion que se ejecuta al seleccionar una opcion del primer select
function cargarAgrupaciones(valor)
{
	var arrayValores=new Array(
		new Array("artisticas","arte_dramatico","Arte dramático"),
		new Array("artisticas","ceramica_artistica","Cerámica artística"),
		new Array("artisticas","conservacion_y_restauracion","Conservación y restauración"),
		new Array("artisticas","comunicacion_grafica","Comunicación gráfica y audiovisual"),
		new Array("artisticas","danza","Danza"),
		new Array("artisticas","diseno_de_interiores","Diseño de interiores"),
		new Array("artisticas","diseno_industrial_artistico","Diseño industrial-Artístico"),
		new Array("artisticas","musica","Música"),
		new Array("artisticas","vidrio_artistico","Vidrio artístico"),

		new Array("ciencias_de_la_salud","enfermeria","Enfermería"),
		new Array("ciencias_de_la_salud","farmacia","Farmacia"),
		new Array("ciencias_de_la_salud","fisioterapia","Fisioterapia"),
		new Array("ciencias_de_la_salud","logopedia","Logopedia"),
		new Array("ciencias_de_la_salud","medicina","Medicina"),
		new Array("ciencias_de_la_salud","odontologia","Odontología"),
		new Array("ciencias_de_la_salud","podologia","Podología"),
		new Array("ciencias_de_la_salud","terapia","Terapia"),
		new Array("ciencias_de_la_salud","veterinaria","Veterinaria"),

		new Array("ciencias_experimentales","biologia","Biología"),
		new Array("ciencias_experimentales","bioquimica","Bioquímica"),
		new Array("ciencias_experimentales","ciencia_alimentos","Ciencia y tecnología de alimentos-nutrición humana y dietética"),
		new Array("ciencias_experimentales","ciencias_ambientales","Ciencias ambientales"),
		new Array("ciencias_experimentales","ciencias_del_mar","Ciencias del mar"),
		new Array("ciencias_experimentales","ciencias_y_tecnicas_estadisticas","Ciencias y técnicas estadísticas"),
		new Array("ciencias_experimentales","enologia","Enología"),
		new Array("ciencias_experimentales","fisica_optica_y_optometria","Física-óptica y optometría"),
		new Array("ciencias_experimentales","geologia","Geología"),
		new Array("ciencias_experimentales","matematicas_estadistica","Matemáticas-estadística"),
		new Array("ciencias_experimentales","quimica","Química"),

		new Array("ciencias_sociales_y_juridicas","biblioteconomia","Documentación-biblioteconomía y documentación"),
		new Array("ciencias_sociales_y_juridicas","ciencias_del_trabajo","Ciencias del trabajo"),
		new Array("ciencias_sociales_y_juridicas","ciencias_financieras","Ciencias actuariales y financieras"),
		new Array("ciencias_sociales_y_juridicas","ciencias_politicas","Ciencias políticas y administración pública"),
		new Array("ciencias_sociales_y_juridicas","comunicacion_audiovisual","Comunicación audiovisual"),
		new Array("ciencias_sociales_y_juridicas","deporte","Ciencias de la actividad física y del deporte"),
		new Array("ciencias_sociales_y_juridicas","direccion_empresas","Administración y dirección de empresas-ciencias empresariales"),
		new Array("ciencias_sociales_y_juridicas","economia","Economía"),
		new Array("ciencias_sociales_y_juridicas","educacion_social","Educación social"),
		new Array("ciencias_sociales_y_juridicas","investigacion_de_mercado","Investigación y técnicas de mercado"),
		new Array("ciencias_sociales_y_juridicas","leyes","Leyes"),
		new Array("ciencias_sociales_y_juridicas","maestro","Maestro"),
		new Array("ciencias_sociales_y_juridicas","pedagogia","Pedagogía"),
		new Array("ciencias_sociales_y_juridicas","periodismo","Periodismo"),
		new Array("ciencias_sociales_y_juridicas","psicologia","Psicología"),
		new Array("ciencias_sociales_y_juridicas","psicopedagogia","Psicopedagogía"),
		new Array("ciencias_sociales_y_juridicas","publicidad_y_relaciones_publicas","Publicidad y relaciones públicas"),
		new Array("ciencias_sociales_y_juridicas","sociologia","Sociología"),
		new Array("ciencias_sociales_y_juridicas","trabajo_social","Trabajo social"),
		new Array("ciencias_sociales_y_juridicas","turismo","Turismo"),

		new Array("ensenanzas_tecnicas","aeronautica","Aeronáutica"),
		new Array("ensenanzas_tecnicas","aforestal_montes","Forestal-montes"),
		new Array("ensenanzas_tecnicas","agricola_agronomia","Agrícola-agronomía"),
		new Array("ensenanzas_tecnicas","arquitectura","Arquitectura"),
		new Array("ensenanzas_tecnicas","automatica_electronica","Automática y electrónica industrial"),
		new Array("ensenanzas_tecnicas","diseno_industrial","Diseño industrial"),
		new Array("ensenanzas_tecnicas","geologia","Geología"),
		new Array("ensenanzas_tecnicas","geodesia_topografia","Geodesia-topografía"),
		new Array("ensenanzas_tecnicas","industrial","Industrial"),
		new Array("ensenanzas_tecnicas","informatica_electronica","Informática-electrónica"),
		new Array("ensenanzas_tecnicas","materiales","Materiales"),
		new Array("ensenanzas_tecnicas","minas","Minas"),
		new Array("ensenanzas_tecnicas","naval","Naval"),
		new Array("ensenanzas_tecnicas","obras_publicas","Obras públicas-caminos canales y puertos"),
		new Array("ensenanzas_tecnicas","organizacion_industrial","Organización industrial"),
		new Array("ensenanzas_tecnicas","quimica","Química"),
		new Array("ensenanzas_tecnicas","telecomunicacion","Telecomunicación"),

		new Array("humanidades","antropologia_social_y_cultural","Antropología social y cultural"),
		new Array("humanidades","bellas_artes","Bellas artes"),
		new Array("humanidades","filologia","Filología"),
		new Array("humanidades","filosofia","Filosofía"),
		new Array("humanidades","geografia","Geografía"),
		new Array("humanidades","historia","Historia"),
		new Array("humanidades","historia_del_arte","Historia del arte"),
		new Array("humanidades","historia_y_ciencias_de_la_musica","Historia y ciencias de la música"),
		new Array("humanidades","humanidades","Humanidades"),
		new Array("humanidades","linguistica","Lingüística"),
		new Array("humanidades","literatura","Teoría de la literatura y literatura comparada"),
		new Array("humanidades","traduccion_e_interpretacion","Traducción e interpretación"),
		
		new Array("otras_ensenanzas","aviacion_civil","Aviación civil"),
		new Array("otras_ensenanzas","ciencias_religiosas","Ciencias religiosas"),
		new Array("otras_ensenanzas","estudios_militares","Estudios militares")
	);
	if(valor=="0"){// desactivamos el segundo select
		document.getElementById("group").disabled=true;
	}else{
	// eliminamos todos los posibles valores que contenga el select2
	document.getElementById("group").options.length=0;

	// añadimos los nuevos valores al select2
	document.getElementById("group").options[0]=new Option("- Selecciona - ", "0");
	for(var i=0;i<arrayValores.length;i++){// unicamente añadimos las opciones que pertenecen al id seleccionado del primer select
		if(arrayValores[i][0]==valor){
			document.getElementById("group").options[document.getElementById("group").options.length]=new Option(arrayValores[i][2], arrayValores[i][1]);}
		}
	}
	// habilitamos el segundo select
	document.getElementById("group").disabled=false;
}

//Funciones para la búsqueda de informes de ocupaciones
function muestraTablaAnual() {
	document.getElementById("tablaMensual").style.display="none";
	document.getElementById("tablaAnual").style.display="";
}

function muestraTablaMensual() {
	document.getElementById("tablaMensual").style.display="";
	document.getElementById("tablaAnual").style.display="none";
}
