function initMap() {
  var map = document.getElementById("map");
  var lat = parseFloat(map.getAttribute("dati-lat"));
  var lng = parseFloat(map.getAttribute("dati-lng"));

  var center = { lat: lat, lng: lng };

  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: center,
  });

  var marker = new google.maps.Marker({
    position: center,
    map: map,
  });
}

function loadGoogleMaps() {
  var script = document.createElement('script');
  script.src = "https://maps.googleapis.com/maps/api/js?key=&callback=initMap";
  script.defer = true;
  document.body.appendChild(script);
}

loadGoogleMaps();

