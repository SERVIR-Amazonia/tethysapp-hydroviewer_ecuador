// ------------------------------------------------------------------------------------------------------------ //
//                                              INITIALIZE THE MAP                                              //
// ------------------------------------------------------------------------------------------------------------ //

// Set the map container
var map = L.map("map-container", {
    zoomControl: false,
}).setView([-1.7, -78.5], 7);


// Add the base map
L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);


// Add the zoom control
L.control.zoom({ 
    position: "bottomright"
}).addTo(map);


// Add drainage network
fetch('https://geoserver.hydroshare.org/geoserver/HS-77951ba9bcf04ac5bc68ae3be2acfd90/wfs?service=WFS&version=1.1.0&request=GetFeature&typeName=ecuador-geoglows-drainage&outputFormat=application/json', {
    method: 'GET',
    headers: {'Content-Type': 'application/json'}
})
.then(response => response.json())
.then(data => {
    rivers = L.geoJSON(data, {
        style: {
            weight: 1,
            color: "#4747C9",
            zIndex: 10000
        }
    }).addTo(map);
    // Buffer to select rivers
    rivers.bringToFront();
    map.almostOver.addLayer(rivers);
    // On click function
    map.on('almost:click', showPanel);
})
.catch(error => console.error('Error fetching data:', error));
















// --------------------------------------------------------------------------
$('.sub-menu ul').hide();
$('.active').show();
$('.active-angle').find(".fa-light").toggleClass("fa-angle-up");

$(".sub-menu a").click(function () {
	$(this).parent(".sub-menu").children("ul").slideToggle("100");
	$(this).find(".fa-light").toggleClass("fa-angle-up");
});

 