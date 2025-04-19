document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById("trends-chart").getContext("2d");
  
    // TODO: read filter values from the DOM (category, quarters, scope)
    const params = new URLSearchParams({
      category:   "",
      start_q:    "",
      end_q:      "",
      scope:      "individual",
    });
  
    // Fetch the data from Django
    fetch(`/trends/data/?${params}`)
      .then(res => res.json())
      .then(json => {
        // TODO: validate json contains {quarters, great, decent, terrible}
        new Chart(ctx, {
          type: "line",
          data: {
            labels: json.quarters,
            datasets: [
              {
                label: "Great",
                data: json.great,
                borderColor: "green",      // styling can be overridden in CSS after logic implemented
                fill: false,
              },
              {
                label: "Decent",
                data: json.decent,
                borderColor: "orange",
                fill: false,
              },
              {
                label: "Terrible",
                data: json.terrible,
                borderColor: "red",
                fill: false,
              },
            ]
          },
          options: {
            // TODO: chart.js tweaks for display
          }
        });
      })
      .catch(err => console.error("Failed to load trend data:", err));
  });