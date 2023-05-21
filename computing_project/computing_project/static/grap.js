const barCanvas = document.getElementById
("barCanvas");
 
const barChart = new Chart(barCanvas, {
    type: "bar",
    data: {
      labels: ["Being", "Tokyo", "Hong"],
      datasets: [{
        data: [240, 140, 120],
        backgroundColor: [
          "crimson",
          "light",
          "lightblue",
          "violet"
        ]
      }]
    },
    options: {
      scales: {
        y: {
          suggestedMax: 500,
          ticks: {
            font: {
              size: 18
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: 18
            }
          }
        }
      }
    }
  });
  