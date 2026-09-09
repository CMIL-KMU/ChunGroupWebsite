/*
  manages the KOR / ENG content toggle.
  paragraphs are marked up as <div class="lang" data-lang="ko|en">.
*/

{
  // load saved language before the page renders; English is the default
  document.documentElement.dataset.lang =
    window.localStorage.getItem("site-lang") ?? "en";

  const sync = () => {
    const current = document.documentElement.dataset.lang;
    document.querySelectorAll(".lang-toggle button").forEach((button) => {
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.setLang === current)
      );
    });
  };

  window.addEventListener("load", sync);

  // when user picks a language
  window.onLangToggle = (lang) => {
    document.documentElement.dataset.lang = lang;
    window.localStorage.setItem("site-lang", lang);
    sync();
  };
}
