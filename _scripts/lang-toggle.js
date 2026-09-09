/*
  manages the KOR / ENG content toggle.
  paragraphs are marked up as <div class="lang" data-lang="ko|en">.
*/

{
  // load saved (or browser-derived) language before the page renders
  const saved = window.localStorage.getItem("site-lang");
  const fromBrowser = (navigator.language || "en").toLowerCase().startsWith("ko")
    ? "ko"
    : "en";
  document.documentElement.dataset.lang = saved ?? fromBrowser;

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
