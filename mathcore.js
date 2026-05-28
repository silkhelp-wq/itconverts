/* itconverts — mathcore.js
 * A small, safe recursive-descent expression evaluator (no eval()).
 * window.MATH.evaluate(expr, {deg:Boolean, vars:{x:..}, ans:..}) -> Number (throws on error)
 * Supports: + - * / ^, unary +/-, parentheses, implicit multiply (2pi, 3(4)),
 * postfix factorial !, functions, constants (pi, e), variable x, ans.
 */
(function (global) {
  'use strict';

  var FUNCS = {
    sin: function (x, deg) { return Math.sin(deg ? x * Math.PI / 180 : x); },
    cos: function (x, deg) { return Math.cos(deg ? x * Math.PI / 180 : x); },
    tan: function (x, deg) { return Math.tan(deg ? x * Math.PI / 180 : x); },
    asin: function (x, deg) { var r = Math.asin(x); return deg ? r * 180 / Math.PI : r; },
    acos: function (x, deg) { var r = Math.acos(x); return deg ? r * 180 / Math.PI : r; },
    atan: function (x, deg) { var r = Math.atan(x); return deg ? r * 180 / Math.PI : r; },
    sinh: function (x) { return Math.sinh(x); },
    cosh: function (x) { return Math.cosh(x); },
    tanh: function (x) { return Math.tanh(x); },
    ln: function (x) { return Math.log(x); },
    log: function (x) { return Math.log(x) / Math.LN10; },
    log2: function (x) { return Math.log(x) / Math.LN2; },
    sqrt: function (x) { return Math.sqrt(x); },
    cbrt: function (x) { return Math.cbrt(x); },
    abs: function (x) { return Math.abs(x); },
    exp: function (x) { return Math.exp(x); },
    floor: function (x) { return Math.floor(x); },
    ceil: function (x) { return Math.ceil(x); },
    round: function (x) { return Math.round(x); },
    sign: function (x) { return Math.sign(x); }
  };
  var CONSTS = { pi: Math.PI, e: Math.E, tau: Math.PI * 2 };

  function tokenize(src) {
    var tokens = [], i = 0, n = src.length;
    var isDigit = function (c) { return c >= '0' && c <= '9'; };
    var isAlpha = function (c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); };
    while (i < n) {
      var c = src[i];
      if (c === ' ' || c === '\t') { i++; continue; }
      if (isDigit(c) || (c === '.' && isDigit(src[i + 1]))) {
        var num = '';
        while (i < n && (isDigit(src[i]) || src[i] === '.')) { num += src[i++]; }
        // scientific notation: 1e3, 2.5E-4
        if (i < n && (src[i] === 'e' || src[i] === 'E') &&
            (isDigit(src[i + 1]) || ((src[i + 1] === '+' || src[i + 1] === '-') && isDigit(src[i + 2])))) {
          num += src[i++]; if (src[i] === '+' || src[i] === '-') { num += src[i++]; }
          while (i < n && isDigit(src[i])) { num += src[i++]; }
        }
        tokens.push({ t: 'num', v: parseFloat(num) });
        continue;
      }
      if (isAlpha(c)) {
        var id = '';
        while (i < n && (isAlpha(src[i]) || isDigit(src[i]))) { id += src[i++]; }
        tokens.push({ t: 'id', v: id.toLowerCase() });
        continue;
      }
      if ('+-*/^(),!%'.indexOf(c) !== -1) {
        // unicode operator aliases handled before calling tokenize
        tokens.push({ t: 'op', v: c }); i++; continue;
      }
      throw new Error('Unexpected “' + c + '”');
    }
    return tokens;
  }

  function factorial(n) {
    if (n < 0 || Math.floor(n) !== n) { return gamma(n + 1); }
    var r = 1; for (var k = 2; k <= n; k++) { r *= k; } return r;
  }
  // Lanczos gamma for non-integer factorials
  function gamma(z) {
    var g = 7, c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
      771.32342877765313, -176.61502916214059, 12.507343278686905,
      -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    if (z < 0.5) { return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z)); }
    z -= 1; var x = c[0];
    for (var i = 1; i < g + 2; i++) { x += c[i] / (z + i); }
    var t = z + g + 0.5;
    return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
  }

  function parse(tokens, opts) {
    var pos = 0;
    var deg = !!opts.deg;
    var vars = opts.vars || {};
    var peek = function () { return tokens[pos]; };
    var next = function () { return tokens[pos++]; };
    function expect(v) { var t = next(); if (!t || t.v !== v) { throw new Error('Expected “' + v + '”'); } }

    // expr := term (('+'|'-') term)*
    function parseExpr() {
      var v = parseTerm();
      var t;
      while ((t = peek()) && t.t === 'op' && (t.v === '+' || t.v === '-')) {
        next(); var r = parseTerm(); v = t.v === '+' ? v + r : v - r;
      }
      return v;
    }
    // term := factor (('*'|'/'|'%'| implicit) factor)*
    function parseTerm() {
      var v = parseFactor();
      var t;
      while ((t = peek())) {
        if (t.t === 'op' && (t.v === '*' || t.v === '/' || t.v === '%')) {
          next(); var r = parseFactor();
          v = t.v === '*' ? v * r : (t.v === '/' ? v / r : v % r);
        } else if ((t.t === 'num') || (t.t === 'id') || (t.t === 'op' && t.v === '(')) {
          // implicit multiplication: 2pi, 3(4), (1)(2)
          var r2 = parseFactor(); v = v * r2;
        } else { break; }
      }
      return v;
    }
    // factor := power with unary
    function parseFactor() {
      var t = peek();
      if (t && t.t === 'op' && (t.v === '+' || t.v === '-')) {
        next(); var val = parseFactor(); return t.v === '-' ? -val : val;
      }
      return parsePower();
    }
    // power := postfix ('^' factor)?  (right-assoc)
    function parsePower() {
      var base = parsePostfix();
      var t = peek();
      if (t && t.t === 'op' && t.v === '^') { next(); var exp = parseFactor(); return Math.pow(base, exp); }
      return base;
    }
    // postfix := primary '!'? '%'?
    function parsePostfix() {
      var v = parsePrimary();
      var t;
      while ((t = peek()) && t.t === 'op' && (t.v === '!')) { next(); v = factorial(v); }
      return v;
    }
    function parsePrimary() {
      var t = next();
      if (!t) { throw new Error('Unexpected end'); }
      if (t.t === 'num') { return t.v; }
      if (t.t === 'op' && t.v === '(') { var v = parseExpr(); expect(')'); return v; }
      if (t.t === 'id') {
        var name = t.v;
        if (FUNCS[name]) {
          expect('('); var arg = parseExpr(); expect(')');
          return FUNCS[name](arg, deg);
        }
        if (CONSTS.hasOwnProperty(name)) { return CONSTS[name]; }
        if (name === 'ans') { return opts.ans || 0; }
        if (vars.hasOwnProperty(name)) { return vars[name]; }
        throw new Error('Unknown “' + name + '”');
      }
      throw new Error('Unexpected “' + (t.v) + '”');
    }

    var result = parseExpr();
    if (pos < tokens.length) { throw new Error('Unexpected “' + tokens[pos].v + '”'); }
    return result;
  }

  function normalize(src) {
    return String(src)
      .replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-')
      .replace(/π/g, 'pi').replace(/√/g, 'sqrt').replace(/∙|·/g, '*')
      .replace(/\^\s*/g, '^');
  }

  function evaluate(src, opts) {
    opts = opts || {};
    var clean = normalize(src);
    if (!clean.trim()) { throw new Error('Empty'); }
    var tokens = tokenize(clean);
    var v = parse(tokens, opts);
    if (typeof v !== 'number' || !isFinite(v)) {
      if (isNaN(v)) { throw new Error('Not a number'); }
      // allow Infinity to surface as a result rather than crash
    }
    return v;
  }

  global.MATH = { evaluate: evaluate, FUNCS: FUNCS, CONSTS: CONSTS, normalize: normalize };
})(window);
