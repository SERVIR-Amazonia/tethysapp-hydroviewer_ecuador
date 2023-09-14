// ------------------------------------------------------------------------------------------------------------ //
//                                             HTML FOR FLOOD ALERT                                             //
// ------------------------------------------------------------------------------------------------------------ //
const floodWarningsHTML = `<div class="control control-group">
                                <label class="label-control" for="select-loc">Niveles de alerta:</label>
                                <div class="alert-panel-checkbox">
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-002yr" checked>
                                        <label class="form-check-label" for="check-002yr">Periodo de retorno: 2 años</label>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-005yr" checked>
                                        <label class="form-check-label" for="check-005yr">Periodo de retorno: 5 años</label>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-010yr" checked>
                                        <label class="form-check-label" for="check-010yr">Periodo de retorno: 10 años</label>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-025yr" checked>
                                        <label class="form-check-label" for="check-025yr">Periodo de retorno: 25 años</label>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-050yr" checked>
                                        <label class="form-check-label" for="check-050yr">Periodo de retorno: 50 años</label>
                                    </div>
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-100yr" checked>
                                        <label class="form-check-label" for="check-100yr">Periodo de retorno: 100 años</label>
                                    </div>
                                </div>
                                <label class="label-control" for="select-warnings">Advertencias meteorológicas:</label>
                                <div class="alert-panel-checkbox">
                                    <div class="form-check form-switch">
                                        <input class="form-check-input" type="checkbox" id="check-warning">
                                        <label class="form-check-label" for="check-warning"> Alertas por lluvias y tormentas </label>
                                    </div>
                                    <table class="table-warning" id="table-warning-selector">
                                        <tr class="tr-warning">
                                            <th class="th-warning bajo">Bajo</th>
                                            <th class="th-warning medio">Medio</th>
                                            <th class="th-warning alto">Alto</th>
                                            <th class="th-warning muy-alto">Muy Alto</th>
                                        </tr>
                                    </table>
                                </div>
                                <br>`;

// Add HTML into the control panel
$("#flood-warnings")[0].innerHTML = floodWarningsHTML;




// ------------------------------------------------------------------------------------------------------------ //
//                                             LOAD FLOOD WARNINGS                                              //
// ------------------------------------------------------------------------------------------------------------ //
fetch("get-alerts")
    .then((response) => (layer = response.json()))
    .then((layer) => {
        est_R002 = add_station_icon(layer, "R2");
        est_R002.addTo(map);
        est_R002.on('click', showPanel)

        est_R005 = add_station_icon(layer, "R5");
        est_R005.addTo(map); 
        est_R005.on('click', showPanel)

        est_R010 = add_station_icon(layer, "R10");
        est_R010.addTo(map);
        est_R010.on('click', showPanel)

        est_R025 = add_station_icon(layer, "R25");
        est_R025.addTo(map);
        est_R025.on('click', showPanel)

        est_R050 = add_station_icon(layer, "R50");
        est_R050.addTo(map);
        est_R050.on('click', showPanel)
                
        est_R100 = add_station_icon(layer, "R100");
        est_R100.addTo(map);
        est_R100.on('click', showPanel)
    });




// ------------------------------------------------------------------------------------------------------------ //
//                                         DINAMIC SELECT FOR WARNINGS                                          //
// ------------------------------------------------------------------------------------------------------------ //   
$('#check-002yr').on('change', function () {
    if($('#check-002yr').is(':checked')){
        est_R002.addTo(map);
    } else {
        map.removeLayer(est_R002); 
    };
});
                
$('#check-005yr').on('change', function () {
    if($('#check-005yr').is(':checked')){
        est_R005.addTo(map);
    } else {
        map.removeLayer(est_R005); 
    };
});
                
$('#check-010yr').on('change', function () {
    if($('#check-010yr').is(':checked')){
        est_R010.addTo(map);
    } else {
        map.removeLayer(est_R010); 
    };
});
                
$('#check-025yr').on('change', function () {
    if($('#check-025yr').is(':checked')){
        est_R025.addTo(map);
    } else {
        map.removeLayer(est_R025); 
    };
});
                
$('#check-050yr').on('change', function () {
    if($('#check-050yr').is(':checked')){
        est_R050.addTo(map);
    } else {
        map.removeLayer(est_R050); 
    };
});
                
$('#check-100yr').on('change', function () {
    if($('#check-100yr').is(':checked')){
        est_R100.addTo(map);
    } else {
        map.removeLayer(est_R100); 
    };
});



// ------------------------------------------------------------------------------------------------------------ //
//                                       LOADING METEOROLOGICAL WARNINGS                                        //
// ------------------------------------------------------------------------------------------------------------ // 

  // Alertas meteorologicas INAMHI
warnings = L.geoJSON(null, {
  style: function (feature) {
    var color;
    if (feature.properties.Nivel === 'Muy Alto') {
      color = '#EF4C4D';
      opacity = 1;
    } else if (feature.properties.Nivel === 'Alto') {
      color = '#FFC44E';
      opacity = 1;
    } else if (feature.properties.Nivel === 'Medio') {
      color = '#FFFF4D';
      opacity = 1;
    } else {
      color = '#FFFFFF';
      opacity = 1;
    }

    return {
      fillColor: color,
      fillOpacity: opacity,
      stroke: true,
      color: color,
      weight: 1
    };
  }
});
  
// Filtrar alertas
function filter_warnings(data, nivel){
  var filteredFeatures = data.features.filter(function(feature) {
    return feature.properties.Nivel === nivel;
  });
  return(filteredFeatures )
}
  
// URL y parametros del recurso de hydroshare
var url = 'https://geoserver.hydroshare.org/geoserver/HS-e1920951d6194c78948e45ae7b08ec64/wfs';
var params = {
  service: 'WFS',
  version: '1.1.0',
  request: 'GetFeature',
  typeName: 'Advertencia',
  outputFormat: 'application/json'
}; 
  
// Carga los datos WFS utilizando AJAX y agrega los resultados a la capa geoJSON
$.ajax({
  url: url,
  data: params,
  dataType: 'json'
}).done(function(response){
    console.log("Funciona");
  alertas =  {
    type: 'FeatureCollection',
    features: filter_warnings(response, "Medio").concat(
              filter_warnings(response, "Alto"),
              filter_warnings(response, "Muy Alto")) };
  warnings.addData(alertas);
  console.log("Termina");
});


$('#check-warning').on('change', function () {
    if($('#check-warning').is(':checked')){
        warnings.addTo(map);
        var layers = warnings.getLayers();
        if (layers[0].feature.properties.Nivel === "Medio") {
            layers.reverse();
        }
        for (var i = 0; i < layers.length; i++) {
          layers[i].bringToBack();
        }
    } else {
        map.removeLayer(warnings); 
    };
}); 

$('#table-warning-selector').on('click', function () {
    $('#warning-modal').modal('show');
});