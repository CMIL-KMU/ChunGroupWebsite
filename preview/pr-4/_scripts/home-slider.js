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

    // Mobile touch swipe circular loop detection
    let touchStartX = 0;
    let touchEndX = 0;

    slider.addEventListener('touchstart', e => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    slider.addEventListener('touchend', e => {
      touchEndX = e.changedTouches[0].screenX;
      
      const swipeDistance = touchStartX - touchEndX;
      const threshold = 40; // Minimum swipe distance in pixels to trigger wrap
      const scrollLeft = slider.scrollLeft;
      const maxScroll = slider.scrollWidth - slider.clientWidth;
      
      // Swipe Left -> Scroll Right (Next)
      if (swipeDistance > threshold) {
        if (scrollLeft >= maxScroll - 15) {
          // At the end, wrap to beginning
          slider.scrollTo({ left: 0, behavior: 'smooth' });
        }
      }
      // Swipe Right -> Scroll Left (Prev)
      else if (swipeDistance < -threshold) {
        if (scrollLeft <= 15) {
          // At the beginning, wrap to end
          slider.scrollTo({ left: maxScroll, behavior: 'smooth' });
        }
      }
    }, { passive: true });
  });
});
