/* itconverts — study-search.js   (window.ITC_STUDY)
 * A refined, education-only search for students of all ages, anywhere.
 *
 * Design decision #1 (chosen): results come ONLY from a curated allowlist of
 * free, open, ad-free educational sources — so "educational, nothing else" is
 * enforced by WHERE we look, not by trying to judge every query. No AI, no paid
 * search API, no API key, no per-query cost. Runs straight from the browser.
 *
 * Sources (all free, CORS-enabled, multilingual via the {lang} subdomain):
 *   - Wikipedia    — encyclopedic "taught in school" core
 *   - Wikibooks    — open textbooks
 *   - Wiktionary   — definitions / language
 * Add more later by extending SOURCES (Wikiversity, Wikisource, etc.).
 */
(function (g) {
  'use strict';
  var CFG = g.ITC_CONFIG || {};
  var lang = (CFG.STUDY_LANG || 'en').toLowerCase();

  // Each source uses the same Wikimedia REST search endpoint on its own host.
  var SOURCES = [
    { id: 'wikipedia',  label: 'Wikipedia',  host: function (l) { return l + '.wikipedia.org'; },  badge: 'encyclopedia' },
    { id: 'wikibooks',  label: 'Wikibooks',  host: function (l) { return l + '.wikibooks.org'; },  badge: 'open textbook' },
    { id: 'wiktionary', label: 'Wiktionary', host: function (l) { return l + '.wiktionary.org'; }, badge: 'dictionary' }
  ];

  // Defense-in-depth: even if something odd comes back, only these hosts render.
  var ALLOW = ['wikipedia.org', 'wikibooks.org', 'wiktionary.org', 'wikiversity.org', 'wikisource.org'];

  function stripTags(html) { return String(html == null ? '' : html).replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim(); }

  function hostOf(u) { try { return new URL(u).hostname.toLowerCase().replace(/^www\./, ''); } catch (e) { return ''; } }
  function allowed(url) {
    var h = hostOf(url); if (!h) return false;
    for (var i = 0; i < ALLOW.length; i++) { var d = ALLOW[i]; if (h === d || h.slice(-(d.length + 1)) === '.' + d) return true; }
    return false;
  }

  function articleUrl(l, host, page) {
    var slug = (page.key || page.title || '').replace(/ /g, '_');
    return 'https://' + host + '/wiki/' + encodeURIComponent(slug).replace(/%2F/g, '/');
  }
  function thumbUrl(t) { if (!t || !t.url) return ''; return t.url.indexOf('//') === 0 ? 'https:' + t.url : t.url; }

  // Pure: turn one Wikimedia REST page into a normalized result card.
  function normalizePage(page, src, l) {
    if (!page || !page.title) return null;
    var host = src.host(l);
    var url = articleUrl(l, host, page);
    if (!allowed(url)) return null;
    return {
      title: page.title,
      snippet: stripTags(page.excerpt) || stripTags(page.description) || '',
      url: url,
      site: src.label,
      source: src.id,
      badge: src.badge,
      thumb: thumbUrl(page.thumbnail)
    };
  }

  function fetchSource(src, query, l, limit) {
    var ep = 'https://' + src.host(l) + '/w/rest.php/v1/search/page?q=' + encodeURIComponent(query) + '&limit=' + (limit || 5);
    return fetch(ep, { headers: { 'Accept': 'application/json', 'Api-User-Agent': 'itconverts/1.0 (educational search)' } })
      .then(function (r) { return r.ok ? r.json() : { pages: [] }; })
      .then(function (d) { return (d && d.pages ? d.pages : []).map(function (p) { return normalizePage(p, src, l); }).filter(Boolean); })
      .catch(function () { return []; });   // one source failing must not break the whole search
  }

  function search(query, opts) {
    opts = opts || {};
    query = String(query || '').trim();
    var l = (opts.lang || lang).toLowerCase();
    var limit = opts.limit || 4;
    if (!query) return Promise.resolve({ query: query, lang: l, results: [] });

    // Query each source in parallel, then interleave so the first result of
    // each source appears before the second of any (variety over depth).
    return Promise.all(SOURCES.map(function (s) { return fetchSource(s, query, l, limit); }))
      .then(function (lists) {
        var out = [], i = 0, more = true;
        while (more) {
          more = false;
          for (var s = 0; s < lists.length; s++) { if (lists[s][i]) { out.push(lists[s][i]); more = true; } }
          i++;
        }
        return { query: query, lang: l, results: out };
      });
  }

  g.ITC_STUDY = {
    search: search,
    setLang: function (l) { lang = String(l || 'en').toLowerCase(); },
    getLang: function () { return lang; },
    SOURCES: SOURCES, ALLOW: ALLOW,
    // exposed for unit tests:
    _normalizePage: normalizePage, _allowed: allowed, _stripTags: stripTags, _articleUrl: articleUrl, _thumbUrl: thumbUrl, _hostOf: hostOf
  };
})(window);
