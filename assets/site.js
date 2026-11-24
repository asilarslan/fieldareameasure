// Sticky mobile CTA, Android store links and language switcher.
(function () {
  // Single-button CTAs point to the App Store; send Android visitors to Google Play instead.
  if (/android/i.test(navigator.userAgent)) {
    document.querySelectorAll('a[data-play]').forEach(function (a) { a.href = a.getAttribute('data-play'); });
  }

  // Mobile sticky App Store button: only after the hero, and never on top of the tool.
  var sticky = document.querySelector('.sticky-cta');
  var hero = document.querySelector('[data-hero]');
  var tool = document.querySelector('[data-tool]');
  if (sticky && hero && 'IntersectionObserver' in window) {
    var heroVisible = true, toolVisible = false;
    var update = function () { sticky.classList.toggle('show', !heroVisible && !toolVisible); };
    new IntersectionObserver(function (e) { heroVisible = e[0].isIntersecting; update(); }).observe(hero);
    if (tool) new IntersectionObserver(function (e) { toolVisible = e[0].isIntersecting; update(); }).observe(tool);
  }

  var lang = document.querySelector('.lang');
  if (lang) lang.addEventListener('change', function () { location.href = lang.value; });
})();
