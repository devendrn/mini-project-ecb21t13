// chart.js is imported in index.html

const qualities = [
    10, 20, 30, 40, 50, 60, 70, 75,  80, 85, 90, 95, 97, 100
];

const score = await fetch('../score.json').then((response) => response.json());

const ct = document.getElementById('container');

for (let format in score) {
  const categories = score[format];
  const title = document.createElement("div");
  title.innerHTML = `<hr><h2>${format}</h2>`;
  ct.append(title);

  for (let category in categories) {
    const images = categories[category];
    console.log(images);
  
    const title = document.createElement("h3");
    title.innerText = category;
    ct.append(title);

    let size_ratio_dataset = [];
    let ms_error_dataset = [];

    for (let img in images) {
      let scores = images[img];

      size_ratio_dataset.push(
        { label: img, data: scores.size_ratio, fill: false, tension: 0.1 }
      );

      ms_error_dataset.push(
        { label: img, data: scores.ms_error, fill: false, tension: 0.1 }
      );
    }

    const row = document.createElement("div");
    row.classList.add('flex-row');

    const canvas1 = document.createElement("canvas");
    const canvas2 = document.createElement("canvas");

    new Chart(canvas1, {
      type: 'line',
      data: { labels: qualities, datasets: size_ratio_dataset },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } },
        plugins: { title: { display: true, text: 'Size ratio' } }
      }

    });

    new Chart(canvas2, {
      type: 'line',
      data: { labels: qualities, datasets: ms_error_dataset },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } },
        plugins: { title: { display: true, text: 'MS Error' } }
      }
    });

    row.append(canvas1);
    row.append(canvas2);
    ct.append(row);
  }
}
