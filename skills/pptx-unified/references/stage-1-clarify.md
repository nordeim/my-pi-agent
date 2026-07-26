# Stage 1: CLARIFY

> Collect 6 mandatory inputs before writing any code. Skipping this stage is the #1 cause of full-deck re-renders.

---

## When to skip `AskUserQuestion`

If the user has explicitly said any of:
- "no need to ask for my approvals"
- "proceed with your best recommendations"
- "just do it"
- "skip questions"

→ Skip the `AskUserQuestion` call and apply the **recommended defaults** (below). Document the chosen defaults in `slides_brief.json.design` so downstream sub-agents have a single source of truth.

Otherwise, batch all 6 questions in a SINGLE `AskUserQuestion` call (max 6 questions per call).

---

## The 6 mandatory dimensions

### 1. Audience

**Why it matters:** Determines tone, density, and which features to highlight.

**Options to offer (adapt to the source material):**
- "Power users of <product>" — existing users who want to discover capabilities
- "Developers / engineers" — technical audience evaluating for fork/adoption
- "Open-source community" — GitHub visitors making a star/fork decision in 60 seconds
- "Internal team" — reference index for "which skill/tool to use when"

**Recommended default:** infer from the source material. A repo README → "developers/power users".

### 2. Deck length

**Why it matters:** 8 (lightning) / 12 (standard marketing) / 16+ (comprehensive reference) are completely different artifacts.

**Options:**
- **8 slides** — Cover + Hook + 3 highlights + 3 deep-dives + CTA. For a 5-minute lightning talk.
- **12 slides** — Cover + Hook + Bento + Map + Section Divider + 3 deep-dives + Beyond + Timeline + Setup + CTA. The marketing sweet spot. **(Recommended default)**
- **16 slides** — Cover + 2 section dividers + 12 content + CTA. Adds per-category breakdown + comparison matrix.
- **20+ slides** — Comprehensive reference with one slide per category + variant comparisons + setup + contributing guide.

### 3. Palette (bg + primary + accent as a trio)

**Why it matters:** One coherent trio, not 3 independent color choices.

**Load `palette-presets.md` for 8 curated palettes.** The default recommendation:

- **GitHub Dark:** `#0D1117` / `#E6EDF3` / `#58A6FF` — matches most dev-tool repos, feels native to developers

Offer palette options that are TUNED to the source material. A finance deck and a children's-book pitch should NEVER see the same 3 palette options.

### 4. Typography (heading + body + numeric pairing)

**Why it matters:** Font choice signals voice. Inter = modern SaaS. Playfair = editorial. Geist = Vercel-native.

**Load `typography-pairings.md` for 6 curated pairings.** The default recommendation:

- **Inter + JetBrains Mono:** Inter for headings/body, JetBrains Mono for numbers/code/labels. Clean, modern, developer-native.

### 5. Visual reference

**Why it matters:** A named style anchor gives the sub-agents a shared visual target.

**Options:**
- **Linear changelog** — dark, generous whitespace, big stats, accent-color highlights, monospace numerics. **(Recommended default for dev-tool decks)**
- **Vercel keynote** — ultra-minimal, one idea per slide, huge typography, subtle gradients
- **Stripe Press** — editorial, serif headlines, restrained accent color, print-quality feel
- **GitHub Universe** — brand-forward, octicon-style icons, dark with purple/blue accents

### 6. Speaker notes

**Why it matters:** Determines whether the deck is self-explanatory or needs a presenter.

**Options:**
- **None** — slides are self-explanatory marketing material
- **Short (3-5 bullet hints)** — enough to guide a presenter without reading verbatim **(Recommended default)**
- **Full (~80-150 word script)** — ready to read aloud for a recorded walkthrough

---

## The `AskUserQuestion` call structure

If you are asking (not skipping), batch all 6 questions in ONE call:

```
AskUserQuestion(questions=[
  {header: "Audience", question: "...", type: "single", options: [...]},
  {header: "Length", question: "...", type: "single", options: [...]},
  {header: "Palette", question: "...", type: "single", options: [...]},
  {header: "Typography", question: "...", type: "single", options: [...]},
  {header: "Style ref", question: "...", type: "single", options: [...]},
  {header: "Notes", question: "...", type: "single", options: [...]}
])
```

**Rules:**
- Each question: short `header` (≤12 chars), the `question` itself, 3-4 `options` (each with `label` + concrete `description`).
- Mark exactly ONE option per question as `recommended: true` — the default you'd pick if the user didn't answer.
- Each option's `description` MUST be concrete (a palette hint, a font name, a sample headline). Vague descriptions like "formal" / "casual" are forbidden.
- Do NOT call any other tool in the same turn as `AskUserQuestion`.

---

## Anti-patterns

### Anti-pattern: skipping clarify "because the request is clear"
Even when the user says "make a deck about X", you still need to confirm audience + length + palette. A 20-slide comprehensive reference deck and an 8-slide lightning talk are completely different artifacts.

### Anti-pattern: asking 1 question per turn
Drip-asking across 6 turns wastes 5 turns. Batch all 6 in one `AskUserQuestion` call.

### Anti-pattern: vague option descriptions
"Light / Dark / Other" is a failure mode. Each option must name a concrete palette, font, or style reference so the user can react to something specific.

### Anti-pattern: marking multiple options as `recommended`
Exactly ONE option per question gets `recommended: true`. Marking 2+ defeats the purpose — the recommendation exists to provide a default if the user doesn't answer.

---

## Output of Stage 1

A `design` block (mental or written) that will become the `slides_brief.json.design` field in Stage 3:

```json
{
  "title": "(deck title)",
  "style_name": "Linear Changelog Dark",
  "palette": {"background": "#0D1117", "primary": "#E6EDF3", "accent": "#58A6FF"},
  "typography": {"heading": "Inter", "body": "Inter", "numeric": "JetBrains Mono"},
  "reference": "Linear.app changelog pages"
}
```

Plus the `language` and `speaker_notes` fields for the top-level brief.

Proceed to Stage 2: RESEARCH.
