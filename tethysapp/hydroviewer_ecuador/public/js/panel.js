// ------------------------------------------------------------------------------------------------------------ //
//                                            PANEL DATA INFORMATION                                            //
// ------------------------------------------------------------------------------------------------------------ //
const sleep = ms => new Promise(r => setTimeout(r, ms));
var global_comid;
var loader = `<div class="loading-container" style="height: 350px; padding-top: 12px;"> 
                <div class="loading"> 
                  <h2>LOADING DATA</h2>
                  <span></span><span></span><span></span><span></span><span></span><span></span><span></span> 
                </div>
              </div>`; 


async function get_data_station(comid, name, lat, lon, loc1, loc2){
    // Updating the comid
    global_comid = comid
    
    // Add data to the panel
    $("#station-comid-custom").html(`<b>COMID:</b> &nbsp ${comid}`)
    $("#station-river-custom").html(`<b>RIO:</b> &nbsp ${name}`)
    $("#station-latitude-custom").html(`<b>LATITUD:</b> &nbsp ${lat}`)
    $("#station-longitude-custom").html(`<b>LONGITUD:</b> &nbsp ${lon}`)
    $("#station-locality1-custom").html(`<b>PROVINCIA:</b> &nbsp ${loc1}`)
    $("#station-locality2-custom").html(`<b>CANTÓN:</b> &nbsp ${loc2}`) 

    // Add the dynamic loader
    $("#hydrograph").html(loader)
    $("#visual-analisis").html(loader)
    $("#metrics").html(loader)
    $("#forecast").html(loader)
    $("#corrected-forecast").html(loader)

    // We need stop 300ms to obtain the width of the panel-tab-content
    await sleep(300);

    // Retrieve the data
    $.ajax({
        type: 'GET', 
        url: "get-data",
        data: {
            comid: comid,
            width: `${$("#panel-tab-content").width()}`
        }
    }).done(function(response){
        $("#modal-body-panel-custom").html(response)
    })
}


// Show data panel
function showPanel(e) {
    var comid = e.layer.feature.properties.comid;
    var name = e.layer.feature.properties.river;
    var lat = e.layer.feature.properties.latitude;
    var lon = e.layer.feature.properties.longitude;
    var loc1 = e.layer.feature.properties.loc1;
    var loc2 = e.layer.feature.properties.loc2;
    $("#panel-modal").modal("show")
    get_data_station(comid, name, lat, lon, loc1, loc2)
}