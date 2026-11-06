#!/usr/bin/env python3
# generate_blueprint_html.py — BLUEPRINT.md -> interactive single-file BLUEPRINT.html
# Zero external resources: system fonts, embedded CSS/JS, inline SVG diagram.
import re
import datetime
import markdown
from pathlib import Path

HERE = Path(__file__).resolve().parent          # pdf-sources/
ROOT = HERE.parent                              # the bundle root
SRC = ROOT / 'BLUEPRINT.md'
OUT = ROOT / 'BLUEPRINT.html'
CSS = (HERE / 'html_template.css').read_text()
JS = (HERE / 'html_template.js').read_text()

md_text = SRC.read_text()

# ---- split hero (before first hr) from body
head, _, body_md = md_text.partition('\n---\n')
title_m = re.search(r'^# (.+)$', head, re.M)
doc_title = title_m.group(1).strip() if title_m else 'Agent Dev Sandbox Blueprint'
lede = re.sub(r'^# .+?\n+', '', head).strip()
lede = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', lede)
lede = re.sub(r'`([^`]+)`', r'<code>\1</code>', lede)

words = len(re.findall(r"\b[\w.-]+\b", body_md))
read_min = max(1, round(words / 220))

mk = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc', 'sane_lists'],
                       extension_configs={'toc': {'permalink': False, 'toc_depth': '2-3'}})
body_html = mk.convert(body_md)
toc_tokens = mk.toc_tokens  # top-level = h2 sections

# ---- split into <section> chunks at each h2
parts = re.split(r'(<h2 id="[^"]+">.*?</h2>)', body_html)
sections = []
i = 1
while i < len(parts):
    h2 = parts[i]
    content = parts[i + 1] if i + 1 < len(parts) else ''
    sec_id = re.search(r'id="([^"]+)"', h2).group(1)
    raw_title = re.sub(r'<[^>]+>', '', h2)
    num_m = re.match(r'(\d+)\.\s+(.*)', raw_title)
    num, name = (num_m.group(1), num_m.group(2)) if num_m else ('', raw_title)
    # h3 subsections for TOC subs
    subs = [(m.group(1), re.sub(r'<[^>]+>', '', m.group(2)))
            for m in re.finditer(r'<h3 id="([^"]+)">(.*?)</h3>', content)]
    sections.append({'id': sec_id, 'num': num, 'name': name,
                     'h2': h2, 'content': content, 'subs': subs})
    i += 2

# ---- locate §5 and §11 for injections
SVG = '''
<figure class="arch" aria-label="System design diagram">
<svg viewBox="0 0 900 710" role="img" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,'Segoe UI',Roboto,'Noto Sans SC',sans-serif">
  <defs>
    <marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="3.5" orient="auto">
      <path d="M0,0 L7,3.5 L0,7" stroke="var(--icon)" stroke-width="1.4" fill="none"/>
    </marker>
  </defs>
  <style>
    .b-title{font-size:20px;font-weight:700;fill:var(--text)}
    .b-desc{font-size:16px;fill:var(--muted)}
    .chip{font-size:15px;fill:var(--accent)}
    .bus-t{font-size:15px;fill:#fff}
    .w-label{font-size:14px;fill:var(--muted)}
  </style>
  <!-- wires -->
  <path d="M 560 150 L 560 122 L 755 122 L 755 76" stroke="var(--icon)" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>
  <path d="M 450 254 L 450 306" stroke="var(--icon)" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>
  <path d="M 176 334 L 176 366" stroke="var(--icon)" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>
  <path d="M 420 334 L 420 366" stroke="var(--icon)" stroke-width="1.5" fill="none" marker-end="url(#ah)"/>
  <text x="575" y="112" class="w-label">NAT egress</text>
  <text x="465" y="286" class="w-label">only NIC: agent-internal</text>
  <!-- internet -->
  <rect x="640" y="18" width="230" height="54" rx="6" fill="var(--panel)" stroke="var(--border)" stroke-width="1.5"/>
  <text x="755" y="50" text-anchor="middle" font-size="17" font-weight="600" fill="var(--muted)">Internet</text>
  <!-- host frame -->
  <rect x="16" y="100" width="868" height="590" rx="8" fill="var(--section-bg)" stroke="var(--header-fill)" stroke-width="1.5"/>
  <text x="36" y="128" font-size="16" font-weight="700" fill="var(--header-fill)" letter-spacing="1">DEBIAN 13 HOST &#183; 16-32 GB &#183; KVM</text>
  <text x="864" y="128" text-anchor="end" font-size="14" fill="var(--muted)">systemd --user (linger) &#183; Quadlet agent-gateway.service</text>
  <!-- gateway -->
  <rect x="250" y="150" width="400" height="104" rx="6" fill="var(--card)" stroke="var(--header-fill)"/>
  <text x="266" y="176" class="b-title">agent-gateway &#8212; rootless Squid</text>
  <text x="266" y="197" class="b-desc">single-file domain allowlist &#183; denied: HTTP 403 + log</text>
  <rect x="266" y="208" width="158" height="26" rx="13" fill="var(--panel)" stroke="var(--accent)" stroke-width="1.2"/>
  <text x="345" y="226" text-anchor="middle" class="chip">nic1 agent-egress</text>
  <rect x="436" y="208" width="172" height="26" rx="13" fill="var(--panel)" stroke="var(--accent)" stroke-width="1.2"/>
  <text x="522" y="226" text-anchor="middle" class="chip">nic2 agent-internal</text>
  <!-- bus -->
  <rect x="70" y="308" width="760" height="26" rx="4" fill="var(--header-fill)"/>
  <text x="450" y="326" text-anchor="middle" class="bus-t">agent-internal &#8212; internal network: no default route &#183; external DNS &#8594; NXDOMAIN</text>
  <!-- workspaces -->
  <rect x="70" y="368" width="212" height="132" rx="6" fill="var(--section-bg)" stroke="var(--border)" stroke-left="3"/>
  <rect x="70" y="368" width="3.5" height="132" fill="var(--accent)"/>
  <text x="86" y="392" font-size="18" font-weight="700" fill="var(--text)">agent-&lt;workspace&gt;</text>
  <text x="86" y="413" class="b-desc" font-size="14.5">keep-id:uid=1000 &#183; cap-drop=ALL</text>
  <text x="86" y="434" class="b-desc" font-size="14.5">no-new-privileges &#183; pids/mem/cpu caps</text>
  <text x="86" y="455" class="b-desc" font-size="14.5">env-file secrets &#183; seeded browsers</text>
  <rect x="314" y="368" width="212" height="132" rx="6" fill="var(--section-bg)" stroke="var(--border)"/>
  <rect x="314" y="368" width="3.5" height="132" fill="var(--accent)"/>
  <text x="330" y="392" font-size="18" font-weight="700" fill="var(--text)">agent-__ci-&lt;run&gt;</text>
  <text x="330" y="413" class="b-desc" font-size="14.5">single-shot CI run (&#167;12)</text>
  <text x="330" y="434" class="b-desc" font-size="14.5">per-run isolation self-audit</text>
  <text x="330" y="455" class="b-desc" font-size="14.5">artifacts &#8594; __ci/artifacts/</text>
  <text x="560" y="440" font-size="20" font-weight="600" fill="var(--muted)">&#215; N workspaces</text>
  <!-- VM -->
  <rect x="70" y="540" width="760" height="132" rx="6" fill="var(--section-bg)" stroke="var(--muted)"/>
  <text x="86" y="566" font-size="19" font-weight="700" fill="var(--text)">Tier 2 &#8212; KVM micro-VM per engagement (QEMU + official Debian 13 cloud image)</text>
  <rect x="86" y="580" width="180" height="28" rx="14" fill="var(--panel)" stroke="var(--border)"/>
  <text x="176" y="599" text-anchor="middle" font-size="14.5" fill="var(--muted)">cloud-init provisioning</text>
  <rect x="278" y="580" width="360" height="28" rx="14" fill="var(--panel)" stroke="var(--border)"/>
  <text x="458" y="599" text-anchor="middle" font-size="14.5" fill="var(--muted)">QEMU restrict=on &#183; nftables: proxy only, no DNS</text>
  <rect x="650" y="580" width="164" height="28" rx="14" fill="var(--panel)" stroke="var(--border)"/>
  <text x="732" y="599" text-anchor="middle" font-size="13" fill="var(--muted)">same image inside the VM</text>
</svg>
<figcaption>Figure 1 &#8212; System design: one host, two enforcement tiers, three consumption modes of one image.</figcaption>
</figure>
'''

CHECKLIST = '''
<div class="checklist" id="day0">
  <h4>Day-0 build checklist <span style="color:var(--accent)">&#183; progress saved locally</span></h4>
  <div class="cl-sub">Phase 0&#8211;5 from the runbook above &#8212; tick each gate only when its expected outcome printed.</div>
  <div class="cl-bar"><div id="cl-bar-fill"></div></div>
  <label><input type="checkbox"><span><b>Phase 0</b> &#8212; <code>00-preflight.sh</code> &rarr; <code>0 blocker(s)</code></span></label>
  <label><input type="checkbox"><span><b>Phase 1</b> &#8212; <code>10-host-bootstrap.sh [--tier2]</code> &rarr; all checkmarks (re-login if kvm group added)</span></label>
  <label><input type="checkbox"><span><b>Phase 1b</b> &#8212; <code>00-preflight.sh --post</code> &rarr; <code>0 blocker(s)</code></span></label>
  <label><input type="checkbox"><span><b>Phase 2</b> &#8212; <code>20-build-image.sh</code> &rarr; image <code>agent-dev-sandbox:1</code> built</span></label>
  <label><input type="checkbox"><span><b>Phase 3</b> &#8212; <code>30-gateway.sh up</code> &rarr; gateway running, probe <code>status=200</code></span></label>
  <label><input type="checkbox"><span><b>Phase 4 (GATE)</b> &#8212; <code>50-verify.sh</code> &rarr; <b>0 failed</b> (warnings allowed, each explained)</span></label>
  <label><input type="checkbox"><span><b>Phase 5 (optional)</b> &#8212; <code>60-tier2-microvm.sh base</code> &rarr; golden VM frozen</span></label>
  <label><input type="checkbox"><span><b>CI smoke</b> &#8212; <code>45-ci-run.sh run --repo .../budget-wiser.git -- bash -lc 'bun install &amp;&amp; bun run gate'</code> &rarr; exit 0</span></label>
  <div class="cl-actions">
    <button class="icon-btn" type="button" id="cl-reset">Reset</button>
    <span id="cl-status"></span>
  </div>
</div>
'''

for sec in sections:
    if sec['num'] == '5':
        # SVG after the h2; ASCII art (the big code block) becomes collapsible
        m = re.search(r'<pre>.*?</pre>', sec['content'], re.S)
        if m and 'systemd --user' in m.group(0):
            ascii_block = m.group(0)
            wrapped = ('<details class="ascii"><summary>ASCII version of this diagram '
                       '(as in BLUEPRINT.md)</summary>' + ascii_block + '</details>')
            sec['content'] = sec['content'].replace(ascii_block, wrapped)
        sec['content'] = SVG + sec['content']
    if sec['num'] == '11':
        sec['content'] = CHECKLIST + sec['content']

# ---- build TOC nav
toc_items = []
for sec in sections:
    label = (('<span class="secnum">%s.</span> ' % sec['num']) if sec['num'] else '') + sec['name']
    toc_items.append('<a href="#%s" data-target="%s">%s</a>' % (sec['id'], sec['id'], label))
    for sid, sname in sec['subs']:
        sname_clean = re.sub(r'<[^>]+>', '', sname)
        toc_items.append('<a class="sub" href="#%s" data-target="%s">%s</a>' % (sid, sid, sname_clean))
toc_html = '\n'.join(toc_items)

sec_html = []
for sec in sections:
    sec_html.append('<section class="doc-sec" id="%s">\n%s\n%s\n</section>'
                    % (sec['id'], sec['h2'], sec['content'].strip()))

today = datetime.date.today().strftime('%Y-%m-%d')

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} \u2014 interactive</title>
<meta name="description" content="Secure, egress-restricted development environment blueprint for AI coding agents on Debian 13 \u2014 interactive single-file edition.">
<style>
{css}
</style>
</head>
<body>
<div id="progress"></div>
<header class="topbar">
  <button class="icon-btn" id="nav-btn" aria-label="Toggle navigation">&#9776;</button>
  <div class="brand">Agent Dev <small>&middot; Sandbox Blueprint</small></div>
  <div class="searchwrap">
    <span class="kbd-hint">/</span>
    <input id="search" type="text" placeholder="Search the blueprint\u2026 (min 2 chars)" autocomplete="off" spellcheck="false">
    <button class="clear-btn" id="clear-btn" type="button" aria-label="Clear search">&times;</button>
  </div>
  <span id="search-meta"></span>
  <button class="icon-btn" id="theme-btn" type="button">\u263D Dark</button>
</header>
<div class="layout">
  <nav class="sidebar" aria-label="Table of contents">
    <h3>Contents</h3>
    <div class="toc">
{toc}
    </div>
    <h3>Shortcuts</h3>
    <div class="toc">
      <a href="#" onclick="return false" style="cursor:default">/ &nbsp;focus search</a>
      <a href="#" onclick="return false" style="cursor:default">Esc &nbsp;clear search</a>
      <a href="#" onclick="return false" style="cursor:default">Ctrl/Cmd+P &nbsp;print (light theme)</a>
    </div>
  </nav>
  <main>
    <div class="doc-hero">
      <h1>Agent Dev <span class="tint">Sandbox</span></h1>
      <p class="lede">{lede}</p>
      <div class="chips">
        <span class="chip"><b>14</b> sections</span>
        <span class="chip"><b>{words:,}</b> words</span>
        <span class="chip"><b>{read}</b> min read</span>
        <span class="chip">facts verified <b>2026-11-05</b></span>
        <span class="chip">rendered <b>{today}</b></span>
      </div>
    </div>
    <div id="no-results"><b>No matches.</b><br>Try a shorter query \u2014 search covers section titles and body text.</div>
{sections}
    <footer class="doc-foot">
      <span>Agent Dev Sandbox \u2014 Comprehensive Blueprint \u00b7 interactive single-file edition</span>
      <span>Mirrors <code>BLUEPRINT.md</code> \u00b7 works fully offline</span>
    </footer>
  </main>
</div>
<script>
{js}
</script>
</body>
</html>
'''.format(title=doc_title, css=CSS, toc=toc_html, lede=lede,
           words=words, read=read_min, today=today,
           sections='\n'.join(sec_html), js=JS)

OUT.write_text(html)
print('written:', OUT, '|', len(html), 'bytes |', len(sections), 'sections |', words, 'words')
