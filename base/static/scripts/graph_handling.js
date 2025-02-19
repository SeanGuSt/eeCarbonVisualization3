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


$(".site_radio").click(function(){
    selectedValue = $(this).val();
    inputs = selectedValue.split("_");
    // Hide all pedon option sections
    const allPedonSections = document.querySelectorAll('.pedon-options');
    allPedonSections.forEach(function(section) {
        section.style.display = 'none';
    });

    // Show the pedon section for the selected site
    const pedonSection = document.getElementById('pedons_of_' + inputs[0] + "_" + inputs[1] + "_" + inputs[2]);
    if (pedonSection) {
        pedonSection.style.display = 'block';
    }
    const url = pdUrl + `?type=${encodeURIComponent("Individual Station")}&name=${encodeURIComponent(inputs[0])}&site_id=${encodeURIComponent(inputs[1])}&site_source=${encodeURIComponent(inputs[2])}`;

    // Perform the fetch request
    fetch(url)
    .then(response => response.json())
    .then(data => {
        pedonSection.innerHTML = '<p>No pedons available for this site.</p>'; // Clear previous pedons if any
        if (data.pedons.length > 0) {
            pedonSection.innerHTML = '';
            data.pedons.forEach(pedon => {
                const radioBtn = document.createElement('input');
                radioBtn.type = 'radio';
                radioBtn.className = 'pedon_radio'
                radioBtn.id = 'pedon_' + pedon.name + "_" + pedon.pedon_id;
                radioBtn.name = 'pedon_' + inputs[0];
                radioBtn.value = pedon.name + "_" + pedon.pedon_id;;

                const label = document.createElement('label');
                label.setAttribute('for', 'pedon_' + pedon.name + "_" + pedon.pedon_id);
                label.innerText = pedon.name;

                pedonSection.appendChild(radioBtn);
                pedonSection.appendChild(label);
                pedonSection.appendChild(document.createElement('br'));
            });
        }
    });
});


$(document).on('click', ".pedon_radio", function(){
    selectedValue = $(this).val();
    inputs = selectedValue.split("_");
    console.log("Selected value: " + selectedValue);
    $.ajax({                       // initialize an AJAX request
        url: spUrl,
        data: {
            "type" : "Individual Station",
            "name" : inputs[0],
            "id" : inputs[1],
            "var" : ""
        },
        success: function(response){
            soilLayerLine.options.scales.x.title.text = selectedValue + " Samples' Averaged Spline";
            soilLayerLine.data.labels = response.x;
            cdd[0].data = response.y0;
            cdd[1].labels = response.x;
            cdd[1].data = response.y;
            cdd[2].labels = response.x;
            cdd[2].data = response.y1;
            soilLayerLine.update();
            console.log(cdd[0])
        }
    });
});
