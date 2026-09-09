/*
  reveals the compact nav bar once the big home banner has scrolled away.
*/

{
  const onLoad = () => {
    const bar = document.querySelector(".mini-nav");
    const header = document.querySelector("header");
    if (!bar || !header) return;

    const update = () => {
      const past = window.scrollY > header.offsetHeight - 40;
      bar.dataset.shown = String(past);
      bar.setAttribute("aria-hidden", String(!past));
    };

    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
  };

  window.addEventListener("load", onLoad);
}
