// Rewrites the language-switcher click to land on the equivalent page in the
// other locale instead of that locale's homepage. Zensical's alternate/hreflang
// config only supports a single static link per locale (see CLAUDE.md), so this
// patches it client-side by swapping the /it/<->/en/ prefix on the current path.
// Assumes docs/it/ and docs/en/ mirror each other 1:1 (true today) — no
// existence check is done before redirecting.
//
// Intercepts the click itself (capture phase) rather than rewriting the href
// ahead of time — the theme's own bundled JS may re-render or otherwise touch
// this menu, so acting at click time on a live DOM query is more robust than
// a one-shot href mutation at load time.
document.addEventListener("click", function (event) {
  var link = event.target.closest(".md-select__link[hreflang]");
  if (!link) {
    return;
  }
  var targetLocale = link.getAttribute("hreflang");
  if (targetLocale !== "it" && targetLocale !== "en") {
    return;
  }
  var path = window.location.pathname;
  var match = path.match(/^\/(it|en)\//);
  if (!match) {
    return;
  }
  event.preventDefault();
  // Also stop propagation: the theme's own bundled JS attaches its own click
  // handler to this same link and, in this build, re-navigates using
  // location.hostname (which drops a non-default port) after this listener
  // runs — preventDefault() alone doesn't stop that second handler from
  // firing and overriding the navigation below. Since this listener runs in
  // the capture phase at the document level, stopping propagation here keeps
  // the event from ever reaching that handler.
  event.stopPropagation();
  window.location.href = path.replace(/^\/(it|en)\//, "/" + targetLocale + "/");
}, true);
