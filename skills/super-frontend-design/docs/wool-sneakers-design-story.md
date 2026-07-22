# Design Story: WOOL RUNNERS SG

> **Narrative**: "From Alpine meadows to Singapore streets — merino wool reimagined for tropical urban life"  
> **Stage**: PEAK (Storytelling Through Design)  
> **Emotion**: Comfort + Innovation + Tropical Urban Grit

---

## 1. The Hook (Visceral Level)

**Hero Headline**: *"Wool for the Tropical Urbanite"*

**Visceral Impact**:
- First impression: Warm white (#F5F0EB) evokes natural wool, not sterile tech
- Oat-colored (#E8DCC8) cards feel like touching merino fiber
- Foggy gray (#B8B0A8) suggests Singapore's urban haze, concrete jungle backdrop
- Typography: Instrument Serif italic "Tropical Urbanite" — editorial luxury meets street smarts

**Color Psychology**:
- Warm neutrals = "This is natural, breathable, soft"
- Charcoal accents = "This is urban, durable, serious footwear"
- No bright colors = "We don't need gimmicks, the material speaks"

---

## 2. The Journey (Behavioral Level)

### 2.1 Hero Section → "Shop Now" Click
**Behavioral Experience**:
- Foggy gradient background (135deg warm white → oat → foggy gray-light)
- Wool texture overlay (opacity 0.08) — subconscious tactile cue
- CTA buttons: Charcoal bg + warm white text (13.5:1 contrast)
- Hover: Scale(1.05) — "This button invites clicking"

### 2.2 Brand Story Section
**Narrative Flow**:
1. **Natural Temperature Regulation** → "Merino adapts to your body" (scientific trust)
2. **Urban Durability** → "From MRT stations to park connectors" (Singapore-specific)
3. **Sustainable Choice** → "Carbon-neutral shipping to Singapore" (values alignment)

**Behavioral Reinforcement**:
- Each card: Warm white bg on oat section (clean information hierarchy)
- Readable: 1.6 line-height, 0.875rem secondary text
- Icons (🌡️💧🌿): Quick visual anchors, scannable

### 2.3 Product Grid (The Core Experience)
**Product Names** (Behavioral Design):
- **Urban Strider** → For the daily commute (MRT, office)
- **Garden Runner** → For weekend BBT, park connectors
- **Metro Hiker** → For the adventurous (exploring Singapore's neighborhoods)

**Interactive Elements**:
- Size selector: 44×44px buttons (WCAG AAA touch targets)
- Selected state: Charcoal fill (clear visual feedback)
- "Add to Cart": Tactile Maximalism — button squishes on click (scale 0.95 → 1.0)

### 2.4 Shopping Cart (The Climax)
**Drawer Animation**:
- Slide from right (translateX: 100% → 0) in 300ms cubic-bezier(0.4, 0, 0.2, 1)
- Overlay fades in (opacity: 0 → 1) — focus is on cart
- Items fade in sequentially (staggered 150ms delays)
- Remove button: Underlined, red-hover (clear destructive action)

**Behavioral Completions**:
- Quantity updates → Total recalculates instantly
- "Proceed to Checkout" → Green pasture icon (🌿) signals "eco-friendly purchase")

---

## 3. The Memory (Reflective Level)

### 3.1 Post-Purchase Reflection
**What the user remembers**:
- "I bought wool sneakers designed for Singapore's heat" (functional uniqueness)
- "The website felt like touching wool" (tactile UI differentiation)
- "They get it — 32°C, 80% humidity is no joke" (market empathy)

### 3.2 Brand Story Arc (PEAK Stage)
```
Act 1: PROBLEM (Hero)
  "Synthetic sneakers + Singapore humidity = Sweaty disaster"

Act 2: SOLUTION (Story + Materials)
  "Merino wool: Naturally breathable, temperature-regulating, moisture-wicking"

Act 3: PROOF (Product Grid)
  "3 styles, each engineered for Singapore's urban terrain"

Act 4: ACTION (Cart + Checkout)
  "Join the tropical urbanite movement — comfort without compromise"
```

---

## 4. Storytelling Design Elements

### 4.1 Tactile Maximalism (Anti-Generic)
| Element | Tactile Cue | Why It Works |
|---------|-------------|---------------|
| **Wool Texture Overlay** | SVG circle pattern, opacity 0.08 | Subconscious "this is wool" signal |
| **Oat-Colored Cards** | Soft, warm background | "Touch me, I'm comfortable" |
| **Squishy Buttons** | Scale(1.05) hover, Scale(0.98) active | Physical button press simulation |
| **Foggy Gradient** | 135deg warm white → oat → foggy gray | "Urban haze meets natural warmth" |

### 4.2 Micro-Storytelling (SATISFYING Stage)
| Interaction | Story Beat | Timing |
|-------------|------------|--------|
| **Page Load** | "Welcome to the wool revolution" | Hero fades in 600ms |
| **Product Hover** | "Feel the texture" | Card lifts 4px, 150ms |
| **Add to Cart** | "Your comfort journey begins" | Button squish + cart badge animates |
| **Cart Open** | "Review your choices" | Slide-in 300ms, overlay fades |

---

## 5. Emotional Design Matrix

### 5.1 Target Emotions by Section
| Section | Primary Emotion | Secondary Emotion | Color Strategy |
|---------|-----------------|--------------------|----------------|
| **Hero** | Curiosity + Desire | "I need this for SG heat" | Warm white + Charcoal contrast |
| **Story** | Trust + Security | "This is scientifically proven" | Oat cards, clean layout |
| **Products** | Excitement + Belonging | "These are MY people" | Product cards, size selection |
| **Cart** | Anticipation + Pride | "I'm making the right choice" | Clear summary, eco-badges |

### 5.2 Singapore-Specific Emotional Anchors
- **MRT Stations** → Daily commute comfort (relatable pain point)
- **32°C, 80% Humidity** → Specific climate data (credibility)
- **Park Connectors** → Weekend lifestyle aspiration
- **Urban Exploration** → Adventurous identity (Metro Hiker)

---

## 6. Anti-Generic Narrative Choices

### 6.1 Rejected Tropes (Why They Fail)
| Generic Trope | Why We Rejected It | Our Alternative |
|---------------|---------------------|------------------|
| **"Sustainable Footwear"** | Every brand says this | "Tested at 32°C, 80% humidity — Singapore Climate Certified" |
| **Purple Gradient Hero** | AI-generated cliché | Warm white → Oat → Foggy Gray (tactile, warm) |
| **Bento Grid Products** | Predictable, boring | Asymmetric visual hierarchy, massive typography |
| **"Buy Now" CTA** | Aggressive, salesy | "Shop the Drop" (exclusive, limited) |

### 6.2 Unique Narrative Elements
- **Merino Micron Rating** (18.5 micron) → Premium quality signal
- **Weight Comparison** ("18% lighter than average") → Quantified benefit
- **Stack Height** (8mm for Garden Runner) → Technical detail for enthusiasts
- **Carbon-Neutral Shipping** → Specific to Singapore (local trust)

---

## 7. Peak Moment: The "Aha!" Reveal

**The Moment**: User scrolls to Materials section, sees:
> *"Not all wool is created equal. Our superfine Merino (18.5 micron) is sourced from ethically-raised sheep and processed using carbon-neutral methods."*

**Emotion**: Reflective pride — "I'm not just buying shoes, I'm making a statement about comfort, sustainability, and urban intelligence."

**Visual Reinforcement**:
- 3 columns: 32°C Optimized 🌡️ | Moisture-Wicking 💧 | Eco-Certified 🌿
- Large emoji icons (2rem) — visual anchors, quick scan
- Sage green accent (#8BA87A) — eco-trust signal

---

## 8. Storytelling Verification (PEAK Stage Checklist)

- [✅] **Narrative Arc**: Problem → Solution → Proof → Action (complete 4-act structure)
- [✅] **Tactile Cues**: Wool texture overlays, squishy buttons, warm color palette
- [✅] **Singapore Specificity**: MRT, 32°C, humidity data, park connectors
- [✅] **Emotional Journey**: Curiosity → Trust → Excitement → Anticipation
- [✅] **Anti-Generic**: No purple gradients, no bento grids, no "Buy Now" CTAs
- [✅] **Reflective Takeaway**: "I'm a tropical urbanite who chooses comfort + sustainability"

---

## 9. Design Decision Rationale

### 9.1 Why "Tactile Maximalism"?
- **Generic Problem**: AI designs feel flat, digital, disconnected from physical reality
- **Our Solution**: Wool texture overlays, squishy buttons → "This is a physical product you can feel"
- **Result**: Users remember the tactile experience, not just the product specs

### 9.2 Why Instrument Serif + Inter?
- **Luxury/Refined Strategy** (from 03-design-system.md)
- Instrument Serif (Display): Editorial luxury, "premium merino"
- Inter (Body): Highly legible at small sizes, modern sans-serif
- **Contrast + Harmony**: Different enough for hierarchy, similar enough for cohesion

### 9.3 Why Low-Saturation Warm Palette?
- **Reject "AI Slop"**: No bright purples, no neon accents, no glassmorphism
- **Embrace "Natural"**: Wool is earthy, warm, organic — palette reflects material
- **Urban Grit**: Foggy gray = Singapore's concrete jungle, humid haze

---

**Design Story Created**: 2026-05-07  
**Next Step**: Launch Phase5 VERIFY (accessibility audit, performance check)  
**Status**: PEAK stage complete — narrative framework established ✅
