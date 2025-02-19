//IMPORTANT: init_geo, myUrl, dlUrl, spUrl, and detUrl come from stationFinder.html
//Placeholder constants
const BCOLOR = ["black", "pink", "orange", "blue", "green", "yellow"];//List of colors for the layers of the bar graph
let X_AXIS_DEFAULT_TEXT = "State";
let place_name = "";
let popup_holder = "";
let GRAPH_MODE = "Spline ";
let URLs = myUrl;
const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    noWrap: true
})
var stateGeo = L.geoJson(stateData, {style: style, onEachFeature: onEachFeature});
var countyGeo = L.geoJson(countyData, {style: style, onEachFeature: onEachFeature});
const map = L.map('map', {
    center: init_geo,
    zoom: 4,
    layers: [tiles, stateGeo]
});
const baseLayer = {"tiles" : tiles};
const overlay = {
    //"Individual Stations" : circleLayer,
    "State" : stateGeo,
    "County" : countyGeo
};
var soilLayerBarChart = null;//Initial chart curve.
map.on('popupopen', function(e) {
    place_name = e.popup._source._tooltip._content;
    popup_holder = e.popup._source;
    graph_builder();
});
const layerControl = L.control.layers(overlay, {}).addTo(map);
var searchControl = new L.Control.Search({
    layer: stateGeo,
    propertyName: 'name',
    marker: false,
    moveToLocation: function(latlng, title, map) {
        //map.fitBounds( latlng.layer.getBounds() );
        var zoom = map.getBoundsZoom(latlng.layer.getBounds());
          map.setView(latlng, zoom); // access the zoom
    }
});
map.on("baselayerchange", function(event){
    searchControl.collapse();
    map.closePopup();
    X_AXIS_DEFAULT_TEXT = event.name;
    searchControl.setLayer(overlay[event.name]);
});
searchControl.on('search:locationfound', function(e) {
    e.layer.setStyle({fillColor: '#3f0', color: '#0f0'});
    if(e.layer._popup)
        e.layer.openPopup();

}).on('search:collapsed', function(e) {
    stateGeo.resetStyle(e.layer);
});
map.addControl( searchControl );  //inizialize search control 
const defaultScalesMap = {
    x: {
        type: "category",
        stacked: true,
        offset: true,
        title: {
            display: true,
            text: X_AXIS_DEFAULT_TEXT,
            color: "black",
            font: {
                size: 14
            }
        },
    },
    y: {
        stacked: true,
        min: 0, // This ensures the y-axis starts at 0
        reverse: true, // This reverses the y-axis
        title: {
            display: true,
            text: "Depth (cm)"
        }
    },
};
configBar = {
    maintainAspectRatio: false,
    scales: defaultScalesMap,
    plugins: {
        legend: {
            display: false
        }
    },
};
//chartId is a janky method of making the bar graphs easier to handle.
//Without this, the user would need to fully close each popup they opened before opening a new one,
//otherwise they would get an empty popup.
var chartId = 0;
const DATASET_BAR_GRAPH = 1;

function getColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
}
function style(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}
function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });
    layer.bringToFront();
}
function resetHighlight(e) {
    var layer = e.target;
    stateGeo.resetStyle(layer);
}
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
    });
    let feature_name = feature.properties.name;
    if(feature.properties.state){feature_name = feature_name + ", " + feature.properties.state;}
    layer.bindTooltip(feature_name);
    layer.bindPopup()
}
function downloadData(e){
    var site = soilLayerBarChart.options.scales.x.title.text;
    $.ajax({                       // initialize an AJAX request
        url: dlUrl,  // set the url of the request (= localhost:8000/Many_Layers/download-params/)
        data: {
            "type" : X_AXIS_DEFAULT_TEXT,
            "name" : place_name
        },
        success: function(response){
            const blob = new Blob([response], { type: 'text/csv' });
            const elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(blob);
            elem.download = site + ".csv";
            document.body.appendChild(elem);
            elem.click();
            document.body.removeChild(elem);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            alert("Status: " + textStatus); alert("Error: " + errorThrown); 
        } 
    })
    
}
function newpage(event){
    window.location.href = detUrl + "?type=" + X_AXIS_DEFAULT_TEXT + "&name=" + place_name;
}
function updateSoilSpline(event){
    if(GRAPH_MODE==="Spline "){
        GRAPH_MODE = "All ";
        URLs = spUrl;
    }
    else{
        GRAPH_MODE = "Spline ";
        URLs = myUrl;
    }
    graph_builder()

    
}
function graph_builder(){
    $.ajax({                       // initialize an AJAX request
        url: URLs,  // set the url of the request
        data: {      
            "type" : X_AXIS_DEFAULT_TEXT,
            "name" : place_name
        },
        success: function (data) {
            if(data.layer_.length == 0){
                const popupGraph = `No data to display. Sorry!`;
                popup_holder.bindPopup(popupGraph);
                return;
            }
            console.log("Starting Graph");
            if(soilLayerBarChart != null){
                soilLayerBarChart.destroy();
                //If the chartId is 1, set it to 0. If 0, set it to 1.
                //This allows us to change bar charts easily. My best guess as to why it works is it... allows the old chart time to replace the stuff it had?
                //I said it was my best guess, not a good one.
                //To see the problem with bar charts not appearing, simply comment out the line below.
                chartId = chartId == 1 ? 0 : 1;
            }
            const popupGraph = `<div><canvas id="soilLayerBarChart`+chartId+`" width="560" height="315"></canvas></div>
                                <button id="download" onclick="downloadData(event)">Download</button>
                                <button id="switch" onclick="updateSoilSpline(event)">` + GRAPH_MODE +  `View</button>
                                <a href = "` + detUrl + `?type=` + X_AXIS_DEFAULT_TEXT + `&name=` + place_name + `">Detailed View</a>`;
            console.log("Binding Graph");
            popup_holder.bindPopup(popupGraph);
            var ctxMap = document.getElementById("soilLayerBarChart"+chartId).getContext("2d");
            console.log("Making Chart");
            const dataBar = {datasets: [{type: 'bar'}]};
            soilLayerBarChart = new Chart(ctxMap, {
                // The type of chart we want to create
                type: "bar",
                // The data for our dataset
                data: dataBar,
                //The configuration details for our graph
                options: configBar
            });
            var cdd = soilLayerBarChart.data.datasets;//cdd short for chart data datasets
            const footer_keys_count = data.footer_keys.length;
            const footer = (tooltipItems) => {
                let footer_lines = [];
                tooltipItems.forEach(function(tooltipItem) {//For each layer of soil data
                    for(let i = 0; i < footer_keys_count; i++){//For each string in footer_keys
                        value = cdd[tooltipItem.datasetIndex-1][data.footer_keys[i]][tooltipItem.dataIndex];
                        if(value){//If this value exists
                            //have the following string show up.
                            footer_lines.push(data.footer_values[i] + ": " + value);
                        }
                            
                    }
                });
                return footer_lines;
            };
            soilLayerBarChart.options.scales.x.title.text = X_AXIS_DEFAULT_TEXT + ": " + place_name;//Set x-axis label
            soilLayerBarChart.options.plugins.tooltip.callbacks.footer = footer;//Set the footers.
            for(let layer_num = 0; layer_num < data.layer_.length; layer_num++){
                var newDataset = {
                    data: data.data[layer_num],
                    type : "bar",
                    label : "Layer " + data.layer_[layer_num],
                    backgroundColor : BCOLOR[layer_num % BCOLOR.length]
                };
                console.log(cdd);
                console.log(data);
                for (let i = 0; i < footer_keys_count; i++){
                    cdd[layer_num][data.footer_keys[i]] = data[data.footer_keys[i]][layer_num];
                }
                cdd.push(newDataset);
            }
            for(let i = 1; i <= cdd[DATASET_BAR_GRAPH].data.length; i++){soilLayerBarChart.data.labels.push("Sample " + i);}
            soilLayerBarChart.update();
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            alert("Status: " + textStatus); alert("Error: " + errorThrown); 
        }   
    });
}