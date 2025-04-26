document.addEventListener("DOMContentLoaded", function () {
    fetch("/data/")
        .then((response) => response.json())
        .then((data) => {
            const latestDate = data.dates[data.dates.length - 1];
            const ctx = document.getElementById("myTrendsChart").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.dates,
                    datasets: [
                        {
                            label: "Green",
                            data: data.green,
                            backgroundColor: "rgba(75, 192, 192, 0.6)",
                        },
                        {
                            label: "Amber",
                            data: data.amber,
                            backgroundColor: "rgba(255, 206, 86, 0.6)",
                        },
                        {
                            label: "Red",
                            data: data.red,
                            backgroundColor: "rgba(255, 99, 132, 0.6)",
                        },
                    ],
                },
                options: {
                    indexAxis: "y",
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        title: {
                            display: false
                        },
                    },
                    
                    scales: {
                        x: {
                            ticks: {
                                callback: function(value) {
                                    return Number.isInteger(value) ? value : '';
                                }
                            }
                        },
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