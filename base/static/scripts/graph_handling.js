/*This just creates the initial graph we see on loading the page*/
ctx = document.getElementById("soilLayerDataLine").getContext("2d");
graphDrawn = false;
const lower_bound_default = 0;
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
        labels: [0, 1, 2, 3],
        datasets: [{
            type: "bar",
            barThickness: 'flex',
            barPercentage: 1,
            categoryPercentage: 1,
            labels: [0, 1, 1.2, 1.3],
            data: [0.5, 1, 2, 0.6],
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
        }]
      },
    //The configuration details for our graph
    options: {
        maintainAspectRatio: false,
        scales: scales,
        plugins: {
            legend: {
                display: false
            },
        }
    }
});
var cdd = soilLayerLine.data.datasets;//cdd short for chart data datasets


$(document).on('click', ".pedon_radio", function(){
    selectedValue = $(this).val();
    inputs = selectedValue.split("_");
    std_name = document.querySelector('input[name="stan2avg"]:checked').value;
    console.log("Selected value: " + selectedValue);
    $.ajax({                       // initialize an AJAX request
        url: spUrl,
        data: {
            "type" : "Individual Site",
            "name" : inputs[0],
            "id" : inputs[1],
            "site_id" : inputs[2],
            "var" : std_name
        },
        success: function(response){
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
});
$(".integral_bounds").change(function(){
    updateIntegralBounds();
    if(graphDrawn){redrawIntegral();}
});
function redrawIntegral(){
    x_min = $("#integral_lower_bound").val();
    x_max = $("#integral_upper_bound").val();
    selectedValue = document.querySelector('input[name="pedon2avg"]:checked').value;
    inputs = selectedValue.split("_");
    std_name = soilLayerLine.options.scales.y.title.text;
    url = arUrl + `?type=${encodeURIComponent("Individual Site")}&name=${encodeURIComponent(inputs[0])}&id=${encodeURIComponent(inputs[1])}&site_id=${encodeURIComponent(inputs[2])}&var=${encodeURIComponent(std_name)}&x_min=${encodeURIComponent(x_min)}&x_max=${encodeURIComponent(x_max)}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById("integral_output").innerHTML = "Area: " + data.area[0];
        console.log(data.x);
        cdd[1].data = data.x.map((value, index) => {
            return { x: value, y: data.y[index] };
          });
        soilLayerLine.update();
        console.log(data.area[0]);
    })
}
function updateIntegralBounds(){
    if($("#integral_lower_bound").val()) {$("#integral_upper_bound").attr("min", $("#integral_lower_bound").val());}
    if($("#integral_upper_bound").val()) {$("#integral_lower_bound").attr("max", $("#integral_upper_bound").val());}
}
