const createLineChart = (data, canvasId) => {
  const title = data.title;
  const episodeNumbers = data.episodes.map((ep) => {
    return ep.episodeNumber;
  });
  const imdbRatings = data.episodes.map((ep) => {
    return ep.imDbRating;
  });
  const lowestRating = Math.min(
    ...imdbRatings.map((rating) => {
      return Number(rating);
    })
  );

  const ctx = document.getElementById(canvasId).getContext("2d");

  Chart.defaults.font.size = 12;

  const lineChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: episodeNumbers,
      datasets: [
        {
          label: `"${title}"  Season #1 - IMDB ratings per episode`,
          data: imdbRatings,
          borderColor: "rgb(255, 30, 0)",
          fill: false,
          tension: 0,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: "Episodes",
          },
        },
        y: {
          title: {
            display: true,
            text: "Ratings",
          },
          min: lowestRating - 1,
          max: 10,
        },
      },
    },
  });
};

// results.html js
const mockData = {
  title: "Stranger Things",
  episodes: [
    {
      episodeNumber: "1",
      imDbRating: "8.6",
    },
    {
      episodeNumber: "2",
      imDbRating: "8.5",
    },
    {
      episodeNumber: "3",
      imDbRating: "8.9",
    },
    {
      episodeNumber: "4",
      imDbRating: "9.0",
    },
    {
      episodeNumber: "5",
      imDbRating: "8.8",
    },
    {
      episodeNumber: "6",
      imDbRating: "8.9",
    },
    {
      episodeNumber: "7",
      imDbRating: "9.1",
    },
    {
      episodeNumber: "8",
      imDbRating: "9.4",
    },
  ],
};
createLineChart(mockData, "ratings-line-chart");
