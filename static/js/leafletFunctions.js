var map;
var ajaxRequest;
var plotlist;
var marker;
var plotlayers=[];
var bounds;
var longitud;
var latitud;
var visited_locations = [];
var numberOfvisits = [];
var popupMessages = [];

function initmap(map_name) {
	// set up AJAX request
	ajaxRequest =  getXmlHttpObject();
	if (ajaxRequest==null) {
	  alert ("This browser does not support HTTP Request");
	}
	map = new L.Map(map_name, {center: new L.LatLng(-33.447487, -70.673676), zoom: 12});
	//var map = new L.Map('map', {center: new L.LatLng(51.3, 0.7), zoom: 9});

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});   
	// start the map in South-East England
	map.addLayer(osm);

	return map;
}


function getXmlHttpObject() {
	if (window.XMLHttpRequest) { return new XMLHttpRequest(); }
	if (window.ActiveXObject)  { return new ActiveXObject("Microsoft.XMLHTTP"); }
	return null;
}

function askForPlots() {
	// request the marker info with AJAX for the current bounds
	//wait to getbounds
	var bounds=map.getBounds();
	var minll=bounds.getSouthWest();
	var maxll=bounds.getNorthEast();
	var msg='leaflet/findbybbox.cgi?format=leaflet&bbox='+minll.lng+','+minll.lat+','+maxll.lng+','+maxll.lat;
	ajaxRequest.onreadystatechange = stateChanged;
	ajaxRequest.open('GET', msg, true);
	ajaxRequest.send(null);
}

function stateChanged() {
	// if AJAX returned a list of markers, add them to the map
	if (ajaxRequest.readyState==4) {
		//use the info here that was returned
		if (ajaxRequest.status==200) {
			plotlist=eval("(" + ajaxRequest.responseText + ")");
			removeMarkers();
			for (i=0;i<plotlist.length;i++) {
				var plotll = new L.LatLng(plotlist[i].lat,plotlist[i].lon, true);
				var plotmark = new L.Marker(plotll);
				plotmark.data=plotlist[i];
				map.addLayer(plotmark);
				plotmark.bindPopup("<h3>"+plotlist[i].name+"</h3>"+plotlist[i].details);
				plotlayers.push(plotmark);
			}
		}
	}
}

function removeMarkers() {
	for (i=0;i<plotlayers.length;i++) {
		map.removeLayer(plotlayers[i]);
	}
	plotlayers=[];
}

function onMapMove(e) { askForPlots(); }

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

function addPath(sequence,map) {
	  var pointList = [];
      for (var i = 0; i < sequence.length; i++) {
          pointList.push(new L.LatLng(dict_latlong_stops[sequence[i]]['lat'], dict_latlong_stops[sequence[i]]['long']));
      }
      var firstpolyline = new L.polyline(pointList);
      firstpolyline.addTo(map);
}

function addMarkerByStep(sequence,pointsAdded,markerCounter) {
	latitud = dict_latlong_stops[sequence[markerCounter]]['lat'];
	longitud = dict_latlong_stops[sequence[markerCounter]]['long'];
	jobMarkerIcon = L.AwesomeMarkers.icon({
                          icon: '',
                          markerColor: 'darkblue',
                          prefix: 'fa',
                          html:(markerCounter+1)
                          });
	marker = L.marker([latitud,longitud], {icon: jobMarkerIcon});
    marker.addTo(map);
	bounds=map.getBounds();
	map.fitBounds(bounds);
}
function addMarkerSubida(sequence,netapa,nviaje, pointsAdded, markerCounter, fecha,metroOrBus){
	var par_subida = sequence[markerCounter]['subida'];
	latitud = dict_latlong_stops[par_subida]['lat'];
	longitud = dict_latlong_stops[par_subida]['long'];
	var markerMessage = "";
	var index_location = visited_locations.indexOf(par_subida);
	if(index_location<0){
		visited_locations.push(par_subida);
		index_location = visited_locations.length-1;
		numberOfvisits.push(1);
		popupMessages.push("<b>"+par_subida+"<b/>");
	}
	else{
		numberOfvisits[index_location]+=1;
	}
	if(netapa[markerCounter] == 1){
		if(par_subida.indexOf('-') && metroOrBus){
			markerColor = 'darkblue';
		}
		else if(metroOrBus){
			markerColor = 'green';
		}
		else{
			markerColor = 'green';
		}
		polyline.addLatLng(new L.LatLng(latitud, longitud));
		popupMessages[index_location] = popupMessages[index_location] + "<br>" + "Origen, viaje N°" + nviaje[markerCounter] + ", "+ fecha;
	}
	else{
		if(par_subida.indexOf('-') && metroOrBus){
			markerColor = 'darkblue';
		}
		else if(metroOrBus){
			markerColor = 'green';
		}
		else{
			markerColor = 'darkblue';
		}
		polyline.addLatLng(new L.LatLng(latitud, longitud));
		popupMessages[index_location] = popupMessages[index_location] + "<br>"+ "Transbordo, viaje N°" + nviaje[markerCounter] + ", "+ fecha;
	}
	jobMarkerIcon = L.AwesomeMarkers.icon({
                          icon: '',
                          markerColor: markerColor,
                          prefix: 'fa',
                          html:numberOfvisits[index_location]
                          });
	marker = L.marker([latitud,longitud], {icon: jobMarkerIcon});
    marker.addTo(map);
    markerMessage = popupMessages[index_location];
    marker.bindPopup(markerMessage);
}
function addMarkerBajada(sequence,netapa,nviaje, pointsAdded, markerCounter, fecha,metroOrBus){
	var par_bajada = sequence[markerCounter]['bajada'];
	latitud = dict_latlong_stops[par_bajada]['lat'];
	longitud = dict_latlong_stops[par_bajada]['long'];
	var index_location = visited_locations.indexOf(par_bajada);
	if(index_location<0){
		visited_locations.push(par_bajada);
		index_location = visited_locations.length-1;
		numberOfvisits.push(1);
		popupMessages.push("<b>"+par_bajada+"<b/>");
	}
	else{
		numberOfvisits[index_location]+=1;
	}
	if(netapa[markerCounter]>=netapa[markerCounter+1] || netapa.length-1 == markerCounter){
		if(par_bajada.indexOf('-') && metroOrBus){
			markerColor = 'darkblue';
		}
		else if(metroOrBus){
			markerColor = 'green';
		}
		else{
			markerColor = 'red';
		}
    	polyline.addLatLng(new L.LatLng(latitud, longitud));
    	polyline = L.polyline([]).addTo(map);
		popupMessages[index_location] = popupMessages[index_location] + "<br>" + "Destino, viaje N°" + nviaje[markerCounter] + ", "+ fecha;
	}
	else{
		if(par_bajada.indexOf('-') && metroOrBus){
			markerColor = 'darkblue';
		}
		else if(metroOrBus){
			markerColor = 'green';
		}
		else{
			markerColor = 'darkblue';
		}
    	polyline.addLatLng(new L.LatLng(latitud, longitud));
		popupMessages[index_location] = popupMessages[index_location] + "<br>" + "Transbordo, viaje N°" + nviaje[markerCounter] + ", "+ fecha;
    }
	jobMarkerIcon = L.AwesomeMarkers.icon({
                          icon: '',
                          markerColor: markerColor,
                          prefix: 'fa',
                          html:numberOfvisits[index_location]
                          });
	marker = L.marker([latitud,longitud], {icon: jobMarkerIcon});
    marker.addTo(map);
    markerMessage = popupMessages[index_location];
    marker.bindPopup(markerMessage);
}

function addMarker(sequence, netapa, nviaje, pointsAdded, markerCounter, fechas,metroOrBus) {
	//ver si hay subida y bajada
	if(!!sequence[markerCounter]['subida']){
		addMarkerSubida(sequence, netapa, nviaje, pointsAdded, markerCounter, fechas[markerCounter],metroOrBus);
	}
	if(!!sequence[markerCounter]['bajada']){
		addMarkerBajada(sequence, netapa, nviaje, pointsAdded, markerCounter, fechas[markerCounter],metroOrBus);
	}
	bounds=map.getBounds();
	map.fitBounds(bounds);
}

function addMarker2(sequence,pointsAdded,markerCounter) {
	latitud = dict_latlong_stops[sequence[markerCounter]]['lat'];
	longitud = dict_latlong_stops[sequence[markerCounter]]['long'];
	jobMarkerIcon = L.AwesomeMarkers.icon({
                          icon: '',
                          markerColor: 'darkblue',
                          prefix: 'fa',
                          html:(markerCounter+1)
                          });
	marker = L.marker([latitud,longitud], {icon: jobMarkerIcon});
    marker.addTo(map);
    polyline.addLatLng(new L.LatLng(dict_latlong_stops[sequence[pointsAdded]]['lat'], dict_latlong_stops[sequence[pointsAdded]]['long']));
	bounds=map.getBounds();
	map.fitBounds(bounds);
}

function addCircleRois(map,rois){
	for (i=0;i<rois.length;i++) {
		latitud = rois[i]['lat'];
		longitud = rois[i]['long'];
		//agregar tantos circulos como rois hayan en cada corte temporal
		var circle = L.circle([latitud,longitud], 500, {
		                color: 'red',
		                fillColor: '#f03',
		                fillOpacity: 0.5
		            }).addTo(map);
		//es necesario agregar el circulo a alguna parte???
	}
	
}