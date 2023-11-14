 // ------------------------------------------------------------------------------------------------------------ //
//                                             HTML FOR FLOOD ALERT                                             //
// ------------------------------------------------------------------------------------------------------------ //
const droughtWarningsHTML = `<div class="control control-group">
                            <div class="alert-panel-checkbox">
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="check-d-medio">
                                    <label class="form-check-label" for="check-d-medio">Estiaje moderado</label>
                                </div>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="check-d-alto">
                                    <label class="form-check-label" for="check-d-alto">Estiaje alto</label>
                                </div>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="check-d-muy-alto">
                                    <label class="form-check-label" for="check-d-muy-alto">Estiaje severo</label>
                                </div>
                            </div>
                            <br>`;

// Add HTML into the control panel
$("#drougth-warnings")[0].innerHTML = droughtWarningsHTML;



// ------------------------------------------------------------------------------------------------------------ //
//                                            LOAD DROUGHT WARNINGS                                             //
// ------------------------------------------------------------------------------------------------------------ //
fetch("get-alerts-drought")
    .then((response) => (layer = response.json()))
    .then((layer) => {
        est_S1 = add_station_icon_drought(layer, "S1");
        //est_S1.addTo(map);
        est_S1.on('click', showPanel)

        est_S2 = add_station_icon_drought(layer, "S2");
        //est_S2.addTo(map); 
        est_S2.on('click', showPanel)

        est_S3 = add_station_icon_drought(layer, "S3");
        //est_S3.addTo(map);
        est_S3.on('click', showPanel)
    });


// ------------------------------------------------------------------------------------------------------------ //
//                                         DINAMIC SELECT FOR WARNINGS                                          //
// ------------------------------------------------------------------------------------------------------------ //   
$('#check-d-medio').on('change', function () {
    if($('#check-d-medio').is(':checked')){
        est_S1.addTo(map);
    } else {
        map.removeLayer(est_S1); 
    };
});
                
$('#check-d-alto').on('change', function () {
    if($('#check-d-alto').is(':checked')){
        est_S2.addTo(map);
    } else {
        map.removeLayer(est_S2); 
    };
});
                
$('#check-d-muy-alto').on('change', function () {
    if($('#check-d-muy-alto').is(':checked')){
        est_S3.addTo(map);
    } else {
        map.removeLayer(est_S3); 
    };
});
 