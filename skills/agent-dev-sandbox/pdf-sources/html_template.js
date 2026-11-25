/* BLUEPRINT.html — interactions: theme, scroll-spy, search, copy, checklist */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------------- pristine section snapshots ---------------- */
  // Taken BEFORE any binding injects interactive elements (copy buttons),
  // so a search-restore cycle replays authored content only — never
  // serialized, listener-less copies of attached widgets.
  var secEls = $$('section.doc-sec');
  var originals = new Map();
  secEls.forEach(function (s) { originals.set(s, s.innerHTML); });

  /* ---------------- theme ---------------- */
  var THEME_KEY = 'ads-blueprint-theme';
  var saved = null;
  try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
  var preferDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    $('#theme-btn').textContent = t === 'dark' ? '\u2600\ufe0f Light' : '\u263D Dark';
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
  }
  applyTheme(saved || (preferDark ? 'dark' : 'light'));
  $('#theme-btn').addEventListener('click', function () {
    applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  /* ---------------- mobile nav ---------------- */
  $('#nav-btn').addEventListener('click', function () {
    document.body.classList.toggle('nav-open');
  });
  $$('.toc a').forEach(function (a) {
    a.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
  });

  /* ---------------- progress bar ---------------- */
  var bar = $('#progress');
  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = max > 0 ? (100 * h.scrollTop / max) + '%' : '0%';
  }
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- scroll-spy ---------------- */
  var links = $$('.toc a[data-target]');
  var sections = links.map(function (a) { return document.getElementById(a.getAttribute('data-target')); });
  function spy() {
    var pos = window.scrollY + 90, idx = 0;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i] && sections[i].offsetTop <= pos) idx = i;
    }
    links.forEach(function (a, i) { a.classList.toggle('active', i === idx); });
  }
  document.addEventListener('scroll', spy, { passive: true });
  spy();

  /* ---------------- copy buttons ---------------- */
  // codeText: the payload of a <pre> WITHOUT the copy button's own label
  // (the button lives inside the <pre>, so pre.innerText would append "Copy").
  function codeText(pre) {
    var code = pre.querySelector('code');
    if (code) return code.textContent;
    var clone = pre.cloneNode(true);
    $$('.copy-btn', clone).forEach(function (b) { b.parentNode.removeChild(b); });
    return clone.textContent;
  }
  // copyText: async Clipboard API first; hidden-textarea + execCommand
  // fallback for engines or locked-down contexts where the API is missing
  // or rejects (e.g. file:// in hardened browsers). onOk fires only on
  // confirmed success.
  function copyText(text, onOk) {
    var fallback = function () {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:0;left:-9999px;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      if (ok) onOk();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(onOk, fallback);
    } else {
      fallback();
    }
  }
  // bindCopy: single, idempotent binder for the initial attach AND the
  // re-attach after search restore (clearMarks replaces section innerHTML
  // from the pristine snapshot). Strips any existing buttons first so a
  // double call can never leave inert duplicates behind.
  function bindCopy() {
    $$('.copy-btn').forEach(function (b) { b.parentNode.removeChild(b); });
    $$('pre').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.type = 'button';
      btn.textContent = 'Copy';
      btn.setAttribute('aria-label', 'Copy code to clipboard');
      btn.addEventListener('click', function () {
        copyText(codeText(pre), function () {
          btn.textContent = 'Copied \u2713';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 1600);
        });
      });
      pre.appendChild(btn);
    });
  }
  bindCopy();

  /* ---------------- day-0 checklist ---------------- */
  var CL_KEY = 'ads-blueprint-checklist';
  var boxes = $$('.checklist input[type="checkbox"]');
  function loadCl() {
    var state = [];
    try { state = JSON.parse(localStorage.getItem(CL_KEY) || '[]'); } catch (e) {}
    boxes.forEach(function (b, i) { b.checked = !!state[i]; });
    renderCl();
  }
  function saveCl() {
    var state = boxes.map(function (b) { return b.checked; });
    try { localStorage.setItem(CL_KEY, JSON.stringify(state)); } catch (e) {}
    renderCl();
  }
  function renderCl() {
    var bar = $('#cl-bar-fill'), status = $('#cl-status');
    if (!bar || !status) return;
    var done = boxes.filter(function (b) { return b.checked; }).length;
    bar.style.width = (boxes.length ? 100 * done / boxes.length : 0) + '%';
    status.textContent = done + ' / ' + boxes.length + ' steps done' +
      (done === boxes.length && boxes.length ? ' \u2014 environment verified \u2713' : '');
  }
  function bindChecklist() {
    // (Re)attach listeners: search restore replaces the section DOM, which
    // clones the checklist elements and orphans any previous listeners.
    boxes = $$('.checklist input[type="checkbox"]');
    boxes.forEach(function (b) { b.addEventListener('change', saveCl); });
    var rst = $('#cl-reset');
    if (rst) {
      rst.onclick = function () {
        boxes.forEach(function (b) { b.checked = false; });
        saveCl();
      };
    }
  }
  bindChecklist();
  loadCl();

  /* ---------------- search ---------------- */
  var input = $('#search'), meta = $('#search-meta'), clearBtn = $('#clear-btn');

  // Responsive placeholder: the full hint does not fit below ~480 px and the
  // browser would truncate it mid-word; show a short one on narrow viewports.
  function setPlaceholder() {
    input.placeholder = window.innerWidth < 480
      ? 'Search\u2026'
      : 'Search the blueprint\u2026 (min 2 chars)';
  }
  setPlaceholder();
  window.addEventListener('resize', setPlaceholder);

  function clearMarks() {
    secEls.forEach(function (s) {
      s.classList.remove('hidden-sec');
      if (originals.has(s)) s.innerHTML = originals.get(s);
    });
    $('#no-results').style.display = 'none';
    // section innerHTML was just restored from the originals snapshot: re-bind
    // everything that lives INSIDE sections (copy buttons, checklist) and
    // replay persisted checklist state onto the fresh DOM.
    bindCopy();
    bindChecklist();
    loadCl();
  }

  function highlightIn(el, needle) {
    var count = 0;
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = n.parentNode;
        if (p.nodeName === 'SCRIPT' || p.nodeName === 'STYLE' || p.nodeName === 'MARK') return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) {
      var text = node.nodeValue, lower = text.toLowerCase(), idx = lower.indexOf(needle);
      if (idx === -1) return;
      var frag = document.createDocumentFragment(), pos = 0;
      while (idx !== -1) {
        if (idx > pos) frag.appendChild(document.createTextNode(text.slice(pos, idx)));
        var m = document.createElement('mark');
        m.className = 'hl';
        m.textContent = text.slice(idx, idx + needle.length);
        frag.appendChild(m);
        count++;
        pos = idx + needle.length;
        idx = lower.indexOf(needle, pos);
      }
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      node.parentNode.replaceChild(frag, node);
    });
    return count;
  }

  var searchTimer = null;
  function runSearch() {
    var q = input.value.trim().toLowerCase();
    clearBtn.style.display = q ? 'block' : 'none';
    if (q.length < 2) {
      clearMarks();
      meta.textContent = '';
      return;
    }
    clearMarks();
    var total = 0, withHit = 0;
    secEls.forEach(function (s) {
      var hits = highlightIn(s, q);
      if (hits > 0) { withHit++; total += hits; }
      else s.classList.add('hidden-sec');
    });
    // keep hero visible only when everything matches
    var anyVisible = secEls.some(function (s) { return !s.classList.contains('hidden-sec'); });
    $('#no-results').style.display = anyVisible ? 'none' : 'block';
    meta.textContent = total ? total + ' match' + (total > 1 ? 'es' : '') + ' in ' + withHit + ' section' + (withHit > 1 ? 's' : '') : 'no matches';
    var first = secEls.find(function (s) { return !s.classList.contains('hidden-sec'); });
    if (first) first.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  input.addEventListener('input', function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(runSearch, 180);
  });
  clearBtn.addEventListener('click', function () {
    input.value = '';
    runSearch();
    input.focus();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input &&
        document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      input.focus();
      input.select();
    } else if (e.key === 'Escape') {
      if (input.value) { input.value = ''; runSearch(); }
      input.blur();
    }
  });
})();
