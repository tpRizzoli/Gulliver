function initMap() {
  var map = document.getElementById("map");
  var lat = parseFloat(map.getAttribute("dati-lat"));
  var lng = parseFloat(map.getAttribute("dati-lng"));

  var center = { lat: lat, lng: lng };

  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: center,
  });
 var markers = [{lat: lat, lng: lng},];
  for(var i= 0; i< markers.length; i++){
      new google.maps.Marker({
      position: markers[i],
      map: map,
    });
  }
}

