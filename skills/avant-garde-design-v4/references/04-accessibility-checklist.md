# WCAG AAA Accessibility Checklist

## Level A Requirements (Minimum)

### Perceivable

**1.1 Text Alternatives**
- [ ] All images have meaningful `alt` text
- [ ] Decorative images have empty `alt=""`
- [ ] Complex images have extended descriptions
- [ ] Form inputs have associated labels
- [ ] Icons used as buttons have accessible names

**1.2 Time-based Media**
- [ ] Prerecorded audio has text transcript
- [ ] Prerecorded video has captions
- [ ] Live audio has captions

**1.3 Adaptable**
- [ ] Content structure is semantic (proper heading hierarchy)
- [ ] Meaningful sequence is preserved
- [ ] Form inputs have visible labels
- [ ] Form inputs have accessible names

**1.4 Distinguishable**
- [ ] Color is not the only visual means of conveying information
- [ ] Audio control is provided for auto-playing audio
- [ ] Text can be resized up to 200% without loss of content
- [ ] Contrast ratio: 4.5:1 for normal text (AA), 7:1 for AAA
- [ ] Contrast ratio: 3:1 for large text (AA), 4.5:1 for AAA
- [ ] Non-text contrast: 3:1 for UI components

### Operable

**2.1 Keyboard Accessible**
- [ ] All functionality is keyboard accessible
- [ ] No keyboard traps
- [ ] Keyboard shortcuts can be turned off/remapped

**2.2 Enough Time**
- [ ] Time limits can be turned off, adjusted, or extended
- [ ] Moving content can be paused, stopped, or hidden

**2.3 Seizures and Physical Reactions**
- [ ] No content flashes more than 3 times per second
- [ ] Animation from interactions can be disabled

**2.4 Navigable**
- [ ] Skip links are provided
- [ ] Pages have descriptive titles
- [ ] Focus order is logical
- [ ] Focus state is visible
- [ ] Headings and labels are descriptive
- [ ] Current location is indicated in navigation

**2.5 Input Modalities**
- [ ] Touch targets are at least 44x44 pixels
- [ ] Pointer gestures have single-pointer alternatives
- [ ] Label in name: Accessible name matches visible label

### Understandable

**3.1 Readable**
- [ ] Page language is specified (`lang` attribute)
- [ ] Language of parts is specified
- [ ] Reading level is appropriate

**3.2 Predictable**
- [ ] Focus doesn't trigger context change
- [ ] Input doesn't trigger context change
- [ ] Navigation is consistent across pages

**3.3 Input Assistance**
- [ ] Error identification is provided
- [ ] Labels or instructions are provided
- [ ] Error suggestions are provided

### Robust

**4.1 Compatible**
- [ ] Parsing: Valid HTML
- [ ] Name, Role, Value: All UI components have accessible properties
- [ ] Status messages can be programmatically determined

---

## Level AA Requirements

### Perceivable

**1.4 Distinguishable (Additional)**
- [ ] Contrast ratio minimum 4.5:1 for normal text
- [ ] Contrast ratio minimum 3:1 for large text
- [ ] Text can be resized up to 200%

### Operable

**2.4 Navigable (Additional)**
- [ ] Multiple ways to find pages within a site
- [ ] Headings and labels describe topic or purpose

---

## Level AAA Requirements (Enhanced)

### Perceivable

**1.4 Distinguishable**
- [ ] Contrast ratio minimum 7:1 for normal text
- [ ] Contrast ratio minimum 4.5:1 for large text
- [ ] Visual presentation: Width does not exceed 80 characters
- [ ] Visual presentation: Text is not justified
- [ ] Visual presentation: Line spacing is at least 1.5

### Operable

**2.5 Input Modalities**
- [ ] Touch targets are at least 44x44 CSS pixels

### Understandable

**3.1 Readable**
- [ ] Reading level does not exceed lower secondary education
- [ ] Pronunciation guides are available for words where meaning depends on pronunciation

---

## Implementation Code Examples

### Semantic Structure

```html
<!-- Correct heading hierarchy -->
<main>
  <h1>Page Title</h1>
  <section>
    <h2>Section Heading</h2>
    <article>
      <h3>Article Heading</h3>
      <h4>Subsection</h4>
    </article>
  </section>
</main>
```

### Skip Links

```tsx
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

<main id="main-content">
  {/* Content */}
</main>
```

### Focus Management

```tsx
// Custom focus ring
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2">
  Click me
</button>
```

### Form Accessibility

```tsx
<div>
  <label htmlFor="email" className="block mb-1 font-medium">
    Email Address <span className="text-red-500" aria-hidden="true">*</span>
  </label>
  <input
    id="email"
    type="email"
    name="email"
    required
    aria-required="true"
    aria-describedby="email-hint email-error"
    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-brand-500"
  />
  <p id="email-hint" className="text-sm text-muted-foreground mt-1">
    We'll never share your email.
  </p>
  {error && (
    <p id="email-error" role="alert" className="text-sm text-red-500 mt-1">
      {error}
    </p>
  )}
</div>
```

### Icon Button Accessibility

```tsx
// Icon-only button
<button
  aria-label="Close dialog"
  className="p-2 rounded-lg hover:bg-muted focus-visible:ring-2 focus-visible:ring-brand-500"
>
  <XIcon aria-hidden="true" className="w-5 h-5" />
</button>

// Button with visible text and icon
<button className="flex items-center gap-2">
  <SaveIcon aria-hidden="true" className="w-4 h-4" />
  <span>Save Changes</span>
</button>
```

### Reduced Motion Support

```tsx
// Hook for detecting reduced motion preference
import { useEffect, useState } from 'react';

export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}

// Usage
function AnimatedComponent() {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      initial={prefersReducedMotion ? {} : { opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
    >
      Content
    </motion.div>
  );
}
```

---

## Testing Tools

### Automated Testing
- **axe DevTools**: Browser extension for automated testing
- **Lighthouse**: Built into Chrome DevTools
- **WAVE**: Web Accessibility Evaluation Tool
- **Pa11y**: Command-line accessibility tester

### Manual Testing
- **Keyboard Navigation**: Tab through entire page
- **Screen Reader Testing**: VoiceOver (Mac), NVDA (Windows)
- **Zoom Testing**: 200% zoom, reflow at 400%
- **Color Contrast**: WebAIM Contrast Checker

---

## ADA Title II Compliance (Effective April 24, 2026)

Federal law requires all digital content to meet WCAG 2.1 Level AA standards. While AAA is not yet legally required, it represents mastery and future-proofing.

**Key Requirements:**
- All public-facing digital content
- Mobile applications
- Internal systems used by employees
- Third-party content integrated into your site

**Penalties for Non-Compliance:**
- Legal action
- Financial penalties
- Reputation damage
- Loss of federal contracts

---

**See Also:**
- `[SKILL.md](../SKILL.md)` - Main skill file
- `[05-component-patterns.md](05-component-patterns.md)` - Accessible component patterns
