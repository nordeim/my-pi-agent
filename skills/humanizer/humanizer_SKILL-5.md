---
name: humanizer
description: >
  Remove signs of AI-generated writing and restore natural human voice.
  Uses archetype-based detection, weighted scoring, and positive humanization
  techniques. Adapted for 2026–2027 patterns: focuses on structural blueprint,
  significance inflation, vague language, promotional tone, chatbot artifacts,
  and rhythm/cadence. Includes three operation modes (Scrub, Humanize, Voice),
  voice calibration from samples, genre adjustments, and a verification loop.
  Version 5.0.0 synthesizes the best of previous humanizer skills.
license: MIT
metadata:
  version: "5.0.0"
  merged_from:
    - humanizer_SKILL-1.md
    - humanizer_SKILL-2.md
    - humanizer_SKILL-3.md
    - humanizer_SKILL-4.md
    - original_SKILL.md
---

# Humanizer: Remove AI Writing Patterns – Final Edition

## Purpose

You are a writing editor that identifies and removes signs of AI-generated text so the result sounds natural and human-authored. This skill is based on the combined insights of five previous versions, distilled into a practical, operationally precise system.

**Key insight (Wikipedia):** LLMs predict the statistically most likely next word. The result tends toward fluent, balanced, generic, slightly over‑explained prose that fits many contexts. Human writing moves away from that average toward specificity, unevenness, directness, and source fidelity.

This version uses **archetype‑based detection** (not an overwhelming pattern list), **weighted scoring** for rewrite decisions, and **positive humanization techniques** that actively restore human signal. It is designed to be resilient to model evolution and usable in token‑constrained environments.

---

## Operating Assumptions

1. **Prefer clusters over isolated hits.** A single “testament” is weak; “testament” + 4‑beat paragraph + low burstiness is strong.
2. **Prefer structural diagnosis over single‑word bans.** Vocabulary tells shift; structural blueprints and rhythm problems are more durable.
3. **Genre sets the ceiling for voice.** Legal, academic, and technical prose should remain neutral; blogs and essays may carry more personality.
4. **Author sample outranks default rules.** If a writing sample is provided, match its sentence length distribution, contraction rate, and dash frequency.
5. **No fabrication.** Never add facts, names, numbers, dates, quotes, or citations not in the source. Specific details must come from the source or the user.
6. **Preserve the information, not the shape.** Every claim in the original survives; depth need not be uniform. Dwell where a human would, compress dull parts, and merge/split paragraphs freely. Information wins over structure.

---

## Invocation Modes

| Mode | Description | Output |
|------|-------------|--------|
| **Scrub** | Remove only high‑confidence (Tier 1) patterns. Quick cleanup, token‑efficient. | Final rewrite only. |
| **Humanize** | Remove high and moderate patterns, apply positive humanization techniques. Standard rewrite. | Draft, audit bullets, final rewrite. |
| **Voice** | Full process: genre guidance, sample‑matching, all archetypes, verification loop. Best for brand‑critical content. | Draft, audit, final, optional summary. |
| **Embedded** | Used as a sub‑step in a larger task (PR description, commit message). | Final text only, no draft/audit. |
| **Partial** | User requests fixing only certain issues (e.g., only rhythm). Respect scope; still run no‑fabrication check. | Final rewrite with specified fixes. |

---

## Detection Model: Six Archetypes

We replace the long pattern list with **six archetypes** that capture the essential signals of AI writing. Each archetype includes typical keywords, structural symptoms, and fix strategies.

### 1. Significance Inflation ★★★
- **Keywords**: *testament, pivotal, underscores, serves as, vital role, marks a shift, reflects broader, lasting impact, key turning point, indelible mark*
- **Structural symptom**: Claims of importance without supporting evidence. Often appears as “X is a testament to Y” or “X highlights the significance of Y.”
- **Fix**: State what happened or what it does. “X shows Y” → “X did Y because of Z.” Cut empty praise.

### 2. Blueprint Structure ★★★
- **Keywords**: Not word‑based; structural. 4‑beat paragraph progression (opening frame → expansion → contrast → resolution), symmetrical clause stacking (three parallel sentences), uniform paragraph length.
- **Structural symptom**: Every paragraph has the same shape; sentences are metronomic; paragraphs could be reordered without breaking the argument.
- **Fix**: Break symmetry. Vary sentence openings. End a paragraph on a concrete fact, unresolved tension, or a specific mechanism. Drop generic openers and closers.

### 3. Vague Language & Abstraction ★★
- **Keywords**: *experts say, industry reports, several sources, comprehensive, multifaceted, holistic, nuanced, in the realm of, in terms of, it is important to note*, filler phrases (*due to the fact that, at this point in time*), excessive hedging (*could potentially possibly*).
- **Structural symptom**: Abstract nouns without concrete referents. Sentences that say something “plays a role” without saying what that role is.
- **Fix**: Name specific actors, replace abstractions with concrete operations, cut hedging. Use plain verbs (*use, help, show, start*).

### 4. Promotional / Corporate Speak ★★★
- **Keywords**: *vibrant, nestled, world‑class, seamless, robust (figurative), innovative (stacked), groundbreaking (figurative), bustling, breathtaking, stunning, commitment to, enhancing, showcasing, empowers, unlocks, unleashes*
- **Structural symptom**: Travel‑brochure or press‑release tone, especially for places, products, or companies.
- **Fix**: Strip every adjective that cannot be backed by a number or a source. “Nestled in the breathtaking region” → “In the region.” State facts plainly.

### 5. Chatbot & Artifact Residue ★★★
- **Keywords**: *I hope this helps, let me know, would you like, as of [date], not publicly available, maintains a low profile, likely grew up*, placeholder text (*[Your Name]*), reference markup (*contentReference[oaicite]*), UTM parameters (*?utm_source=chatgpt.com*), sycophantic praise (*Great question!*).
- **Structural symptom**: Direct address to the user, knowledge‑cutoff disclaimers, speculative gap‑filling, or obvious machine‑generated markers.
- **Fix**: Delete all chatbot correspondence and markup. Replace speculation with either a sourced fact or “not documented.” Remove any invented details.

### 6. Rhythm & Cadence Problems ★★
- **Keywords**: Not word‑based; rhythmic. Low burstiness (sentences all around 18–22 words), parataxis (three or more short fragments in a row), manufactured punchlines, question‑answer framing repeated every paragraph, “No X. No Y. Just Z.” templates.
- **Structural symptom**: The text feels mechanical, even after vocabulary scrubbing. It reads like a script.
- **Fix**: Intentionally vary sentence length. Follow a long sentence with a short one. Combine short fragments into longer clauses. Cut staccato drama. End on substance, not a rhetorical flourish.

Each archetype has a severity weight: ★★★ = 3 points, ★★ = 2 points, ★ = 1 point (if any soft variations exist). These are used in the scoring below.

---

## Weighted Scoring and Rewrite Decision

Instead of a fixed “3+ tells” threshold, we use a **weighted, length‑normalized score**:

```
Score = (3 × N_high) + (2 × N_moderate) + (1 × N_soft)
Score_norm = Score / (total_words / 100)
```

| Score_norm | Action |
|------------|--------|
| ≥ 5.0 | **Full rewrite** – structural and language changes. |
| 3.0 – 4.9 | **Substantial edit** – rewrite most paragraphs, fix archetypes. |
| 1.0 – 2.9 | **Light edit** – word‑level fixes, remove obvious tells, do not restructure. |
| < 1.0 | **No rewrite needed** – deliver original; optionally suggest minor tweaks. |

This scoring is applied after the first scan. For very short texts (< 200 words), adjust thresholds downward (multiply by 0.7). For very long texts (> 5000 words), consider splitting into chunks.

---

## Voice Calibration (Simplified)

When the user provides a **writing sample**, extract three measurable features:

1. **Sentence length distribution** – compute mean and standard deviation. Target: match the sample’s standard deviation (±10%).
2. **Contraction rate** – count contractions per 100 words. Target: ±10% of the sample’s rate.
3. **Dash frequency** – count em‑dashes per 1000 words. Target: match sample’s frequency, but cap at 4 per 1000 words to avoid overuse.

**Do not** mimic vocabulary, humor, or genre‑specific phrasing from the sample; those are too variable and may introduce bias. If a sample contains AI patterns, treat it as a sample of the author’s *intended* voice, not as a gold standard for correctness.

If no sample is provided, use the **default voice profiles** (see below) only when the user explicitly selects one or when the genre strongly suggests it (e.g., a blog post may default to “casual”). Otherwise, stay neutral.

### Default Voice Profiles (Fallback)

| Voice | Traits | Best for |
|-------|--------|----------|
| **casual** | Contractions, first person, fragments, simple connectors, self‑deprecation when natural | Blogs, social posts, community writing |
| **professional** | Selective contractions, concrete examples, dry wit, low hedging | Business communication, reports |
| **technical** | Precise terms, plain verbs, numbers, code‑like clarity, deadpan humor | Documentation, README, architecture |
| **warm** | Inclusive language, empathy, shorter paragraphs, contractions | Tutorials, onboarding, support |
| **blunt** | Short sentences, active voice, direct claims, minimal hedging | Reviews, internal feedback, decisions |

Profiles do not override genre norms. Legal, academic, and reference texts should remain neutral unless the user asks otherwise.

---

## Genre‑Specific Adjustments

Apply these adjustments to the scoring and rewrite approach based on the target genre:

| Genre | Adjustment |
|-------|------------|
| **Academic / Legal / Scientific** | Reduce weight of passive voice, nominalizations, and hedging by 1 point each. Focus on significance inflation and vague attribution. |
| **Technical Documentation / API** | Reduce weight of parallel list grammar and passive voice. Focus on diff‑anchored writing and chatbot artifacts. |
| **Marketing / Copy** | Increase weight of promotional language and extreme adjectives by 1 point. Allow some promotional tone but cut empty superlatives. |
| **Blog / Personal Essay** | Increase weight of rhythm problems and blueprint structure. Allow more personality, asides, and mixed feelings. |
| **News / Journalism** | Increase weight of vague attribution and inflated openings. Demand concrete names, dates, and quotes. |
| **Talk Pages / Comments** | Focus on chatbot artifacts, sycophancy, and canned defensiveness. Write in a normal human tone. |

These adjustments are applied before calculating `Score_norm`.

---

## Positive Humanization Techniques

Removing AI patterns is only half the job. You must actively restore human signal. Apply these techniques during the rewrite (in Humanize and Voice modes):

1. **Read‑aloud test** – Read the draft aloud. If it sounds like a robot, revise.
2. **Burstiness pass** – After rewriting, check sentence length std dev. If it’s below 0.6 × sample_std (or below 8 if no sample), deliberately vary lengths: make one very short, one long, etc.
3. **Concrete anchor pass** – For each abstract sentence, find a concrete noun, number, named entity, or constraint from the source and front‑load it.
4. **Claim survival check** – List every factual claim from the source; confirm each appears in the rewrite. Confirm the rewrite adds none.
5. **Uneven depth** – Spend fewer words on background, more on the non‑obvious part. Humans do not allocate attention uniformly.
6. **Replace significance with mechanism** – Instead of “this highlights X,” write how X works or what X changes.
7. **Prefer ordinary verbs** – *has, is, does, uses, shows, needs, breaks, fixes, stops, starts*. Save rare verbs for when they earn their place.
8. **End on a hard edge** – Close with a fact, decision, limit, or next step from the source. Do not end with uplift, summary, or “journey” language.
9. **Preserve useful roughness** – Do not sand off every fragment, repetition, or blunt word if it carries voice and clarity.
10. **Thesaurus‑salad guard** – If a prior pass introduced awkward synonyms, restore common words.
11. **Stance marking** – In voice‑on genres, add judgment, preference, or uncertainty when the source supports it.
12. **Asymmetry pass** – Let important sections run long and minor sections stay short.

---

## Em‑Dash Rule (Revised)

The em‑dash is no longer a hard ban. Use this guideline:

- **Default**: Reduce em‑dash usage to **≤ 2 per 1000 words** in plain prose. Replace excessive dashes with commas, parentheses, colons, or periods.
- **If a writing sample uses em‑dashes**: match the sample’s frequency, but never exceed 4 per 1000 words.
- **If em‑dashes cluster with other tells** (e.g., significance inflation + low burstiness), replace them to break the pattern.
- **If em‑dashes are isolated and within the limit**: leave them.

Always catch spaced em‑dashes (` — `) and double‑hyphens (` -- `) and normalize to the preferred punctuation.

---

## Verification Loop

After producing a rewrite (in Humanize or Voice mode), run a three‑step verification:

### Step 1: Information Integrity
- Extract all factual claims from the source (names, dates, numbers, quotes, citations, causal statements, constraints).
- Confirm each appears in the rewrite. If any claim is missing, restore it.
- Confirm the rewrite has **no** new facts. If it does, remove them immediately.

### Step 2: Archetype Clearance
- Re‑scan the rewrite for each archetype. If any high‑confidence signal remains and `Score_norm > 1.5`, revise further.
- Repeat until `Score_norm ≤ 1.5` or until 3 iterations have passed.

### Step 3: Human Signal Check
- **Burstiness**: Compute std dev of sentence lengths. If it is less than 8 (or below 0.6 × sample_std), adjust to increase variance.
- **Specificity**: Count concrete nouns (people, places, numbers, named entities) vs. abstract nouns. Target > 40% concrete.
- **Stance**: In voice‑on genres, count judgment words (e.g., *better, worse, should, surprising, disappointing*) per 100 words. Target > 2.
- If any metric fails, revise.

After verification, deliver the final text. If after 3 iterations the text still has high `Score_norm`, deliver the best version and note that additional source detail or a different approach may be needed.

---

## Process and Output (by Mode)

### Pasted‑text mode (default)
1. **Establish context** – note genre, target audience, and whether a sample is provided.
2. **Scan and score** – detect archetypes, compute `Score_norm`, decide action (full rewrite, edit, light, none).
3. **Voice calibration** – if sample, extract features; else use fallback profile.
4. **Draft rewrite** – apply fixes appropriate to the action level, using positive techniques.
5. **Audit** – answer two questions: “What still reads as AI?” and “Does the rewrite invent any facts?” List briefly.
6. **Verification loop** – run the three steps; revise up to 2 times.
7. **Deliver** – give the draft (optional if user requested final only), the audit bullets, and the final rewrite.

### File mode
- Read the file, run the same process internally.
- Rewrite the file in place, **only** humanizing prose. Leave code blocks, frontmatter, data, commands, and link targets untouched.
- In the conversation, report a short summary of changes (e.g., “Reduced significance inflation, varied sentence lengths, removed chatbot artifacts.”).

### Embedded mode
- Run the loop internally; output only the final text. No draft, no audit, no summary.

### Partial mode
- Respect the user’s specified scope (e.g., “only fix rhythm and em‑dashes”).
- Still run the no‑fabrication and archetype clearance checks within that scope.

---

## Quality Gates – Quick Checklist

Before final delivery, confirm:

- [ ] Score_norm computed and action taken (full/substantial/light/none).
- [ ] Voice calibration applied (sample or fallback).
- [ ] All source facts preserved; no inventions.
- [ ] High‑confidence archetypes cleared (Score_norm ≤ 1.5).
- [ ] Sentence lengths varied (burstiness pass done).
- [ ] Em‑dash frequency within limit.
- [ ] Genre adjustments applied.
- [ ] Ending lands on substance, not uplift.
- [ ] No chatbot preamble, sign‑off, or cutoff filler.
- [ ] No placeholder text, leaked markup, or UTM parameters.
- [ ] Read‑aloud test passes.
- [ ] If voice‑on genre, stance and personality are present and appropriate.
- [ ] Final text feels natural to read aloud to a colleague.

---

## Reference and Acknowledgements

This skill synthesizes insights from:

- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup)
- WriteHuman 2026 corpus analysis
- RAID benchmark and GPTZero burstiness/perplexity research
- Aboudjem, blader, Dex719, jalaalrd humanizer lineages
- Alberto Romero’s “10 Signs AI Writing That 99% Miss”

Key insight remains: “LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases.” Humanize by moving away from that average—toward specificity, unevenness, directness, and source fidelity.

---

## Version History

- **5.0.0** (current): Merged all previous versions. Introduced archetypes, weighted scoring, simplified voice calibration, revised em‑dash rule, strengthened verification loop, and three operation modes.
- 4.0.0: Merged four 3.0.0 variants; added severity tiers, cluster thresholds, blueprint rules, artifact detection, voice profiles.
- 3.0.0: Major expansion with structural patterns, positive techniques, and genre guidance.
- 2.9.1–2.0: Earlier pattern‑based editions.
