# Strategic Design Patterns Catalog

## 1.0 Credibility & Trust Patterns

### 1.1 The "Institutional Badge" Bar
- **Goal:** Build trust through credentials and outcome metrics.
- **Visual:** Monochromatic, high-end gray/slate.

```tsx
export const TrustSignals = () => {
  return (
    <div className="flex flex-wrap items-center justify-center gap-12 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
      <Logo1 className="h-8" />
      <Logo2 className="h-8" />
      <Logo3 className="h-8" />
      <div className="h-8 w-px bg-border" />
      <div className="flex flex-col text-sm font-medium">
        <span className="text-foreground">98.4% Placement Rate</span>
        <span className="text-muted-foreground text-xs uppercase tracking-widest">Q1 2026 Audit</span>
      </div>
    </div>
  );
};
```

---

## 2.0 Visual Hierarchy Patterns

### 2.1 Typographic Focal Point
- **Goal:** Direct user attention instantly.
- **Visual:** Use a massive scale contrast between headline and body text.

```css
@theme {
  --text-headline: 8rem; /* 128px */
  --leading-headline: 0.95;
}
```

```tsx
<h1 className="text-headline font-black leading-headline tracking-super-tight mb-12">
  Design <br /> The <span className="text-brand-500">Unseen</span>.
</h1>
<p className="max-w-md text-xl leading-relaxed text-muted-foreground">
  Strategic positioning meets avant-garde aesthetics. 
</p>
```

---

## 3.0 Conversion Psychology Patterns

### 3.1 Status-Based Urgency (B2B/Institutional)
- **Goal:** Drive action without looking "cheap".
- **Visual:** Use "status pills" instead of blinking timers.

```tsx
<div className="inline-flex items-center gap-2 rounded-full border border-brand-500/20 bg-brand-500/5 px-4 py-1 text-xs font-semibold uppercase tracking-widest text-brand-500">
  <span className="h-2 w-2 rounded-full bg-brand-500 animate-pulse" />
  Enrollment Open for Q2 Cohort
</div>
```

---

## 4.0 Content Narrative Patterns

### 4.1 Asymmetrical Feature Narrative
- **Goal:** Break the "grid of cards" monotony.
- **Visual:** Alternating text/image layout with intentional whitespace offsets.

```tsx
<section className="container py-24">
  <div className="grid md:grid-cols-12 items-center gap-12 lg:gap-24">
    <div className="md:col-span-7 lg:col-span-8 aspect-video rounded-3xl bg-slate-100 overflow-hidden">
      {/* Media Content */}
    </div>
    <div className="md:col-span-5 lg:col-span-4 relative">
       <span className="absolute -left-12 -top-12 text-9xl font-black text-slate-50 opacity-10">01</span>
       <h2 className="text-4xl font-bold mb-6">Master the Oxide Engine.</h2>
       <p className="text-lg text-muted-foreground">Detailed technical narrative...</p>
    </div>
  </div>
</section>
```

---

## 5.0 Anti-Patterns Avoided

| Pattern | Anti-Pattern Avoided | Correct Principle |
|---------|---------------------|-------------------|
| **Badge Bar** | Hero-split logos | Group logos to signal trust as a block. |
| **Status Pills** | Countdown timers | Authentic urgency > artificial pressure. |
| **Headline Scale** | Safe size hierarchy | Use scale to signal confidence. |
| **Narrative Flow** | Generic card grid | Scroll narrative drives focus. |

---

**See Also:**
- `[12-anti-generic-checklist.md](12-anti-generic-checklist.md)` - Design audit
- `[14-animation-standards.md](14-animation-standards.md)` - Motion patterns
