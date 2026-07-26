# Global CSS Template — Canonical Scaffold

> The starting point for every `global.css`. Copy this scaffold, then customize the palette + typography tokens for the specific deck.

---

## The scaffold

```css
/* <deck-name> — <style-name> */
@import url('<google-fonts-import-url>');

:root {
  /* === PALETTE (customize per deck) === */
  --bg: #0D1117;
  --bg-elevated: #161B22;
  --bg-surface: #1C2128;
  --border: #30363D;
  --border-muted: #21262D;
  --primary: #E6EDF3;
  --primary-muted: #8B949E;
  --primary-subtle: #6E7681;
  --accent: #58A6FF;
  --accent-soft: rgba(88, 166, 255, 0.12);
  --accent-glow: rgba(88, 166, 255, 0.25);
  --success: #3FB950;
  --warning: #D29922;
  --danger: #F85149;

  /* === TYPOGRAPHY TOKENS (customize per deck) === */
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-num: 'JetBrains Mono', 'SF Mono', monospace;
  --font-cn: 'Inter', 'PingFang SC', sans-serif;

  /* === TYPE SCALE === */
  --fs-display: 120px;
  --fs-h1: 56px;
  --fs-h2: 40px;
  --fs-h3: 28px;
  --fs-body: 18px;
  --fs-small: 15px;
  --fs-micro: 13px;
  --fs-label: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  background: var(--bg);
  color: var(--primary);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* === SLIDE CANVAS === */
.slide {
  width: 1280px;
  height: 720px;
  background: var(--bg);
  color: var(--primary);
  overflow: hidden;
  position: relative;
  padding: 64px 72px;
  display: flex;
  flex-direction: column;
}

/* === UTILITY CLASSES (OK to ship) === */

/* Subtle grid background */
.grid-bg {
  background-image:
    linear-gradient(rgba(88, 166, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(88, 166, 255, 0.04) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* Accent dot — Linear-style section marker */
.accent-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 12px var(--accent-glow);
}

/* Card surface */
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px;
}

.card-accent {
  border-left: 3px solid var(--accent);
}

/* Eyebrow label */
.eyebrow {
  font-family: var(--font-num);
  font-size: var(--fs-label);
  font-weight: 500;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Footer bar */
.footer {
  position: absolute;
  bottom: 28px;
  left: 72px;
  right: 72px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-num);
  font-size: var(--fs-micro);
  color: var(--primary-subtle);
  border-top: 1px solid var(--border-muted);
  padding-top: 16px;
}

/* Mono number style */
.mono { font-family: var(--font-num); font-feature-settings: 'tnum' 1; }

/* Color utilities */
.accent { color: var(--accent); }
.muted { color: var(--primary-muted); }
.subtle { color: var(--primary-subtle); }

/* Tag pill */
.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--accent-soft);
  border: 1px solid rgba(88, 166, 255, 0.3);
  border-radius: 6px;
  font-family: var(--font-num);
  font-size: var(--fs-micro);
  color: var(--accent);
  font-weight: 500;
}

/* Material Icons baseline */
.material-icons { font-family: 'Material Icons'; font-size: 20px; vertical-align: middle; }
```

---

## Customization checklist

When creating a new deck's `global.css`:

1. **Replace the `@import` line** with the Google Fonts URL for the chosen typography pairing.
2. **Replace the palette variables** (`--bg`, `--primary`, `--accent`, and tonal stops) with the chosen palette.
3. **Replace the typography tokens** (`--font-heading`, `--font-body`, `--font-num`) with the chosen fonts.
4. **Update the accent-soft and accent-glow** values to match the new accent color (use `rgba()` with the accent's RGB values).
5. **Update the `.tag` border color** to match the new accent.
6. **Update the `.grid-bg` line color** to match the new accent.

---

## Forbidden in global.css

### Pre-baked typography classes
```css
/* ❌ FORBIDDEN */
.h-display { font-family: var(--font-heading); font-size: 120px; font-weight: 800; line-height: 1.1; }
.h-1 { ... }
.h-2 { ... }
.cn-sub { ... }
```
Sub-agents will fight these. Define tokens only; let sub-agents apply per-slide inline styles.

### Tailwind-colliding class names
```css
/* ❌ FORBIDDEN — collides with Tailwind utilities */
.h-1 { ... }     /* Tailwind height: 4px */
.h-2 { ... }     /* Tailwind height: 8px */
.h-3 { ... }     /* Tailwind height: 12px */
.hidden { ... }  /* Tailwind display: none */
.block { ... }   /* Tailwind display: block */
.flex { ... }    /* Tailwind display: flex */
.container { ... } /* Tailwind max-width */
```

### Per-slide layout CSS
```css
/* ❌ FORBIDDEN — belongs in the slide HTML */
.cover-layout { display: grid; grid-template-columns: 55% 45%; }
.timeline-card { width: 210px; height: 280px; }
```
Per-slide layout lives in each slide's HTML via inline styles or a `<style>` block.

### More than ~150 lines
If `global.css` exceeds 150 lines, you're probably putting per-slide CSS in it. Split it back out.

---

## Anti-patterns

### Anti-pattern: shipping a 300-line global.css
This usually means per-slide layout CSS leaked in. Keep it under 150 lines — tokens + utilities only.

### Anti-pattern: defining `.hidden` in global.css
Tailwind already defines `.hidden { display: none }`. If you redefine it, the cascade order matters and sub-agents may get confused. Use Tailwind's `hidden` class directly on `<aside data-notes class="hidden">`.

### Anti-pattern: hardcoding font-family in utility classes
`.eyebrow { font-family: 'JetBrains Mono'; }` is brittle. Use `.eyebrow { font-family: var(--font-num); }` so a token change propagates.

### Anti-pattern: no tonal stops
Sub-agents need `--bg-elevated`, `--bg-surface`, `--border`, `--border-muted`, `--primary-muted`, `--primary-subtle` for card surfaces and hierarchy. Without them, sub-agents invent colors that may not match the palette.
