# Performance Budgets & Verification (2026)

## 1.0 Performance Budgets by Design Quadrant

Adhere to these budgets based on your strategic positioning.

| Metric | Institutional (Q1/Q3) | Dynamic (Q2/Q4) | Balanced |
|--------|---------------|---------|----------|
| **Initial JS bundle** | < 120 KB | < 250 KB | < 180 KB |
| **First Contentful Paint** | < 0.8s | < 1.2s | < 1.0s |
| **Largest Contentful Paint** | < 1.2s | < 2.0s | < 1.5s |
| **Time to Interactive** | < 1.5s | < 2.5s | < 2.0s |
| **Cumulative Layout Shift** | < 0.05 | < 0.1 | < 0.05 |
| **Animation Frame Rate** | N/A | 60fps | 60fps |

---

## 2.0 Pre-Commit Performance Checklist

Run these local checks before every commit:

- [ ] **Lighthouse Baseline:** Run Lighthouse on `localhost:3000` (Production Build).
- [ ] **Bundle Analysis:** Run `npm run analyze` to check for unintended large packages.
- [ ] **Image Optimization:** Verify all images in `public/` are compressed (use AVIF/WebP).
- [ ] **Next.js `priority` Check:** Hero images must have the `priority` attribute.
- [ ] **Hydration Check:** No console warnings for hydration mismatches.

---

## 3.0 Pre-Deploy CI Check (Lighthouse CI)

Example configuration for `.lighthouserc.js`:

```js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/'],
      startServerCommand: 'npm run start',
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 1.0 }],
        'categories:best-practices': ['error', { minScore: 1.0 }],
        'categories:seo': ['error', { minScore: 1.0 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
  },
};
```

---

## 4.0 Core Web Vitals Audit Protocol

### 4.1 CLS (Cumulative Layout Shift)
- **Fix:** Reserve space for dynamic content.
- **Implementation:**
```css
.hero-image {
  aspect-ratio: 16 / 9;
  background-color: var(--color-slate-100); /* Placeholder color */
}
```

### 4.2 LCP (Largest Contentful Paint)
- **Fix:** Preload the main font and hero image.
- **Implementation:**
```html
<link rel="preload" href="/fonts/brand-font.woff2" as="font" type="font/woff2" crossorigin="anonymous">
```

### 4.3 INP (Interaction to Next Paint)
- **Fix:** Break up long JS tasks using `requestIdleCallback` or `setTimeout(..., 0)`.
- **Audit:** Interaction latency must be < 200ms.

---

## 5.0 Continuous Performance Monitoring

Use Lighthouse CI and Vercel Analytics to monitor these metrics in production. A task is NOT complete until its performance impact is verified.

---

**See Also:**
- `[11-tech-commitments.md](11-tech-commitments.md)` - Stack standards
- `[16-nextjs-optimization.md](16-nextjs-optimization.md)` - Optimization techniques
