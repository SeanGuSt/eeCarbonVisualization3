/*This just creates the initial graph we see on loading the page*/
ctx = document.getElementById("soilLayerDataLine").getContext("2d");
document.getElementById("pedon_select").initHTML = document.getElementById("pedon_select").innerHTML;
graphDrawn = false;
const lower_bound_default = 0;
const initial_datasets = [{
    type: "bar",
    barThickness: 'flex',
    barPercentage: 1,
    categoryPercentage: 1,
    data: [{x: 3, y: 0.5}, {x: 2, y: 1}, {x: 1, y: 1.3}, {x: 0, y: 2.6}],
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
},
{
    type: "line",
    data: [{x: 3, y: 2.6}, {x: 2, y: 1.3}, {x: 1, y: 1}, {x: 0, y: 0.5}],
    fill: true,
    borderColor: 'rgb(202, 65, 24)',
    backgroundColor: 'rgb(202, 65, 24)',
},
{
    type: "line",
    data: [{x: 3, y: 0.5}, {x: 2, y: 1}, {x: 1, y: 1.3}, {x: 0, y: 2.6}],
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
}];
scales = {
    x: {
        type: "linear",
        min: 0,
        title: {
            display: true,
            text: "Site Spline",
            color: "black",
            font: {
                size: 14
            }
        },
    },
    y: {
        min: 0, // This ensures the y-axis starts at 0
        title: {
            display: true,
            text: "y-axis"
        }
    },
};
soilLayerLine = new Chart(ctx, {
    // The type of chart we want to create
    type: "line",
    // The data for our dataset
    data: {
        datasets: JSON.parse(JSON.stringify(initial_datasets))
      },
    //The configuration details for our graph
    options: {
        maintainAspectRatio: false,
        ticks: {
            align: 'start'
        },
        scales: scales,
        plugins: {
            legend: {
                display: false
            },
        }
    }
});
var cdd = soilLayerLine.data.datasets;//cdd short for chart data datasets
function drawGraph(){
    selectedValue = document.querySelector('input[name="pedon2avg"]:checked').value;
    inputs = selectedValue.split("_");
    std_name = document.querySelector('input[name="stan2avg"]:checked').value;
    console.log("Selected value: " + selectedValue);
    $.ajax({                       // initialize an AJAX request
        url: spUrl,
        data: {
            "type" : "Individual Site",
            "name" : inputs[1],
            "id" : inputs[2],
            "site_id" : inputs[3],
            "var" : std_name
        },
        success: function(response){
            console.log(response);
            soilLayerLine.options.scales.x.title.text = selectedValue + " Sample Spline";
            soilLayerLine.options.scales.y.title.text = std_name;
            soilLayerLine.data.labels = response.x;
            cdd[0].data = response.y0;
            cdd[2].data = response.x.map((value, index) => {
                return { x: value, y: response.y[index] };
              });
            document.getElementById("integral_lower_bound").value = lower_bound_default;
            document.getElementById("integral_upper_bound").value = Math.max(...cdd[2].data.map(item => item.x));
            soilLayerLine.update();
            redrawIntegral();
            graphDrawn = true;
        }
    });
}
function redrawIntegral(){
    x_min = $("#integral_lower_bound").val();
    x_max = $("#integral_upper_bound").val();
    selectedValue = document.querySelector('input[name="pedon2avg"]:checked').value;
    inputs = selectedValue.split("_");
    std_name = soilLayerLine.options.scales.y.title.text;
    url = arUrl + `?type=${encodeURIComponent("Individual Site")}&name=${encodeURIComponent(inputs[1])}&id=${encodeURIComponent(inputs[2])}&site_id=${encodeURIComponent(inputs[3])}&var=${encodeURIComponent(std_name)}&x_min=${encodeURIComponent(x_min)}&x_max=${encodeURIComponent(x_max)}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById("integral_output").innerHTML = "Area: " + data.area;
        cdd[1].data = data.x.map((value, index) => {
            return { x: value, y: data.y[index] };
          });
        soilLayerLine.update();
    })
}
function updateIntegralBounds(){
    if($("#integral_lower_bound").val()) {$("#integral_upper_bound").attr("min", $("#integral_lower_bound").val());}
    if($("#integral_upper_bound").val()) {$("#integral_lower_bound").attr("max", $("#integral_upper_bound").val());}
}
function downloadData(e){
    var site = soilLayerLine.options.scales.x.title.text;
    $.ajax({                       // initialize an AJAX request
        url: dlUrl,  // set the url of the request (= localhost:8000/Many_Layers/download-params/)
        data: {},
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
function updatePedonList(){
    prior_pick = document.querySelector('input[name="pedon2avg"]:checked');
    value = document.querySelector('input[name="stan2avg"]:checked').value;
    url = pdUrl + `${window.location.search}&standard=${encodeURIComponent(value)}`;
    document.getElementById("pedon_select").innerHTML = document.getElementById("pedon_select").initHTML;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        newHTML = ``;
        for (const [key, value] of Object.entries(data)){
            newHTML += `<div class="pedon-option">
                            <input class="pedon_radio" type="radio" id="${key}" name="pedon2avg" value="${key}">
                            <label for="${key}">${value}</label><br>
                        </div>`
        }
        document.getElementById("pedon_select").innerHTML = newHTML;
    })
    .then(() => {
        if(prior_pick){
            prior_in_current = document.getElementById(prior_pick.id);
            if(prior_in_current){
                prior_in_current.checked = true;
                drawGraph();
            }
            else{
                console.log(initial_datasets);
                soilLayerLine.data.datasets = initial_datasets;
                soilLayerLine.update();
                console.log(soilLayerLine.data.datasets);
            }
        }
        
    })
    
}
$(document).on('change', ".pedon_radio", function(){drawGraph();});
$(".integral_bounds").change(function(){
    updateIntegralBounds();
    if(graphDrawn){redrawIntegral();}
});
$(document).on('click', ".stan_radio", function(){updatePedonList()})
window.onload = () => {updatePedonList()};