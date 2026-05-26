// Homepage sliders scroll and circular wrap-around logic

function scrollSlider(sliderId, direction) {
  const container = document.getElementById(sliderId);
  if (!container) return;
  
  const slideWidth = container.clientWidth;
  const currentScroll = container.scrollLeft;
  const maxScroll = container.scrollWidth - container.clientWidth;
  
  // Cyclic navigation:
  // Next on last slide -> go to first slide
  if (direction === 1 && currentScroll >= maxScroll - 15) {
    container.scrollTo({
      left: 0,
      behavior: 'smooth'
    });
  }
  // Prev on first slide -> go to last slide
  else if (direction === -1 && currentScroll <= 15) {
    container.scrollTo({
      left: maxScroll,
      behavior: 'smooth'
    });
  }
  // Regular scroll
  else {
    container.scrollBy({
      left: direction * slideWidth,
      behavior: 'smooth'
    });
  }
}

// Keep button opacities clean but fully functional without disabling them
document.addEventListener("DOMContentLoaded", () => {
  const sliders = document.querySelectorAll(".slider-container");
  
  sliders.forEach(slider => {
    const wrapper = slider.closest(".slider-wrapper");
    if (!wrapper) return;
    
    const prevBtn = wrapper.querySelector(".slider-arrow.prev");
    const nextBtn = wrapper.querySelector(".slider-arrow.next");
    
    // Set baseline opacities so they are always visible and hoverable
    if (prevBtn) {
      prevBtn.style.opacity = "0.8";
      prevBtn.style.pointerEvents = "auto";
    }
    if (nextBtn) {
      nextBtn.style.opacity = "0.8";
      nextBtn.style.pointerEvents = "auto";
    }
  });
});
