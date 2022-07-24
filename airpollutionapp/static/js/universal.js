//var map = L.map('map').fitWorld();
//
//L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//}).addTo(map);

var map = L.map('map',{
    zoomAnimation: false
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>'
		}).addTo(map);

map.fitWorld().zoomIn();

map.on('resize', function(e) {
    map.fitWorld({reset: true}).zoomIn();
});