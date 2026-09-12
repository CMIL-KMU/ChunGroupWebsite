/*
  manages the KOR / ENG content toggle.

  three mechanisms, because not every string can be a pair of elements:

  1. paired elements - <span|div class="lang" data-lang="ko|en"> ... </span>
     The stylesheet hides whichever one does not match html[data-lang], so
     these cost nothing at runtime. Most of the site uses this, emitted by
     _includes/t.html.

  2. attributes - an element carrying data-t-en / data-t-ko has the attribute
     named in data-t-attr rewritten on every switch. Needed for placeholders
     and aria-labels, which cannot hold markup.

  3. script-rendered text - anything drawn by JS (the search results line)
     reads window.siteLang() and re-renders on the "langchange" event.

  Publication entries are deliberately left alone: a citation is a quoted
  bibliographic record and stays in the language it was published in.
*/

{
  const KEY = "site-lang";
  const DEFAULT = "en";

  // apply the saved language before the page renders, so there is no flash of
  // the wrong language (this file is loaded in <head>, before <body> exists)
  const initial = window.localStorage.getItem(KEY) ?? DEFAULT;
  document.documentElement.dataset.lang = initial;
  document.documentElement.lang = initial === "ko" ? "ko" : "en";

  window.siteLang = () => document.documentElement.dataset.lang || DEFAULT;

  // mechanism 2: swap localized attributes
  const applyAttributes = (lang) => {
    document.querySelectorAll("[data-t-en]").forEach((element) => {
      const value = lang === "ko" ? element.dataset.tKo : element.dataset.tEn;
      if (value === undefined) return;
      const attribute = element.dataset.tAttr;
      if (attribute) element.setAttribute(attribute, value);
      else element.textContent = value;
    });
  };

  // reflect the current language on the toggle buttons
  const syncButtons = (lang) => {
    document.querySelectorAll(".lang-toggle button").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.setLang === lang));
    });
  };

  const apply = (lang) => {
    document.documentElement.dataset.lang = lang;
    document.documentElement.lang = lang === "ko" ? "ko" : "en";
    syncButtons(lang);
    applyAttributes(lang);
    // mechanism 3: let script-rendered text redraw itself
    window.dispatchEvent(new CustomEvent("langchange", { detail: { lang } }));
  };

  const onReady = () => apply(window.siteLang());
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", onReady);
  else onReady();

  // when the user picks a language
  window.onLangToggle = (lang) => {
    window.localStorage.setItem(KEY, lang);
    apply(lang);
  };
}
