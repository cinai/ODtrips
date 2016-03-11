var map;
var ajaxRequest;
var plotlist;
var marker;
var plotlayers=[];
var bounds;
var longitud;
var latitud;

function initmap() {
	// set up AJAX request
	ajaxRequest =  getXmlHttpObject();
	if (ajaxRequest==null) {
	  alert ("This browser does not support HTTP Request");
	}
	var map = new L.Map('map', {center: new L.LatLng(-33.447487, -70.673676), zoom: 12});
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
          pointList.push(new L.LatLng(dict_latlong_metro[sequence[i]]['lat'], dict_latlong_metro[sequence[i]]['long']));
      }
      var firstpolyline = new L.polyline(pointList);
      firstpolyline.addTo(map);
}
function addMarker(sequence,pointsAdded,markerCounter) {
	latitud = dict_latlong_metro[sequence[markerCounter]]['lat'];
	longitud = dict_latlong_metro[sequence[markerCounter]]['long'];
	jobMarkerIcon = L.AwesomeMarkers.icon({
                          icon: '',
                          markerColor: 'darkblue',
                          prefix: 'fa',
                          html:(markerCounter+1)
                          });
	marker = L.marker([latitud,longitud], {icon: jobMarkerIcon});
    marker.addTo(map);
    polyline.addLatLng(new L.LatLng(dict_latlong_metro[sequence[pointsAdded]]['lat'], dict_latlong_metro[sequence[pointsAdded]]['long']));
	bounds=map.getBounds();
	map.fitBounds(bounds);
}

function add() {
    // `addLatLng` takes a new latLng coordinate and puts it at the end of the
    // line. You optionally pull points from your data or generate them. Here
    // we make a sine wave with some math.
    polyline.addLatLng(new L.LatLng(dict_latlong_metro[sequence[pointsAdded]]['lat'], dict_latlong_metro[sequence[pointsAdded]]['long']));
    pointsAdded++;
    //map.setView([0, pointsAdded], 3);
    bounds=map.getBounds();
    map.fitBounds(bounds);
    polyline.setStyle({
	    color: 'black',
	    weight: 8
	});

}


var Colors = [
    "#FF0000", 
    "#00FF00", 
    "#0000FF", 
    "#FFFFFF", 
    "#000000", 
    "#FFFF00", 
    "#00FFFF", 
    "#FF00FF"
];

