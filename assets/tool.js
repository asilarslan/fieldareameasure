// Area converter, rectangle calculator and (on arazi.app) TAKS/KAKS calculator. Runs only in the browser.
(function () {
  var lang = document.documentElement.lang;
  var dec = (lang === 'en') ? '.' : ',';
  var parse = function (s) {
    s = String(s).trim().replace(/\s/g, '');
    if (!s) return NaN;
    if (dec === ',') s = s.replace(/\./g, '').replace(',', '.'); else s = s.replace(/,/g, '');
    return parseFloat(s);
  };
  var fmt = function (x) {
    if (!isFinite(x)) return '';
    var d = Math.abs(x) >= 1000 ? 2 : Math.abs(x) >= 1 ? 4 : 6;
    var s = x.toLocaleString(lang === 'pt' ? 'pt-BR' : lang, { maximumFractionDigits: d });
    return s;
  };

  var conv = document.querySelector('[data-conv]');
  if (conv) {
    var inputs = conv.querySelectorAll('input[data-u]');
    inputs.forEach(function (inp) {
      inp.addEventListener('input', function () {
        var v = parse(inp.value);
        inputs.forEach(function (o) { o.parentNode.classList.toggle('src', o === inp); });
        var m2 = v * parseFloat(inp.dataset.f);
        inputs.forEach(function (o) { if (o !== inp) o.value = isFinite(m2) ? fmt(m2 / parseFloat(o.dataset.f)) : ''; });
      });
    });
    // Start with 1 hectare (or the first unit) so every field shows an example value.
    var start = conv.querySelector('[data-u="ha"]') || inputs[0];
    start.value = fmt(1); start.dispatchEvent(new Event('input'));
  }

  var rect = document.querySelector('[data-rect]');
  if (rect) {
    var out = rect.querySelector('[data-rout]');
    var calc = function () {
      var l = parse(rect.querySelector('[data-l]').value), w = parse(rect.querySelector('[data-w]').value);
      var f = parseFloat(rect.querySelector('[data-lu]').value);
      if (!(l > 0 && w > 0)) { out.textContent = ''; return; }
      var m2 = l * w * f * f;
      var units = Array.prototype.map.call(document.querySelectorAll('input[data-u]'), function (i) {
        return { k: i.dataset.u, f: parseFloat(i.dataset.f), n: i.parentNode.querySelector('span').textContent.replace(/ \(.*/, '') };
      }).filter(function (u) { return ['m2', 'ha', 'ac', 'ft2', 'donum'].indexOf(u.k) >= 0; });
      out.textContent = units.map(function (u) { return fmt(m2 / u.f) + ' ' + u.n.toLowerCase(); }).join(' · ');
    };
    rect.addEventListener('input', calc);
    rect.addEventListener('change', calc);
  }

  var taks = document.querySelector('[data-taks]');
  if (taks) {
    var o = taks.querySelector('[data-tout]');
    var run = function () {
      var a = parse(taks.querySelector('[data-area]').value), t = parse(taks.querySelector('[data-t]').value), k = parse(taks.querySelector('[data-k]').value);
      if (!(a > 0)) { o.hidden = true; return; }
      var base = t > 0 ? a * t : NaN, total = k > 0 ? a * k : NaN;
      o.hidden = false;
      o.querySelector('[data-base]').textContent = isFinite(base) ? fmt(base) + ' m²' : '—';
      o.querySelector('[data-total]').textContent = isFinite(total) ? fmt(total) + ' m²' : '—';
      o.querySelector('[data-floors]').textContent = (isFinite(base) && isFinite(total) && base > 0) ? fmt(Math.floor(total / base * 10) / 10) : '—';
    };
    taks.addEventListener('input', run);
  }
})();
