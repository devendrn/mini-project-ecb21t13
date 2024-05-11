const score = await fetch('/score.json').then((response) => response.json());

const ct = document.getElementById('container');

for (let category in score.jpeg) {
  const categories = score.jpeg[category];
  for (let img in categories) {
    const file = "/reference/" + category + "/" + img + ".png"
    console.log(file)
    const image = new Image();
    image.src = file;
    image.style.width = 'var(--image-size)'
    ct.append(image);
  }
}

const style = document.documentElement.style;

const slider = document.getElementById('image-size-slider');
slider.oninput = function() {
  style.setProperty('--image-size', slider.value + "px");
}
