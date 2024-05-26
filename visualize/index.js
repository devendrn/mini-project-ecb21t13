// chart.js is imported in index.html

const qualities = [
    10, 20, 30, 40, 50, 60, 70, 75,  80, 85, 90, 95, 97, 100
];

const score = await fetch('/score.json').then((response) => response.json());

const ct = document.getElementById('container');

let formats = "";
for (let it in score) {
  formats = formats + `<option value="${it}">${it.toUpperCase()}</option>`;
}

const grades = ["vbe", "mse"];
let errors = "";
grades.forEach(it => {
  errors = errors + `<option value="${it}">${it.toUpperCase()}</option>`;
});

ct.innerHTML = `
<input type="range" min="100" max="800" value="300" id="chart-aspect-slider">
<select id="selected-format">${formats}</select>
<select id="selected-error">${errors}</select>
<select id="selected-category1"></select>
<select id="selected-category2"></select>
`;
const sel_f = document.getElementById('selected-format');
const sel_e = document.getElementById('selected-error');
const sel_c1 = document.getElementById('selected-category1');
const sel_c2 = document.getElementById('selected-category2');

sel_f.onchange = plot;
sel_e.onchange = plot;
sel_c1.onchange = plot;
sel_c2.onchange = plot;

const style = document.documentElement.style;
const slider = document.getElementById('chart-aspect-slider');
slider.oninput = function() {
  style.setProperty('--chart-height', slider.value + "px");
}

const canvas = document.createElement("canvas");
Chart.defaults.font = {
  family: "serif",
  size: 15
};
const ch = new Chart(canvas, {
  type: 'line',
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: { 
      // x: { type: 'linear', min: 0, max: 0.7, ticks: { stepSize: 0.1 }},
      x: { type: 'linear', min: 0, max: 0.8, ticks: { stepSize: 0.1 }},
      y: { title: "hie", beginAtZero: true } 
    }
  }
});
const chart_ct = document.createElement('div');
chart_ct.className = "chart-container"
chart_ct.append(canvas);
ct.append(chart_ct);

plot();

function plot() {
  const categories = score[sel_f.value];

  const prev_sc1 = sel_c1.value;
  const prev_sc2 = sel_c2.value;
  let categories_opt = '<option value="null">null</option>';
  for (let it in categories) {
    categories_opt = categories_opt + `<option value="${it}">${it}</option>`;
  } 
  sel_c1.innerHTML = categories_opt;
  sel_c2.innerHTML = categories_opt;
  if (prev_sc1 != "") {
    sel_c1.value = prev_sc1;
    sel_c2.value = prev_sc2;
  }

  let categories_selected = [sel_c1.value];
  if (sel_c1.value != sel_c2.value) {
    categories_selected.push(sel_c2.value);
  }

  let error_dataset = [];
  categories_selected.forEach(cat => {
    if (cat == null) {
      return;
    }
    const images = categories[cat];
    for (let img in images) {
      let scores = images[img];
      let error_scores = [];

      for (var i = 0; i < scores.size_ratio.length; i++) {
        let error_scores_raw;
        if (sel_e.value == "mse") {
          error_scores_raw = scores.ms_error[i];
        } else {
          error_scores_raw = scores.h1_error[i];
        }
        error_scores.push({
          x: scores.size_ratio[i],
          y: error_scores_raw
        });
      }
      error_dataset.push(
        { label: img, data: error_scores, fill: false, tension: 0.1 }
      );
    }
  });

  ch.data.datasets = error_dataset;
  ch.options.scales.x.title = {
    text: "1/CR", display: true
  }
  ch.options.scales.y.title = {
    text: sel_e.value.toUpperCase(), display: true
  }
  ch.update();
}
