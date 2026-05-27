function initChart() {
  const containerId = "home-chart-container";

  const container = document.getElementById(containerId);
  const canvas = document.createElement("canvas");

  container.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  const labels = JSON.parse(document.getElementById("chart_date").textContent);
  const data = JSON.parse(document.getElementById("chart_value").textContent);
  const sellsData = JSON.parse(
    document.getElementById("chart_buy").textContent,
  );

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Total value",
          data: data,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          tension: 0.1,
          spanGaps: true,
        },
        {
          label: "Total investmented",
          data: sellsData,
          borderColor: "rgba(255, 159, 64, 1)",
          backgroundColor: "rgba(255, 159, 64, 0.2)",

          tension: 0.1,
          pointRadius: 5,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 150,
        easing: "easeOutQuad",
      },
      plugins: {
        legend: {
          position: "right",
        },
        title: {
          display: false,
        },
      },
      scales: {
        y: {
          title: {
            display: false,
          },
        },
        yEmpty: {
          type: "linear",
          position: "right",
          min: 0,
          max: 1,
          display: false,
        },
      },
    },
  });
}
initChart();
