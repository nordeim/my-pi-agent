# Typography Pairings — 6 Curated Font Pairings

> Each pairing is a (heading + body + numeric) trio tuned for a specific deck voice. Pick one, or use as inspiration.

---

## 1. Inter + JetBrains Mono (default for dev-tool decks)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

--font-heading: 'Inter', system-ui, sans-serif;
--font-body: 'Inter', system-ui, sans-serif;
--font-num: 'JetBrains Mono', 'SF Mono', monospace;
```

**Use case:** Dev-tool repos, developer-facing marketing, modern SaaS.
**Voice:** Clean, modern, developer-native. Inter is the default for most dev tools.
**Pair with:** GitHub Dark, Indigo Premium, Vercel Monochrome palettes.
**Recommended default** for most dev-tool decks.

---

## 2. Space Grotesk + IBM Plex Mono

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

--font-heading: 'Space Grotesk', system-ui, sans-serif;
--font-body: 'Inter', system-ui, sans-serif;  /* keep Inter for body readability */
--font-num: 'IBM Plex Mono', 'SF Mono', monospace;
```

**Use case:** Distinctive-but-not-trendy decks, design studios, creative tools.
**Voice:** Geometric, slightly editorial. Space Grotesk has character without being fashionable.
**Pair with:** Editorial Cream, Brutalist Contrast, Indigo Premium palettes.

---

## 3. Geist + Geist Mono

```css
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap');

--font-heading: 'Geist', system-ui, sans-serif;
--font-body: 'Geist', system-ui, sans-serif;
--font-num: 'Geist Mono', 'SF Mono', monospace;
```

**Use case:** Vercel-native products, ultra-modern SaaS, AI tools.
**Voice:** Vercel's font. Ultra-modern, restrained, SaaS feel.
**Pair with:** Vercel Monochrome, Indigo Premium, GitHub Dark palettes.
**Note:** Geist is relatively new — may not be on all systems. Falls back to system-ui gracefully.

---

## 4. Playfair Display + Inter

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

--font-heading: 'Playfair Display', Georgia, serif;
--font-body: 'Inter', system-ui, sans-serif;
--font-num: 'JetBrains Mono', 'SF Mono', monospace;
```

**Use case:** Editorial magazines, long-form content, print-quality feel.
**Voice:** Magazine-style serif headlines, modern sans-serif body. Distinctive hierarchy.
**Pair with:** Editorial Cream palette.
**Note:** Use Playfair only for big headlines (display, h1). Body stays Inter for readability.

---

## 5. DM Sans + DM Mono

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

--font-heading: 'DM Sans', system-ui, sans-serif;
--font-body: 'DM Sans', system-ui, sans-serif;
--font-num: 'DM Mono', 'SF Mono', monospace;
```

**Use case:** Friendly SaaS, education tech, consumer-facing products.
**Voice:** Warm, approachable, geometric. Less corporate than Inter.
**Pair with:** Sunset Warm, Forest Canopy, Editorial Cream palettes.

---

## 6. Söhne / IBM Plex Sans + IBM Plex Mono (fallback)

```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

--font-heading: 'IBM Plex Sans', system-ui, sans-serif;
--font-body: 'IBM Plex Sans', system-ui, sans-serif;
--font-num: 'IBM Plex Mono', 'SF Mono', monospace;
```

**Use case:** Enterprise B2B, fintech, AI/ML platforms, IBM-adjacent brands.
**Voice:** Corporate but not stuffy. IBM Plex is engineered for technical readability.
**Pair with:** Indigo Premium, GitHub Dark, Vercel Monochrome palettes.
**Note:** Söhne is the original (used by OpenAI, Linear) but requires a paid license. IBM Plex Sans is the open-source fallback with a similar feel.

---

## Selection guide

| Deck voice | Recommended pairing |
|------------|---------------------|
| Dev-tool / developer-native | Inter + JetBrains Mono (#1) |
| Distinctive / design-studio | Space Grotesk + IBM Plex Mono (#2) |
| Vercel-native / ultra-modern SaaS | Geist + Geist Mono (#3) |
| Editorial / print-quality | Playfair Display + Inter (#4) |
| Friendly / consumer-facing | DM Sans + DM Mono (#5) |
| Enterprise / B2B / fintech | IBM Plex Sans + IBM Plex Mono (#6) |

---

## Font weight guidance

### Inter / Geist / DM Sans / IBM Plex Sans (sans-serif)
- **Body:** 400 (regular)
- **Bullets / secondary text:** 500 (medium)
- **Subheadings / card headers:** 600 (semibold)
- **Slide titles:** 700 (bold)
- **Cover title / hero stats:** 800 (extrabold)

### Playfair Display (serif)
- **Body:** 400 (regular) — but avoid using Playfair for body; use Inter instead
- **Subheadings:** 500 (medium)
- **Slide titles:** 700 (bold)
- **Cover title:** 800 (extrabold)

### JetBrains Mono / IBM Plex Mono / Geist Mono / DM Mono (monospace)
- **Labels / footers:** 400 (regular)
- **Stats / code blocks:** 500 (medium)
- **Hero numbers:** 700 (bold)

---

## Anti-patterns

### Anti-pattern: using a display font for body text
Playfair Display, Space Grotesk, and other display fonts are designed for headlines. Using them for body text destroys readability. Always pair a display heading font with a readable body font (Inter, IBM Plex Sans, DM Sans).

### Anti-pattern: more than 2 font families
One sans-serif (or serif) for text + one monospace for numbers/code. That's it. Adding a third font (e.g., a script font for accents) creates visual noise.

### Anti-pattern: forgetting the `@import` in global.css
If the `@import` line is missing, the fonts won't load and the slide will fall back to system-ui. Always include the Google Fonts `@import` at the top of `global.css`.

### Anti-pattern: not specifying font weights
`@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap')` only loads weight 400. Specify the weights you need: `Inter:wght@400;500;600;700;800`.

### Anti-pattern: using system fonts only
`font-family: system-ui, sans-serif` produces different fonts on different OSes (San Francisco on macOS, Segoe UI on Windows, Roboto on Android). For consistent slide rendering across machines, always use a Google Fonts `@import`.

---

## CJK (Chinese/Japanese/Korean) considerations

If the deck contains CJK text:

1. **Add a CJK font to the `@import`:**
   ```css
   @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');
   ```

2. **Define a `--font-cn` token:**
   ```css
   --font-cn: 'Inter', 'Noto Sans SC', 'PingFang SC', sans-serif;
   ```

3. **Use `--font-cn` for any CJK text** in slide HTML:
   ```html
   <span style="font-family: var(--font-cn);">中文文本</span>
   ```

4. **Font fallback chain:** Latin font → CJK font → system CJK font. The browser will use the Latin font for Latin characters and the CJK font for CJK characters automatically.

**Recommended CJK fonts:** Noto Sans SC (Simplified Chinese), Noto Sans TC (Traditional Chinese), Noto Sans JP (Japanese), Noto Sans KR (Korean).
