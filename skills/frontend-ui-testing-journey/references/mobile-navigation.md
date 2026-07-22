# Mobile Navigation Testing Reference

## Overview

This document provides a comprehensive taxonomy of mobile navigation failures and testing patterns, enhanced with agent-browser v0.25.3 and chrome-devtools-mcp capabilities.

---

## Quick Start: Mobile Testing Commands

```bash
# Set mobile viewport
agent-browser set device "iPhone 12"

# Or custom viewport
agent-browser set viewport 375 812

# Capture annotated screenshot
agent-browser screenshot --annotate /tmp/mobile.png

# Record video of interaction
agent-browser record start /tmp/mobile-test.webm
agent-browser click @e5  # hamburger button
agent-browser wait 500
agent-browser record stop

# Compare before/after
agent-browser screenshot --annotate /tmp/mobile-before.png
agent-browser click @e5
agent-browser screenshot --annotate /tmp/mobile-after.png
agent-browser diff screenshot --baseline /tmp/mobile-before.png
```

---

## Classes of Mobile Navigation Failures (A-H)

### Class A: Touch Target Size Failures

**Symptom:** Buttons too small for reliable touch input.

**Diagnosis:**
```bash
# Check button dimensions
agent-browser eval 'JSON.stringify(
  Array.from(document.querySelectorAll("button")).map(b => ({
    text: b.textContent?.trim(),
    width: b.offsetWidth,
    height: b.offsetHeight,
    meetsMinimum: b.offsetWidth >= 44 && b.offsetHeight >= 44
  }))
)'

# Or use chrome-devtools for detailed layout
mcporter call chrome-devtools.take_snapshot
# Check uid dimensions in output
```

**Anti-patterns to Avoid:**
```tsx
// ❌ Too small
<button className="p-1 text-xs">Click</button>

// ✅ Correct minimum size (44px)
<button className="p-3 text-sm min-h-[44px] min-w-[44px]">Click</button>
```

**Code Examples:**
```tsx
// Proper touch target
<button className="
  min-h-[44px] min-w-[44px]
  p-3 text-sm
  touch-manipulation
  active:scale-95
">
  Click Me
</button>
```

---

### Class B: Overflow and Scroll Failures

**Symptom:** Content hidden or unreachable due to overflow issues.

**Diagnosis:**
```bash
# Check overflow properties
agent-browser eval 'JSON.stringify({
  overflow: getComputedStyle(document.querySelector(".container")).overflow,
  scrollHeight: document.querySelector(".container").scrollHeight,
  clientHeight: document.querySelector(".container").clientHeight,
  hasScroll: document.querySelector(".container").scrollHeight > document.querySelector(".container").clientHeight
})'

# Visual check with annotated screenshot
agent-browser screenshot --annotate /tmp/overflow-check.png
```

**Anti-patterns to Avoid:**
```tsx
// ❌ Fixed height without scroll
<div className="h-screen">Content</div>

// ✅ Proper scroll container
<div className="h-screen overflow-y-auto">Content</div>
```

**Code Examples:**
```tsx
// Scrollable container
<div className="
  h-screen overflow-y-auto
  overscroll-contain
  -webkit-overflow-scrolling: touch
">
  {children}
</div>
```

---

### Class C: Hamburger Menu Failures

**Symptom:** Mobile menu doesn't open or close properly.

**Diagnosis:**
```bash
# Check menu state
agent-browser eval 'JSON.stringify({
  menuVisible: document.querySelector("[role=\"navigation\"]")?.offsetHeight > 0,
  triggerExists: !!document.querySelector("[aria-label=\"Menu\"]"),
  ariaExpanded: document.querySelector("[aria-label=\"Menu\"]")?.getAttribute("aria-expanded")
})'

# Test hamburger interaction with video
agent-browser record start /tmp/hamburger-test.webm
agent-browser click @e5  # hamburger button
agent-browser wait 500
agent-browser eval 'document.querySelector("[aria-expanded]")?.getAttribute("aria-expanded")'
agent-browser record stop
```

**Anti-patterns to Avoid:**
```tsx
// ❌ No ARIA attributes
<button onClick={toggleMenu}>
  <MenuIcon />
</button>

// ✅ Proper ARIA support
<button
  onClick={toggleMenu}
  aria-expanded={isOpen}
  aria-label="Toggle menu"
>
  <MenuIcon />
</button>
```

**Code Examples:**
```tsx
// Accessible mobile menu
<button
  onClick={() => setIsOpen(!isOpen)}
  aria-expanded={isOpen}
  aria-controls="mobile-menu"
  aria-label={isOpen ? "Close menu" : "Open menu"}
>
  {isOpen ? <XIcon /> : <MenuIcon />}
</button>

<nav
  id="mobile-menu"
  aria-hidden={!isOpen}
  className={cn(
    "fixed inset-0 z-50",
    isOpen ? "translate-x-0" : "translate-x-full"
  )}
>
  {/* Menu content */}
</nav>
```

---

### Class D: Viewport Meta Tag Failures

**Symptom:** Page doesn't scale properly on mobile devices.

**Diagnosis:**
```bash
# Check viewport meta tag
agent-browser eval 'document.querySelector("meta[name=\"viewport\"]")?.content'

# Test multiple device viewports
agent-browser set device "iPhone SE"
agent-browser screenshot /tmp/viewport-se.png
agent-browser set device "iPhone 12"
agent-browser screenshot /tmp/viewport-12.png
agent-browser set device "iPad"
agent-browser screenshot /tmp/viewport-ipad.png
```

**Anti-patterns to Avoid:**
```html
<!-- ❌ User-scalable disabled -->
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">

<!-- ✅ Accessible viewport -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Code Examples:**
```html
<!-- Proper viewport configuration -->
<meta
  name="viewport"
  content="width=device-width, initial-scale=1, viewport-fit=cover"
>
```

---

### Class E: Touch Event Handling Failures

**Symptom:** Touch events not firing or firing incorrectly.

**Diagnosis:**
```bash
# Check touch event listeners
agent-browser eval 'JSON.stringify({
  hasTouchStart: !!document.querySelector(".touch-target")?.ontouchstart,
  hasTouchEnd: !!document.querySelector(".touch-target")?.ontouchend,
  hasClick: !!document.querySelector(".touch-target")?.onclick,
  pointerEvents: getComputedStyle(document.querySelector(".touch-target")).pointerEvents
})'

# Test touch with video
agent-browser record start /tmp/touch-test.webm
agent-browser eval 'document.querySelector(".touch-target").dispatchEvent(new TouchEvent("touchstart", { bubbles: true }))'
agent-browser wait 100
agent-browser eval 'document.querySelector(".touch-target").dispatchEvent(new TouchEvent("touchend", { bubbles: true }))'
agent-browser record stop
```

**Anti-patterns to Avoid:**
```tsx
// ❌ Only listening to click
<button onClick={handleClick}>Touch me</button>

// ✅ Handle both click and touch
<button
  onClick={handleClick}
  onTouchEnd={handleTouchEnd}
  className="touch-manipulation"
>
  Touch me
</button>
```

**Code Examples:**
```tsx
// Proper touch handling
<button
  onClick={handleClick}
  onTouchEnd={(e) => {
    e.preventDefault();
    handleClick();
  }}
  className="
    touch-manipulation
    select-none
    active:scale-95
    transition-transform
  "
>
  Touch Me
</button>
```

---

### Class F: Responsive Breakpoint Failures

**Symptom:** Layout breaks at certain viewport widths.

**Diagnosis:**
```bash
# Test multiple viewports with batch
echo '[
  ["set", "viewport", "320", "568"],
  ["screenshot", "--annotate", "/tmp/bp-320.png"],
  ["set", "viewport", "375", "667"],
  ["screenshot", "--annotate", "/tmp/bp-375.png"],
  ["set", "viewport", "414", "896"],
  ["screenshot", "--annotate", "/tmp/bp-414.png"],
  ["set", "viewport", "768", "1024"],
  ["screenshot", "--annotate", "/tmp/bp-768.png"]
]' | agent-browser batch

# Or use device presets
for device in "iPhone SE" "iPhone 12" "iPad"; do
  agent-browser set device "$device"
  agent-browser screenshot --annotate "/tmp/device-${device// /-}.png"
done
```

**Anti-patterns to Avoid:**
```tsx
// ❌ Fixed widths
<div className="w-[500px]">Content</div>

// ✅ Responsive widths
<div className="w-full max-w-[500px] px-4">Content</div>
```

**Code Examples:**
```tsx
// Responsive grid
<div className="
  grid grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  gap-4 px-4
">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

---

### Class G: Font Scaling Failures

**Symptom:** Text too small or too large on mobile.

**Diagnosis:**
```bash
# Check font sizes
agent-browser eval 'JSON.stringify(
  Array.from(document.querySelectorAll("p, h1, h2, h3")).map(e => ({
    tag: e.tagName,
    fontSize: getComputedStyle(e).fontSize,
    lineHeight: getComputedStyle(e).lineHeight
  }))
)'

# Compare mobile vs desktop
agent-browser set viewport 375 812
agent-browser eval 'getComputedStyle(document.querySelector("h1")).fontSize'
agent-browser set viewport 1280 720
agent-browser eval 'getComputedStyle(document.querySelector("h1")).fontSize'
```

**Anti-patterns to Avoid:**
```tsx
// ❌ Fixed pixel sizes
<p className="text-[12px]">Small text</p>

// ✅ Responsive text
<p className="text-sm sm:text-base">Responsive text</p>
```

**Code Examples:**
```tsx
// Responsive typography
<h1 className="
  text-2xl sm:text-3xl lg:text-4xl
  font-bold leading-tight
">
  Heading
</h1>

<p className="
  text-sm sm:text-base
  leading-relaxed
">
  Body text
</p>
```

---

### Class H: Gesture Conflict Failures

**Symptom:** Swipe gestures interfere with scrolling.

**Diagnosis:**
```bash
# Check touch-action property
agent-browser eval 'JSON.stringify({
  bodyTouchAction: getComputedStyle(document.body).touchAction,
  containerTouchAction: getComputedStyle(document.querySelector(".container")).touchAction
})'

# Test scroll behavior with video
agent-browser set device "iPhone 12"
agent-browser record start /tmp/scroll-test.webm
agent-browser eval 'document.querySelector(".container").scrollBy({ top: 100, behavior: "smooth" })'
agent-browser wait 1000
agent-browser record stop
```

**Anti-patterns to Avoid:**
```tsx
// ❌ Touch-action none on scrollable container
<div className="touch-none overflow-y-auto">Content</div>

// ✅ Proper touch-action
<div className="touch-pan-y overflow-y-auto">Content</div>
```

**Code Examples:**
```tsx
// Proper gesture handling
<div
  className="
    touch-pan-y
    overscroll-contain
    overflow-y-auto
  "
  onTouchStart={handleTouchStart}
  onTouchMove={handleTouchMove}
  onTouchEnd={handleTouchEnd}
>
  {children}
</div>
```

---

## Mobile Testing Workflow

### 1. Setup Mobile Environment

```bash
# Set device
agent-browser set device "iPhone 12"

# Or custom viewport
agent-browser set viewport 375 812

# Configure for mobile testing
agent-browser set geo 1.3521 103.8198  # Singapore coordinates
agent-browser set media dark  # Test dark mode
```

### 2. Test Touch Targets (Class A)

```bash
agent-browser eval 'Array.from(document.querySelectorAll("button, a")).filter(e => e.offsetWidth < 44 || e.offsetHeight < 44).length'
# Should return 0
```

### 3. Test Navigation (Classes C, H)

```bash
# Record hamburger test
agent-browser record start /tmp/nav-test.webm
agent-browser screenshot --annotate /tmp/nav-before.png
agent-browser click @e5  # hamburger
agent-browser wait 500
agent-browser screenshot --annotate /tmp/nav-after.png
agent-browser record stop

# Check for race condition (Class H)
agent-browser eval 'JSON.stringify({
  expanded: document.querySelector("[aria-expanded]")?.getAttribute("aria-expanded"),
  menuVisible: document.querySelector("[role=\"navigation\"]")?.offsetHeight > 0
})'
```

### 4. Test Responsive Breakpoints (Class F)

```bash
# Batch test multiple viewports
echo '[
  ["open", "http://localhost:5173/"],
  ["set", "viewport", "320", "568"],
  ["screenshot", "--annotate", "/tmp/mobile-320.png"],
  ["set", "viewport", "375", "812"],
  ["screenshot", "--annotate", "/tmp/mobile-375.png"],
  ["set", "viewport", "768", "1024"],
  ["screenshot", "--annotate", "/tmp/tablet-768.png"],
  ["set", "viewport", "1280", "720"],
  ["screenshot", "--annotate", "/tmp/desktop-1280.png"]
]' | agent-browser batch
```

### 5. Performance Test (chrome-devtools)

```bash
# Lighthouse mobile audit
mcporter call chrome-devtools.navigate_page url=http://localhost:5173/
mcporter call chrome-devtools.emulate viewport="375x812x3,mobile,touch"
mcporter call chrome-devtools.lighthouse_audit

# Performance trace on mobile
mcporter call chrome-devtools.performance_start_trace reload=true
mcporter call chrome-devtools.performance_stop_trace
```

---

## Mobile Testing Commands (Reference)

### Viewport Testing

```bash
# Set mobile viewport
agent-browser set viewport 375 667

# Use device presets
agent-browser set device "iPhone SE"    # 320x568
agent-browser set device "iPhone 12"    # 390x844
agent-browser set device "iPad"         # 768x1024

# Capture mobile screenshot
agent-browser screenshot --annotate /tmp/mobile.png

# Reset to desktop
agent-browser set viewport 1280 720
```

### Touch Simulation

```bash
# Simulate tap
agent-browser click @e5

# Simulate long press
agent-browser eval '(function() {
  const el = document.querySelector(".long-press-target");
  el.dispatchEvent(new TouchEvent("touchstart", { bubbles: true }));
  setTimeout(() => {
    el.dispatchEvent(new TouchEvent("touchend", { bubbles: true }));
  }, 500);
  return "simulated";
})()'
```

### Batch Responsive Testing

```bash
# Test multiple viewports
for width in 320 375 414 768 1024 1280; do
  agent-browser set viewport $width 800
  agent-browser screenshot --annotate "/tmp/viewport-${width}.png"
done

# Or use batch
echo '[
  ["set", "viewport", "320", "800"],
  ["screenshot", "--annotate", "/tmp/v320.png"],
  ["set", "viewport", "375", "800"],
  ["screenshot", "--annotate", "/tmp/v375.png"]
]' | agent-browser batch
```

---

## Best Practices

### 1. Always Test on Real Viewports

```bash
# Common mobile viewports
agent-browser set device "iPhone SE"     # 320x568
agent-browser set device "iPhone 8"      # 375x667
agent-browser set device "iPhone 12"     # 390x844
agent-browser set device "iPhone 11"     # 414x896
agent-browser set device "iPad"          # 768x1024
```

### 2. Verify Touch Targets

- Minimum 44x44px for buttons
- 8px spacing between targets
- Visual feedback on touch

### 3. Test Landscape Orientation

```bash
# Landscape mobile
agent-browser set viewport 812 390  # iPhone 12 landscape
agent-browser screenshot --annotate /tmp/landscape.png
```

### 4. Verify Accessibility

```bash
# Check ARIA attributes
agent-browser eval 'JSON.stringify({
  ariaExpanded: document.querySelector("[aria-expanded]")?.getAttribute("aria-expanded"),
  ariaHidden: document.querySelector("[aria-hidden]")?.getAttribute("aria-hidden"),
  ariaLabel: document.querySelector("[aria-label]")?.getAttribute("aria-label")
})'

# Run Lighthouse accessibility audit
mcporter call chrome-devtools.lighthouse_audit
```

### 5. Use Annotated Screenshots for Evidence

```bash
# Capture with element labels
agent-browser screenshot --annotate /tmp/mobile-audit.png

# Compare before/after
agent-browser screenshot --annotate /tmp/before.png
# ... fix applied ...
agent-browser diff screenshot --baseline /tmp/before.png
```

---

## Quick Reference

### Common Mobile Viewports

| Device | Width | Height | agent-browser command |
|--------|-------|--------|----------------------|
| iPhone SE | 320 | 568 | `set device "iPhone SE"` |
| iPhone 8 | 375 | 667 | `set viewport 375 667` |
| iPhone 12/13 | 390 | 844 | `set device "iPhone 12"` |
| iPhone 11 | 414 | 896 | `set viewport 414 896` |
| iPad | 768 | 1024 | `set device "iPad"` |
| iPad Pro | 1024 | 1366 | `set viewport 1024 1366` |

### Touch Target Guidelines

| Element | Minimum Size | Recommended |
|---------|--------------|-------------|
| Button | 44x44px | 48x48px |
| Link | 44x44px | 48x48px |
| Icon | 24x24px | 32x32px |
| Input | 44px height | 48px height |

### Quick Diagnosis Commands

```bash
# Class A: Touch targets
agent-browser eval 'Array.from(document.querySelectorAll("button")).filter(b => b.offsetWidth < 44).length'

# Class B: Overflow
agent-browser eval 'document.querySelector(".container").scrollHeight > window.innerHeight'

# Class C: Hamburger
agent-browser eval 'document.querySelector("[aria-expanded]")?.getAttribute("aria-expanded")'

# Class D: Viewport
agent-browser eval 'document.querySelector("meta[name=\"viewport\"]")?.content'

# Class E: Touch handlers
agent-browser eval 'getComputedStyle(document.body).touchAction'

# Class F: Breakpoints
agent-browser eval 'window.innerWidth'

# Class G: Font sizes
agent-browser eval 'getComputedStyle(document.querySelector("p")).fontSize'

# Class H: Gesture conflicts
agent-browser eval 'getComputedStyle(document.querySelector(".scroll-container")).touchAction'
```

---

**Reference Version:** 2.0.0  
**Last Updated:** March 26, 2026  
**Source:** AI Academy Project + agent-browser v0.25.3 + chrome-devtools-mcp  
**Status:** Production Ready ✅
