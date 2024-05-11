// chart.js is imported in index.html

const qualities = [
    10, 20, 30, 40, 50, 60, 70, 75,  80, 85, 90, 95, 97, 100
];

const score = await fetch('/score.json').then((response) => response.json());

const ct = document.getElementById('container');

for (let format in score) {
  const categories = score[format];
  const title = document.createElement("div");
  title.innerHTML = `<hr><h2>${format}</h2>`;
  ct.append(title);

  for (let category in categories) {
    const images = categories[category];
  
    const title = document.createElement("h3");
    title.innerText = category;
    ct.append(title);

    let ms_error_dataset = [];
    let h1_error_dataset = [];

    for (let img in images) {
      let scores = images[img];
      let ms_error = [];
      let h1_error = [];

      for (var i = 0; i < scores.size_ratio.length; i++) {
        ms_error.push({
          x: scores.size_ratio[i],
          y: scores.ms_error[i]
        });
        h1_error.push({
          x: scores.size_ratio[i],
          y: scores.h1_error[i]
        });
      }

      ms_error_dataset.push(
        { label: img, data: ms_error, fill: false, tension: 0.1 }
      );
      h1_error_dataset.push(
        { label: img, data: h1_error, fill: false, tension: 0.1 }
      );
    }

    const canvas1 = document.createElement("canvas");
    const canvas2 = canvas1.cloneNode();

    new Chart(canvas1, {
      type: 'line',
      data: { datasets: ms_error_dataset },
      options: {
        responsive: true,
        scales: { x: { type: 'linear', min: 0, max: 1, ticks: { stepSize: 0.1 }}, y: { beginAtZero: true } },
        plugins: { title: { display: true, text: 'MS Error' } }
      }
    });


    new Chart(canvas2, {
      type: 'line',
      data: { datasets: h1_error_dataset },
      options: {
        responsive: true,
        scales: { x: { type: 'linear', min: 0, max: 1, ticks: { stepSize: 0.1 }}, y: { beginAtZero: true } },
        plugins: { title: { display: true, text: 'H1 Error' } }
      }
    });

    const canvas_container1 = document.createElement("div");
    canvas_container1.classList.add('chart');
    const canvas_container2 = canvas_container1.cloneNode();
  
    canvas_container1.append(canvas1);
    canvas_container2.append(canvas2);

    const row = document.createElement("div");
    row.classList.add('chart-row');
    row.append(canvas_container1);
    row.append(canvas_container2);

    ct.append(row);
  }
}
