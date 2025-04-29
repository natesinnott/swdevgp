// Authored By Eeliya
// wait for page to load before runnin js
document.addEventListener("DOMContentLoaded", function () {
    // get data from backend endpoint
    fetch("/data/")
        .then((response) => response.json())
        .then((data) => {
            // get the latest date from data for y-axis label
            const latestDate = data.dates[data.dates.length - 1];
            // get the canvas ctx to draw the chart
            const ctx = document.getElementById("myTrendsChart").getContext("2d");
            // create new horizontal bar chart with data
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.dates,
                    datasets: [
                        // green dataset
                        {
                            label: "Green",
                            data: data.green,
                            backgroundColor: "rgba(75, 192, 192, 0.6)",
                        },
                        // amber dataset
                        {
                            label: "Amber",
                            data: data.amber,
                            backgroundColor: "rgba(255, 206, 86, 0.6)",
                        },
                        // red dataset
                        {
                            label: "Red",
                            data: data.red,
                            backgroundColor: "rgba(255, 99, 132, 0.6)",
                        },
                    ],
                },
                options: {
                    // make chart horizontal
                    indexAxis: "y",
                    // let chart stretch to fit container
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        // hide legend
                        legend: {
                            display: false,
                        },
                        // hide title
                        title: {
                            display: false
                        },
                    },
                    
                    scales: {
                        // show only whole numbers on x axis
                        x: {
                            ticks: {
                                callback: function(value) {
                                    return Number.isInteger(value) ? value : '';
                                }
                            }
                        },
                        // hide y axis labels and set title as latest date
                        y: {
                            ticks: {
                                callback: function() {
                                    return '';
                                }
                            },
                            title: {
                                display: true,
                                text: latestDate,
                                font: {
                                    size: 12
                                }
                            }
                        }
                    },
                },
            });
        });
});