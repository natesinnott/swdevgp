//Authored by Eeliya
// store the current chart instance for later updates
let currentChart = null;

// function to fetch chart data based on filters and update the chart
function fetchChartData() {

    // collect filter values from the form to apply when fetching chart data
    var filters = {
        type: document.querySelector('input[name="scope"]:checked').value,
        category: document.getElementById("category").value,
        start_date: document.getElementById("start-date").value,
        end_date: document.getElementById("end-date").value,
    };

    // get selected chart type (line, bar, etc.)
    var chartType = document.querySelector('input[name="chartType"]:checked').value;

    // send GET request to fetch the trend data with applied filters
    $.get('/trends/data/', filters, function (response) {

        // check if the response contains valid data
        if (response.dates) {

            // get the canvas context for drawing the chart
            var ctx = document.getElementById('trends-chart').getContext('2d');

            // if a chart already exists, destroy it before creating a new one
            if (currentChart) {
                currentChart.destroy();
            }

            // set the chart category label based on the selected filter
            var categoryLabel = filters.category || "All Categories";
            var chartTitle = `${categoryLabel} - ${filters.type.charAt(0).toUpperCase() + filters.type.slice(1)} Chart`;

            // create a new chart instance with the fetched data
            currentChart = new Chart(ctx, {
                type: chartType,
                data: {
                    labels: response.dates,
                    datasets: [{
                        label: 'Green',
                        data: response.green,
                        borderColor: 'rgba(0, 200, 83, 1)',
                        backgroundColor: 'rgba(0, 150, 60, 0.6)',
                        hoverBackgroundColor: 'rgba(0, 200, 83, 1)',
                        fill: false
                    }, {
                        label: 'Amber',
                        data: response.amber,
                        borderColor: 'rgba(255, 193, 7, 1)',
                        backgroundColor: 'rgba(204, 153, 5, 0.6)',
                        hoverBackgroundColor: 'rgba(255, 193, 7, 1)',
                        fill: false
                    }, {
                        label: 'Red',
                        data: response.red,
                        borderColor: 'rgba(244, 67, 54, 1)',
                        backgroundColor: 'rgba(200, 50, 40, 0.6)',
                        hoverBackgroundColor: 'rgba(244, 67, 54, 1)',
                        fill: false
                    }]
                },
                // chart options for customization (e.g., title, scales)
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: chartTitle,
                            font: {
                                size: 24,
                                family: 'SkyRegular',
                            },
                            margin: {
                                top:0,
                                bottom: 70  
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                if (Number.isInteger(value)) {
                                    return value;
                                }
                                return '';
                            }
                        }
                    }
                }
            }});
        } else {
            alert("Error fetching data!");
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Failed to fetch chart data:", textStatus, errorThrown);
        alert("Something went wrong while loading the chart.");
    });
}

// add event listener to handle form submission and fetch new data
document.getElementById('trends-filters').addEventListener('submit', function (event) {
    event.preventDefault();
    fetchChartData();
});

// call fetchChartData once the page is fully loaded
document.addEventListener('DOMContentLoaded', fetchChartData);

// add event listeners to update chart when chart type changes
document.querySelectorAll('input[name="chartType"]').forEach(function (input) {
    input.addEventListener('change', fetchChartData);
});
