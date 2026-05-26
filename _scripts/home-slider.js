// Homepage sliders scroll and arrow button visibility logic

function scrollSlider(sliderId, direction) {
  const container = document.getElementById(sliderId);
  if (!container) return;
  const slideWidth = container.clientWidth;
  container.scrollBy({
    left: direction * slideWidth,
    behavior: 'smooth'
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const sliders = document.querySelectorAll(".slider-container");
  
  sliders.forEach(slider => {
    const wrapper = slider.closest(".slider-wrapper");
    if (!wrapper) return;
    
    const prevBtn = wrapper.querySelector(".slider-arrow.prev");
    const nextBtn = wrapper.querySelector(".slider-arrow.next");
    
    const updateButtons = () => {
      const scrollLeft = slider.scrollLeft;
      const maxScroll = slider.scrollWidth - slider.clientWidth;
      
      if (prevBtn) {
        if (scrollLeft <= 5) {
          prevBtn.setAttribute("disabled", "true");
          prevBtn.style.opacity = "0.2";
          prevBtn.style.pointerEvents = "none";
        } else {
          prevBtn.removeAttribute("disabled");
          prevBtn.style.opacity = "1";
          prevBtn.style.pointerEvents = "auto";
        }
      }
      
      if (nextBtn) {
        if (scrollLeft >= maxScroll - 5) {
          nextBtn.setAttribute("disabled", "true");
          nextBtn.style.opacity = "0.2";
          nextBtn.style.pointerEvents = "none";
        } else {
          nextBtn.removeAttribute("disabled");
          nextBtn.style.opacity = "1";
          nextBtn.style.pointerEvents = "auto";
        }
      }
    };
    
    slider.addEventListener("scroll", updateButtons);
    
    // Initial check (delay slightly to allow rendering)
    setTimeout(updateButtons, 300);
    
    // Re-check on window resize
    window.addEventListener("resize", updateButtons);
  });
});
