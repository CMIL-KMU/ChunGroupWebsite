/* 
  Scroll to top button functionality
  Shows/hides button based on scroll position and handles smooth scroll to top
*/

{
  const onLoad = () => {
    const button = document.getElementById('scroll-to-top');
    if (!button) return;

    // Show/hide button based on scroll position
    const toggleButton = () => {
      if (window.scrollY > 300) {
        button.classList.add('visible');
      } else {
        button.classList.remove('visible');
      }
    };

    // Smooth scroll to top
    const scrollToTop = (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    };

    // Event listeners
    window.addEventListener('scroll', toggleButton);
    button.addEventListener('click', scrollToTop);

    // Initial check
    toggleButton();
  };

  // After page loads
  window.addEventListener('load', onLoad);
}






