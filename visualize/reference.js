const diff_data = await fetch('/diff.json').then((response) => response.json());

const ct = document.getElementById('container');
const dct = document.getElementById('diff-container');

for (let img in diff_data.images) {
  const filename = diff_data.images[img];
  const image = new Image();
  image.loading = "lazy";
  image.src = "reference/" + filename + ".png";
  ct.append(image);
}

let formats = "";
diff_data.formats.forEach(it => {
  formats = formats + `<option value="${it}">${it.toUpperCase()}</option>`;
})

let images = "";
diff_data.images.forEach(it => {
  images = images + `<option value="${it}">${it}</option>`;
})

let qualities = "";
for (let it in diff_data.qualities) {
  qualities = qualities + `<option value="${it}">${diff_data.qualities[it]}%</option>`;
}

let modes = `
<option value="compressed">Normal</option>
<option value="diff/ms_error">Difference MS</option>
<option value="diff/h1_error">Difference H1</option>
`;

let oimg = new Image();
let cimg1 = new Image();
let cimg2 = new Image();

dct.innerHTML = `
<input type="range" min="100" max="500" value="360" id="comp-image-size-slider">
<select id="selected-format">${formats}</select>
<select id="selected-image">${images}</select>
<select id="selected-mode">${modes}</select>
<select id="selected-quality-1">${qualities}</select>
<select id="selected-quality-2">${qualities}</select>
<input id="comment1-input">
<input id="comment2-input">
<div id="labels" class="label-row">
</div>
<div id="comparision-row" class="c-img-row">
</div>
`;

const sel_f = document.getElementById('selected-format');
const sel_i = document.getElementById('selected-image');
const sel_m = document.getElementById('selected-mode');
const sel_q1 = document.getElementById('selected-quality-1');
const sel_q2 = document.getElementById('selected-quality-2');
const label_input1 = document.getElementById('comment1-input');
const label_input2 = document.getElementById('comment2-input');
const crow = document.getElementById('comparision-row');
const labels = document.getElementById('labels');

crow.append(oimg);
crow.append(cimg1);
crow.append(cimg2);

const comment1 = document.createElement('span');
const comment2 = document.createElement('span');
labels.append(document.createElement('span'));
labels.append(comment1);
labels.append(comment2);

updateImageSelection();

const style = document.documentElement.style;

const slider = document.getElementById('image-size-slider');
slider.oninput = function() {
  style.setProperty('--r-img-size', slider.value + "px");
}

const cslider = document.getElementById('comp-image-size-slider');
cslider.oninput = function() {
  style.setProperty('--c-img-size', cslider.value + "px");
}

sel_m.onchange = updateImageSelection;
sel_f.onchange = updateImageSelection;
sel_i.onchange = updateImageSelection;
sel_q1.onchange = updateImageSelection;
sel_q2.onchange = updateImageSelection;
label_input1.onchange = updateImageSelection;
label_input2.onchange = updateImageSelection;

function updateImageSelection() {
  comment1.textContent = label_input1.value;
  comment2.textContent = label_input2.value;
  oimg.src = `reference/${sel_i.value}.png`;

  const cimg = `${sel_m.value}/${sel_f.value}/${sel_i.value.replace("/","_-_")}_-_`;

  const cimg1s = cimg + diff_data.qualities[sel_q1.value];
  const cimg2s = cimg + diff_data.qualities[sel_q2.value];

  if (sel_m.value === "compressed") {
    cimg1.src = cimg1s + `.${sel_f.value}`;
    cimg2.src = cimg2s + `.${sel_f.value}`;
  } else {
    cimg1.src = cimg1s + ".jpg";
    cimg2.src = cimg2s + ".jpg";
  }
}
