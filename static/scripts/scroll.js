const sliders = document.getElementsByClassName('suggestion-card-container')

for (i = 0; i < sliders.length; i++){
  let slider = sliders[i]
  let isDown = false;
  let startX;
  let scrollLeft;

  console.log(slider)

  slider.addEventListener('mousedown', (e) => {
    isDown = true;
    slider.classList.add('active');
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
  });
  slider.addEventListener('mouseleave', () => {
    isDown = false;
    slider.classList.remove('active');
  });
  slider.addEventListener('mouseup', () => {
    isDown = false;
    slider.classList.remove('active');
  });
  slider.addEventListener('mousemove', (e) => {
    if(!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 1.5; //scroll-fast
    slider.scrollLeft = scrollLeft - walk;
  //   console.log(walk);
  });
}


// const slider = document.getElementsByClassName('suggestion-card-container')[0];
