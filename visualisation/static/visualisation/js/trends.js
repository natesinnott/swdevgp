let currentChart = null;


function fetchChartData() {

    var filters = {
        type: document.querySelector('input[name="scope"]:checked').value,
        category: document.getElementById("category").value,
        start_date: document.getElementById("start-date").value,
        end_date: document.getElementById("end-date").value,
    };

    var chartType = document.querySelector('input[name="chartType"]:checked').value;

    $.get('/trends/data/', filters, function (response) {

        console.log("Fetching with filters:", filters);
        console.log("Chart data response:", response);
        if (response.dates) {

            var ctx = document.getElementById('trends-chart').getContext('2d');

            if (currentChart) {
                currentChart.destroy();
            }


            var categoryLabel = filters.category || "All Categories";
            var chartTitle = `${categoryLabel} - ${filters.type.charAt(0).toUpperCase() + filters.type.slice(1)} Chart`;

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
                                return Number.isInteger(value) ? value : '';
                            }
                        }
                    }
                }
                
                
            }
            
        });
        } else {
            alert("Error fetching data!");
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Failed to fetch chart data:", textStatus, errorThrown);
        alert("Something went wrong while loading the chart.");
    });
}

document.getElementById('trends-filters').addEventListener('submit', function (event) {
    event.preventDefault();
    fetchChartData();
});



document.addEventListener('DOMContentLoaded', fetchChartData);

document.querySelectorAll('input[name="chartType"]').forEach(function (input) {
    input.addEventListener('change', fetchChartData);
});
