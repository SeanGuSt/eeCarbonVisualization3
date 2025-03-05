/*This just creates the initial graph we see on loading the page*/
ctx = document.getElementById("soilLayerDataLine").getContext("2d");
scales = {
    x: {
        type: "linear",
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
            labels: [0, 1, 1.2, 1.3],
            data: [0.5, 1, 2, 0.6],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
        },
        {
            type: "line",
            labels: [0, 1, 2, 3],
            data: [0.5, 1, 1.3, 2.6],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
        },
        {
            type: "line",
            labels: [0, 1, 2, 3],
            data: [2.6, 1.3, 1, 0.5],
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
            }
        },
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
            cdd[1].labels = response.x;
            cdd[1].data = response.y;
            cdd[2].labels = response.x;
            cdd[2].data = response.y1;
            soilLayerLine.update();
        }
    });
});
