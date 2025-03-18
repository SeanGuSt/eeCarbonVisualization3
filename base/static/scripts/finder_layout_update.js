//IMPORTANT: init_geo, myUrl, dlUrl, spUrl, and detUrl come from stationFinder.html
//Placeholder constants
const BCOLOR = ["black", "pink", "orange", "blue", "green", "yellow"];//List of colors for the layers of the bar graph
let X_AXIS_DEFAULT_TEXT = "State";
let place_name = "";
let popup_holder = "";
let GRAPH_MODE = "Spline ";
let URLs = myUrl;
const area_tolerance = 100000;
const initial_popup = `<div class="spinner">
                            <span class="dot">.</span>
                            <span class="dot">.</span>
                            <span class="dot">.</span>
                            <span class="dot">.</span>
                            <span class="dot">.</span>
                        </div>
                        <p>Please wait...</p>`;
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
    layer.bindPopup(initial_popup)
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
// Create a layer group for the drawing features
const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Set up the drawing control to allow only rectangle drawing
const drawControl = new L.Control.Draw({
    draw: {
        polygon: false,
        polyline: false,
        circle: false,
        marker: false,
        circlemarker: false,
        rectangle: true, // Enable rectangle drawing
    },
    edit: {
        featureGroup: drawnItems, // Group to manage drawn shapes
        remove: true // Enable feature removal
    }
});
map.addControl(drawControl);

// Function to calculate the area of the rectangle in square kilometers
function calculateArea(cc) {
    console.log(cc);
    // Create the polygon from the bounding box
    const polygon = turf.bboxPolygon([cc.NW.lng, cc.NW.lat, cc.SE.lng, cc.SE.lat]);

    // Get the area of the polygon (in square meters)
    const areaInSqMeters = turf.area(polygon);

    // Convert to square kilometers
    return areaInSqMeters / 1e6;
}

function popup_prep(layer, cc){
    layer.bindPopup();
    X_AXIS_DEFAULT_TEXT = "Rectangle";
    console.log(`${cc.NW.lng}_${cc.NW.lat}_${cc.SE.lng}_${cc.SE.lat}`);
    layer.bindTooltip(`${cc.NW.lng}_${cc.NW.lat}_${cc.SE.lng}_${cc.SE.lat}`);
    layer.openPopup();
}

// Listen for the creation of a rectangle
map.on('draw:created', function (e) {
    const layer = e.layer;
    drawnItems.addLayer(layer);
    
    // Get the coordinates of the rectangle
    const bounds = layer.getBounds();
    const cornerCoordinates = {
        "NW": bounds.getNorthWest(),
        "SE": bounds.getSouthEast()
    };
    area = calculateArea(cornerCoordinates);
    // If the area exceeds the tolerance, show a confirmation
    if (area > area_tolerance) {
        // Show the warning message with area details
        const confirmMessage = `Warning! The area of the rectangle is ${area.toFixed(2)} km², which exceeds the tolerance of ${area_tolerance} km². Do you want to continue?`;

        // Ask the user to confirm if they want to proceed
        if (confirm(confirmMessage)) {
            // User clicked 'Yes', proceed with opening the popup
            popup_prep(layer, cornerCoordinates);
        } else {
            // User clicked 'No', remove the rectangle and stop
            drawnItems.removeLayer(layer);
        }
    } else {
        // If the area is within tolerance, proceed normally
        popup_prep(layer, cornerCoordinates);
    }
    // Open the popup automatically after drawing the rectangle
    //layer.openPopup();

    // Allow the user to right-click to remove the rectangle
    layer.on('contextmenu', function () {
        drawnItems.removeLayer(layer);
    });
});
function graph_builder(){
    url = URLs + `?type=${encodeURIComponent(X_AXIS_DEFAULT_TEXT)}&name=${encodeURIComponent(place_name)}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        // Check if there's any data to display, otherwise show a popup with a message
        if (data.layer_.length === 0) {
            const popupGraph = `No data to display. Sorry!`;
            popup_holder.bindPopup(popupGraph);  // Bind the popup to the map
            return;  // Exit the function early if no data
        }
        
        console.log("Starting Graph");

        // If a chart already exists, destroy it before creating a new one
        if (soilLayerBarChart !== null) {
            soilLayerBarChart.destroy();
            // Toggle chartId between 1 and 0, allowing us to easily switch between charts
            //If the chartId is 1, set it to 0. If 0, set it to 1.
            //My best guess as to why this is necessary is it... allows the old chart time to replace the stuff it had?
            //I said it was my best guess, not a good one.
            //To see the problem with bar charts not appearing, simply comment out the line below.
            chartId = chartId === 1 ? 0 : 1;
        }

        // Prepare the popup HTML with a canvas for the chart and buttons for downloading or switching views
        const popupGraph = `<div><canvas id="soilLayerBarChart` + chartId + `" width="560" height="315"></canvas></div>
                            <button id="download" onclick="downloadData(event)">Download</button>
                            <button id="switch" onclick="updateSoilSpline(event)">` + GRAPH_MODE + `View</button>
                            <a href = "` + detUrl + `?type=` + X_AXIS_DEFAULT_TEXT + `&name=` + place_name + `">Detailed View</a>`;
        console.log("Binding Graph");
        popup_holder.bindPopup(popupGraph);  // Bind the graph to the popup

        // Get the context of the canvas for Chart.js
        var ctxMap = document.getElementById("soilLayerBarChart" + chartId).getContext("2d");
        console.log("Making Chart");

        // Initialize the bar chart with empty data
        const dataBar = { datasets: [{ type: 'bar' }] };
        soilLayerBarChart = new Chart(ctxMap, {
            type: "bar",  // Chart type (bar chart)
            data: dataBar,  // Data for the chart
            options: configBar  // Chart configuration options
        });

        // Get the chart datasets
        var cdd = soilLayerBarChart.data.datasets;
        const footer_keys_count = data.footer_keys.length;

        // Create a custom footer for the chart tooltips
        const footer = (tooltipItems) => {
            let footer_lines = [];
            tooltipItems.forEach(function(tooltipItem) {
                for (let i = 0; i < footer_keys_count; i++) {
                    // Get the value for each footer key and show it in the tooltip
                    value = cdd[tooltipItem.datasetIndex - 1][data.footer_keys[i]][tooltipItem.dataIndex];
                    if (value) {
                        footer_lines.push(data.footer_values[i] + ": " + value);  // Append the footer line
                    }
                }
            });
            return footer_lines;  // Return the footer content
        };

        // Set the x-axis label for the chart
        soilLayerBarChart.options.scales.x.title.text = X_AXIS_DEFAULT_TEXT + ": " + place_name;
        // Assign the footer function to the tooltip plugin
        soilLayerBarChart.options.plugins.tooltip.callbacks.footer = footer;

        // Loop through the layers and add a dataset for each one
        for (let layer_num = 0; layer_num < data.layer_.length; layer_num++) {
            var newDataset = {
                data: data.data[layer_num],  // Data for the layer
                type: "bar",  // Dataset type (bar)
                label: "Layer " + data.layer_[layer_num],  // Label for the layer
                backgroundColor: BCOLOR[layer_num % BCOLOR.length]  // Color for the bars
            };
            // Update the chart's dataset with the footer values
            for (let i = 0; i < footer_keys_count; i++) {
                cdd[layer_num][data.footer_keys[i]] = data[data.footer_keys[i]][layer_num];
            }
            cdd.push(newDataset);  // Add the new dataset to the chart
        }

        // Add labels for each sample to the chart
        for (let i = 1; i <= cdd[DATASET_BAR_GRAPH].data.length; i++) {
            soilLayerBarChart.data.labels.push("Sample " + i);
        }

        // Update the chart to reflect the new data
        soilLayerBarChart.update();
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation
        console.error("Error fetching data:", error);
        alert("An error occurred while loading the graph.");
    });
}

