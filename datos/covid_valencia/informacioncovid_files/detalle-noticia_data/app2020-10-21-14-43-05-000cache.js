$(document).ready(function() {
  $('.carousel-control-prev').focus();
  var num = $( "div" ).find(".panel-body").length;
  for(var i = 0; i < num; i++){

    $("#accordion").attr("id" , "accordion"+ i);
    $("#boton").attr("data-parent" , "#accordion"+ i);
    $("#boton").attr("aria-label" , "#accordion"+ i);
    $("#boton").attr("id" , "boton"+ i);
    $("#boton"+ i).attr("href", '#collapse'+i);
    $('#collapse').attr('id', 'collapse'+i);
  }
   //Primer desplegable abierto por defecto
  $("#collapse0").addClass("show");

  $(".panel-title a").click(function(){
    $(this).toggleClass("active")
    });

  $(".botonDesplegable").click(function(){
    $("i", this).toggleClass("up")
  });

  $("#btnSearchmov").click(function(){
    var attr =   $(".btnSearchHome").attr('role')
    if (attr=="Close") {
      $(".btnSearchHome").attr('role', 'Buscar');
      $(".btnSearchHome").attr('aria-label', 'Buscar');
      $("#searchLine").toggleClass("ocultar");
    }else{
      $(".btnSearchHome").attr('role', 'Close');
      $(".btnSearchHome").attr('aria-label', 'Close');
      $("#searchLine").toggleClass("mostrar");
    }
    $("#searchIco").toggleClass("fa-search");
    $("#searchIco").toggleClass("fa-times");
  });

  $("#botMenuIz").click(function(){
    $("#menuLatMov").toggleClass("ver");
  });


  var cookieName = $("input[name=cookiePopUp]").val();
  // Mostramos el popup si está la cookie a false
  if (getCookie(cookieName)=='false' || getCookie(cookieName)=='') {
	  $('#myModal').show();
  }

 //lightbox
  $("#imagenGaleria img").click(function(){
    var responsive =$(this).attr("data-srcset")
  	$("#lightbox img").attr("data-srcset",responsive)
	  $("#lightbox img").attr("srcset",responsive)
    var ruta =$(this).attr("src")
    $("#lightbox img").attr("src",ruta)
  	$("#lightbox").show()
  })

  $("#lightbox .closeIco").click(function(){
  		$("#lightbox").hide()
  });


  //Desplegar contenido TableSorter
  $(".desem").click(function(){
   $(this).next('ul.hyde').slideToggle('slow');
  });



var lastScrollTop = 200;
$(window).scroll(function(event){
   var st = $(this).scrollTop();
   if (st >= lastScrollTop){
       // downscroll code
       document.getElementById("scrollUp").style.display = "inline"
   } else {
      // upscroll code
      document.getElementById("scrollUp").style.display = "none"
   }
});

	$("table").each(function() {
		var thead = $('table').find('thead').length;
		var rowCount = $('tr:nth-child(2)').text();
		var tag = $('tr:first td').find('a').length;
		if(rowCount != '' && tag <= 0 && thead <= 0){
			$("tr:first-child td").each(function() {
				  $(this).replaceWith('<th>' + $(this).text() + '</th>');
			});
		}
		if(thead > 0){
			$("thead tr:first-child td").each(function() {
				  $(this).replaceWith('<th>' + $(this).text() + '</th>');
			});
		}
	});

	//Crear la url para el plugin accesible en modo responsive
	$('a[id^="accesible"]').each(function() {
		var url = window.location.href;
		var res = url.replace(window.location.hostname, "www--sepe--es.insuit.net");
	    if(window.location.port!=""){
	    	var res = res.replace(":"+window.location.port, "");
	    }
	    $(this).attr("href", res);
	 });


	//ordenar StickyTableHeaders
	  $('#ordenar').tablesorter();
});

//Funci n para crear las cookies de los popups
function createCookiePopUp(input){
	var date = new Date();
	date.setTime(date.getTime()+(7*24*60*60*1000));
	var expires = "; expires="+date.toGMTString();
	var cookie = document.getElementsByName(input);
	if(cookie.length>0){
	    var nombreCookie = cookie[0].value;
	var marcado = cookie[0].checked;
	var pathname = window.location.pathname;
    self.document.cookie = nombreCookie+"="+marcado+expires+";path="+pathname+";";
	}
}

//Funci n para obtener el valor de una cookie
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
      	  var val = c.substring(name.length, c.length);
            return val;
        }
    }
    return "";
}

function createPDFLink(elementToPrint, headerImagePath, footerImagePath, fileName, restPath) {
  const elem = document.querySelectorAll(elementToPrint)[0];
  const cloneNode = elem.cloneNode(true);

  var source = cloneNode;
  var html = "";
  
  var childNodes = source.querySelectorAll("p, span, ul, ol, li, h1, h2, h3, h4, h5, h6, form, table, tr, td, a, div, section, img");
  for(var i = 0; i < childNodes.length; i++) {
	  if(childNodes[i].hasAttribute("style")) {
		  childNodes[i].removeAttribute("style");
	  }
  }
  
  var br = source.getElementsByTagName("hr");
  for(var i = 0; i < br.length; i++) {
	  br[0].parentNode.removeChild(br[0]);
  }
  
  var pdfButtons = source.getElementsByClassName("btn-imprimir");
  var pdfButtonsLength = pdfButtons.length;
  for (var i = 0; i < pdfButtonsLength; i++) {
    if(pdfButtons[0] != null) {
      pdfButtons[0].parentNode.removeChild(pdfButtons[0]);
    }
  }

  var images = source.getElementsByTagName('img');
  var l = images.length;
  for (var i = 0; i < l; i++) {
    if(images[0] != null) {
      images[0].parentNode.removeChild(images[0]);
    }
  }
  
  var divs = source.getElementsByTagName('div');
  var nDivs = Array.prototype.filter.call(divs, function(div){
  	return div.nodeName === 'DIV' && (div.style.display === "none" || div.id.indexOf("des_") != -1);
  });
  
  var nDisvLength = nDivs.length;
  for(var i = 0; i < nDisvLength; i++) {
	  if(nDivs[i] != null) {
		nDivs[i].parentNode.removeChild(nDivs[i]);
	  }
  }

  var locations = source.getElementsByTagName('a');
  var locLen = locations.length;
  for (var i = 0; i < locLen; i++) {
    locations[i].href = locations[i].href;
  }

  var tables = source.getElementsByTagName("table");
  var tablesLen = tables.length;
  for(var i = 0; i < tablesLen; i++) {
    var table = tables[i];
    var tableLinks = tables[i].getElementsByTagName("a");
    var tableLinksLen = tableLinks.length;
    for(var j = 0; j < tableLinksLen; j++) {
      var span = document.createElement("span");
      span.innerHTML = tableLinks[0].innerHTML;
      tableLinks[0].parentNode.replaceChild(span, tableLinks[0]);
    }
  }

  var noscripts = source.getElementsByTagName('noscript');
  var l = noscripts.length;
  for (var i = 0; i < l; i++) {
    if(noscripts[0] != null) {
  	    noscripts[0].parentNode.removeChild(noscripts[0]);
  	}
  }

  var objects = source.getElementsByTagName('object');
  var l = objects.length;
  for (var i = 0; i < l; i++) {
    if(objects[0] != null) {
  	    objects[0].remove();
  	}
  }

  var iframes = source.getElementsByTagName('iframe');
  var l = iframes.length;
  for (var i = 0; i < l; i++) {
    if(iframes[0] != null) {
      iframes[0].parentNode.removeChild(iframes[0]);
    }
  }

  var scripts = source.getElementsByTagName('script');
  var l = scripts.length;
  for (var i = 0; i < l; i++) {
    if(scripts[0] != null) {
      scripts[0].parentNode.removeChild(scripts[0]);
    }
  }

  var galerias = source.getElementsByClassName('galeria');
  var l = galerias.length;
  for (var i = 0; i < l; i++) {
    galerias[0].parentNode.removeChild(galerias[0]);
  }

  var textosPie = source.getElementsByClassName('textoPie');
  var l = textosPie.length;
  for (var i = 0; i < l; i++) {
    textosPie[0].parentNode.removeChild(textosPie[0]);
  }

  var cols = source.getElementsByClassName('col-lg-3');
  var l = cols.length;
  for (var i = 0; i < l; i++) {
    cols[0].parentNode.removeChild(cols[0]);
  }

  var tabs = source.getElementsByClassName('nav-tabs');
  var l = tabs.length;
  for (var i = 0; i < l; i++) {
    tabs[0].parentNode.removeChild(tabs[0]);
  }

  html = source.outerHTML;


  html = html.replace(/<ul/g, "<ul style='margin-left:0'");
  html = "<html>" + "<body><div>" + html + "</div></body></html>";
	html = html.replace(/<a/g, "<a style='color:rgb(0,0,255);text-decoration:underline;line-height:10px;'");
	html = html.replace(/<h1/g, "<h1 style='font-size:20px;font-weight:bold;line-height:19px'");
	html = html.replace(/<\/h1>/g, "</h1><p style='line-height:5px'>&nbsp;</p>");
	html = html.replace(/<h2/g, "<h2 style='font-size:18px;font-weight:bold;line-height:19px'");
	html = html.replace(/<\/h2>/g, "</h2><p style='line-height:5px'>&nbsp;</p>");
	html = html.replace(/<h3/g, "<h3 style='font-size:13px;font-weight:bold;line-height:15px'");
	html = html.replace(/<\/h3>/g, "</h3><p style='line-height:5px'>&nbsp;</p>");
	html = html.replace(/<h4/g, "<h4 style='font-size:11px;font-weight:bold;line-height:15px'");
	html = html.replace(/<\/h4>/g, "</h4><p style='line-height:5px'>&nbsp;</p>");
	html = html.replace(/<p/g, "<p style='text-align:justify;line-height:14px;font-size:11px;'");
	html = html.replace(/<\/ul>/g, "</ul><p style='line-height:5px'>&nbsp;</p>");
	html = html.replace(/<li>/g, "<li style='text-align:justify;line-height:14px;font-size:11px;margin-left:0;'>");
  html = html.replace(/<\/p>/g, "</p><p style='line-height:5px'>&nbsp;</p>");
  html = html.replace(/<!--[\s\S]*?-->/g, "");

  var restPostURL = restPath + '/.rest/pdf/download';

  var form = document.createElement("form");
  var htmlInput = document.createElement("input");
  var fileNameInput = document.createElement("input");
  var headerImagePathInput = document.createElement("input");
  var footerImagePathInput = document.createElement("input");
  var linkPageInput = document.createElement("input");

  form.method = "POST";
  form.action = restPostURL;
  form.target = "_blank";

  fileNameInput.value= fileName.replace(/\s/g, "_").replace(/\||\\|\/|\:|\*|\?|\"|\<|\>|\./g, "");
  fileNameInput.name="filename";
  form.appendChild(fileNameInput);

  htmlInput.value=html;
  htmlInput.name="html";
  form.appendChild(htmlInput);

  headerImagePathInput.value=headerImagePath;
  headerImagePathInput.name="headerImgPath";
  form.appendChild(headerImagePathInput);

  footerImagePathInput.value=footerImagePath;
  footerImagePathInput.name="footerImgPath";
  form.appendChild(footerImagePathInput);

  linkPageInput.value = window.location.href;
  linkPageInput.name = "linkPage";
  form.appendChild(linkPageInput);

  form.style.display="none";
  document.body.appendChild(form);

  form.submit();

  document.body.removeChild(form);
}

$(document).ready(function(){
$('fieldset.mod').contents().unwrap();
$('.form-row > fieldset').contents().unwrap();
});

//Tabla responsive//
$(window).resize(function(){

    if ($(window).width() <= 1100) {

        $(".table-responsive").addClass("bordeDer")

        $(".table-responsive").scroll(function(){
            event.preventDefault();
            if ($(this).scrollLeft() == 0){
                $(this).addClass("bordeDer");
                $(this).removeClass("bordeIz");
            }
            else if ($(this).scrollLeft() > $(this).width()) {
                $(this).removeClass("bordeDer");
                $(this).addClass("bordeIz");
            }
            else {
                $(this).addClass("bordeIz");
                $(this).addClass("bordeDer");
            }
        })
    }

});