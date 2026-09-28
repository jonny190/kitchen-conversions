/* Kitchen Conversions — converters. No dependencies, no tracking. */
(function () {
  "use strict";

  var US_CUP_ML = 236.5882365;

  function num(el) {
    var v = parseFloat(String(el.value).replace(",", "."));
    return isFinite(v) ? v : null;
  }

  function fmt(v, decimals) {
    if (v === null) return "";
    if (Math.abs(v) >= 1000) decimals = Math.min(decimals, 1);
    return Number(v.toFixed(decimals)).toString();
  }

  /* Nearest common kitchen fraction, for amounts under 8 (cups/spoons). */
  function toFraction(v) {
    if (v === null || v <= 0 || v >= 8) return "";
    var whole = Math.floor(v), rest = v - whole;
    var table = [[0, ""], [0.125, "1/8"], [0.25, "1/4"], [0.3333, "1/3"], [0.375, "3/8"],
                 [0.5, "1/2"], [0.625, "5/8"], [0.6667, "2/3"], [0.75, "3/4"], [0.875, "7/8"], [1, ""]];
    var best = table[0][1], bestd = 1;
    for (var i = 0; i < table.length; i++) {
      var d = Math.abs(table[i][0] - rest);
      if (d < bestd) { bestd = d; best = table[i][1]; }
    }
    if (best === "" && rest > 0.0625 && rest < 0.1875) best = "1/8";
    var out = whole > 0 ? String(whole) : "";
    if (best) out += (out ? " " : "") + best;
    if (bestd > 0.04) out = "≈ " + out;
    return out;
  }

  function wireRatio(box) {
    var a = box.querySelector('[data-role="from"]'),
        b = box.querySelector('[data-role="to"]'),
        factor = parseFloat(box.getAttribute("data-factor")),
        da = parseInt(box.getAttribute("data-from-decimals") || "4", 10),
        db = parseInt(box.getAttribute("data-to-decimals") || "0", 10),
        frac = box.getAttribute("data-fraction") === "to",
        fracEl = (box.parentElement || box).querySelector(".frac-out");

    function sync(src, dst, mult, dec, other) {
      var v = num(src);
      if (v === null) { dst.value = ""; if (other) other.textContent = ""; return; }
      var r = v * mult;
      dst.value = fmt(r, dec);
      if (other) other.textContent = frac ? toFraction(r) : fmt(r, dec);
    }
    a.addEventListener("input", function () { sync(a, b, factor, db, fracEl); });
    b.addEventListener("input", function () { sync(b, a, 1 / factor, da, null); });
    if (a.value !== "") sync(a, b, factor, db, fracEl);
  }

  function cToF(c) { return c * 9 / 5 + 32; }
  function fToC(f) { return (f - 32) * 5 / 9; }

  function wireTemp(box) {
    var a = box.querySelector('[data-role="from"]'),
        b = box.querySelector('[data-role="to"]'),
        mode = box.getAttribute("data-mode") || "c2f";
    function conv(v) { return mode === "c2f" ? cToF(v) : fToC(v); }
    function sync(src, dst) {
      var v = num(src);
      dst.value = v === null ? "" : fmt(conv(v), 0);
    }
    a.addEventListener("input", function () { sync(a, b); });
    b.addEventListener("input", function () { sync(b, a); });
  }

  function wireUnits(box) {
    var data;
    try { data = JSON.parse(box.getAttribute("data-units")); } catch (e) { return; }
    var from = box.querySelector('[data-role="unit-from"]'),
        to = box.querySelector('[data-role="unit-to"]'),
        input = box.querySelector('[data-role="unit-value"]'),
        out = (box.parentElement || box).querySelector('[data-role="unit-out"]');
    if (!from || !to || !input || !out) return;
    Object.keys(data).forEach(function (k) {
      from.add(new Option(k, k));
      to.add(new Option(k, k));
    });
    var keys = Object.keys(data);
    to.value = keys[1] || keys[0];
    function calc() {
      var v = num(input);
      if (v === null) { out.textContent = ""; return; }
      var base = v * data[from.value];
      out.textContent = fmt(base / data[to.value], 6) + " " + to.value;
    }
    from.addEventListener("change", calc);
    to.addEventListener("change", calc);
    input.addEventListener("input", calc);
    calc();
  }

  function wireScaler(form) {
    var factor = form.querySelector('[name="factor"]');
    function run() {
      var f = parseFloat(factor.value);
      if (!isFinite(f) || f <= 0) return;
      Array.prototype.forEach.call(form.querySelectorAll("input[data-base]"), function (inp) {
        var base = parseFloat(inp.getAttribute("data-base"));
        inp.value = fmt(base * f, base % 1 === 0 ? 0 : 2);
      });
    }
    if (factor) factor.addEventListener("input", run);
  }

  document.addEventListener("DOMContentLoaded", function () {
    Array.prototype.forEach.call(document.querySelectorAll(".converter[data-factor]"), wireRatio);
    Array.prototype.forEach.call(document.querySelectorAll(".converter[data-mode]"), wireTemp);
    Array.prototype.forEach.call(document.querySelectorAll(".converter[data-units]"), wireUnits);
    Array.prototype.forEach.call(document.querySelectorAll("form.scale"), wireScaler);
  });
})();
