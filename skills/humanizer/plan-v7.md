# Meticulous Plan: Ultimate Merged Edition — `SKILL.md` v7.0.0

---

## 1. Design Philosophy & Lessons Incorporated

### 1.1 What v6.0.0 Got Right (Retain)
- The **6 Archetype** framework (conceptual, future-proof, resistant to model vocabulary shifts)
- The **Heuristic Triage Logic Gates** (replacing v5's broken `Score_norm` math)
- The **Verification Loop** (3-step: Information Integrity → Archetype Clearance → Human Signal Check)
- The **Diagnostic Scratchpad** (forced Chain of Thought before output)
- The **Operation Modes** (Scrub, Humanize, Voice, Embedded, Partial)
- The **Genre Matrix** concept

### 1.2 What v6.0.0 Got Wrong (Fix)
| Failure | Root Cause | v7.0.0 Fix |
|---|---|---|
| Hallucinated "fifty years" in fiction | Removed fiction exception from v3/v4 | **Restore explicit `<fiction_protocol>`** with permission for invented sensory/emotional detail within established world |
| Over-edited human clichés | No "cliché ≠ AI tell" rule | Add to "What NOT to flag": familiar metaphors in fiction are human signals |
| Ignored Gate 4 (Pass-Through) | Gate 4 enforcement too weak | **Hard constraint**: "If Gate 4 triggers, semantic edits are PROHIBITED. Typographic normalization only." |
| Positive Humanization Engine misapplied to fiction | No genre gate on concreteness demands | Add: "Concrete Anchor Pass, Friction Injection, Specificity Engine apply ONLY to non-fiction. In fiction, replaced by Voice Consistency Check." |
| No explicit fiction genre row | Genre matrix incomplete | Add dedicated row with distinct Do/Avoid columns |

### 1.3 What Previous Versions Contributed (Synthesize)
| Source | Contribution to v7.0.0 |
|---|---|
| **v1 (SKILL-1)** | Forensic artifact catalog (oaicite, grok-card, UTM params, ppl-ai-file-upload), era-tagged vocabulary (2023–2026) |
| **v2 (SKILL-2)** | Blueprint Problem philosophy, 4-beat paragraph, symmetrical clause stacking, metadiscourse/stance, burstiness/perplexity metrics |
| **v3 (SKILL-3)** | Positive Humanization Techniques (Pub test, read-aloud, first-paragraph cut, friction injection, treadmill effect, abstraction trap, subtext vacuum, Latinate bias) |
| **v4 (SKILL-4)** | Severity tiers (★★★/★★/★), cluster analysis thresholds, 48-pattern quick-reference table, domain-specific baselines, fiction genre exception |
| **v5 (SKILL-5)** | 6 Archetypes, weighted scoring concept (replaced by Logic Gates), simplified voice calibration (3 measurable features), revised em-dash rule (frequency cap), verification loop, operation modes |
| **v6 (my draft)** | Diagnostic scratchpad, XML structural boundaries, Heuristic Triage, Ironclad Final Checklist |

---

## 2. Document Architecture (Section-by-Section Outline)

The final document will be structured in **9 major sections**, ordered for optimal LLM attention (critical constraints at top AND bottom, operational detail in the middle).

### Section 1: YAML Frontmatter + Purpose + Key Insight
- Version: `7.0.0`
- `merged_from`: all previous versions
- Purpose statement (2 sentences)
- Key Insight (Wikipedia quote)
- Operating Assumptions (7 bullet points, condensed from v5)

### Section 2: `<prime_directives>` (Ironclad Rules)
Five non-negotiable rules, stated as absolute constraints:
1. **Preserve Information, Destroy Shape** (from v1–v5)
2. **Zero Fabrication** (with explicit fiction exception restored)
3. **Source-Bounded Friction** (new in v6, retained)
4. **Genre Ceilings** (from v3/v4/v5)
5. **Gate 4 Enforcement** (NEW: hard prohibition on semantic edits when text is clean)

### Section 3: `<diagnostic_scratchpad>` (Chain of Thought Requirement)
- XML-tagged scratchpad template
- Mandatory fields: Forensic Artifacts, Archetypes Triggered, Source Claims, Triage Decision, Genre Classification
- Must be completed BEFORE any rewrite begins

### Section 4: `<heuristic_triage>` (Logic Gates)
Four gates, replacing v5's math:
- **Gate 1: Forensic Tripwire** → Instant Scrub
- **Gate 2: Archetype Density (3+)** → Full Structural Rewrite
- **Gate 3: Surface Tells (1–2)** → Targeted Line-Edit
- **Gate 4: Clean** → Pass-Through (typographic normalization ONLY)

**Critical addition**: Explicit instruction that Gate 4 PROHIBITS semantic edits, creative upgrades, or "improvements" to human prose.

### Section 5: `<the_six_archetypes>` (Core Detection Engine)
Each archetype includes:
- Severity rating (★★★ / ★★ / ★)
- Keywords/Symptoms (nested from v1/v4 granular lists)
- Structural symptom description
- Fix strategy
- **Genre exceptions** (where applicable)

The six archetypes:
1. **Significance Inflation** ★★★
2. **Structural Blueprint** ★★★
3. **Vague Abstraction** ★★
4. **Promotional / Corporate Slop** ★★★
5. **Chatbot & Artifact Residue** ★★★ (with full forensic catalog from v1)
6. **Rhythm & Cadence** ★★

### Section 6: `<fiction_protocol>` (NEW — Critical Addition)
This section did not exist in v6 and caused the hallucination failure. It will include:
- **Permission structure**: Invented sensory, emotional, and micro-detail is permitted within the established world
- **Prohibition**: Do not invent plot facts, character names, or events that contradict the source
- **Cliché protection**: Familiar metaphors, well-worn similes, and conventional emotional language in fiction are HUMAN signals, not AI tells. Do NOT "upgrade" them.
- **Gate override**: In fiction, Gate 4 means "deliver unchanged except typographic normalization." The Positive Humanization Engine's concreteness demands do NOT apply.
- **Verification adjustment**: Step 1 (Claim Survival) checks for plot consistency and character continuity, not factual non-invention.
- **Voice priority**: In fiction, the author's voice, cadence, and metaphorical choices outrank all style rules.

### Section 7: `<positive_humanization_engine>` (From v3, Genre-Gated)
Techniques (each with explicit genre applicability):
1. Read-Aloud Test (all genres)
2. Pub Test / Desk Test (non-fiction)
3. First-Paragraph Cut (non-fiction, journalism)
4. Burstiness Pass (all genres, but DO NOT apply to fiction with already-high burstiness)
5. Concrete Anchor Pass (non-fiction ONLY)
6. Friction Injection (non-fiction ONLY, source-bounded)
7. Claim Survival Check (all genres, with fiction-adjusted criteria)
8. Uneven Depth (non-fiction)
9. Replace Significance with Mechanism (non-fiction)
10. Prefer Ordinary Verbs (all genres)
11. End on a Hard Edge (non-fiction; fiction ends on narrative beat)
12. Preserve Useful Roughness (all genres — CRITICAL)
13. Thesaurus-Salad Guard (all genres)
14. Stance Marking (voice-on genres only)
15. Asymmetry Pass (non-fiction)
16. Metadiscourse Pass (voice-on genres only)

### Section 8: `<voice_calibration>` + `<genre_matrix>` + `<operation_modes>`
- **Voice Calibration**: Sample matching (sentence length std dev, contraction rate, dash frequency) from v5
- **Default Voice Profiles**: 5 profiles (casual, professional, technical, warm, blunt) from v4/v5
- **Genre Matrix**: 10 rows including the critical **Fiction / Narrative** row:

| Genre | Aim | Do | Avoid |
|---|---|---|---|
| Fiction / Narrative | Voice, scene, emotional truth | Invented sensory/emotional detail within world; preserve author's metaphors; protect clichés as human signal | Applying non-fiction no-fabrication rule; "upgrading" familiar metaphors; injecting concreteness demands; over-editing at Gate 4 |

- **Operation Modes**: Scrub, Humanize, Voice, Embedded, Partial (from v5/v6)

### Section 9: `<verification_loop>` + `<quality_gates>` + `<ironclad_final_checklist>`
- **Verification Loop** (3 steps, with fiction-adjusted Step 1)
- **Quality Gates** (15-item checklist from v4/v5)
- **Ironclad Final Checklist** (repeated at bottom for recency bias anchoring)

---

## 3. Conflict Resolution Matrix

| Conflict | Resolution in v7.0.0 |
|---|---|
| **Zero Fabrication vs. Fiction** | Explicit `<fiction_protocol>` grants permission for sensory/emotional micro-detail. Plot facts remain protected. |
| **Concrete Anchor Pass vs. Fiction** | Genre-gated: Concrete Anchor Pass applies ONLY to non-fiction. In fiction, replaced by Voice Consistency Check. |
| **Em-dash hard ban (v1–v4) vs. frequency cap (v5)** | v5's frequency cap wins: ≤ 2 per 1000 words default, ≤ 4 with sample override. Clustering with other archetypes triggers removal. |
| **Score_norm math (v5) vs. LLM arithmetic limits** | Replaced by Heuristic Triage Logic Gates (categorical, not numerical). |
| **60-pattern list (v1) vs. 6 archetypes (v5)** | Archetypes are the cognitive framework. Granular patterns are nested as "symptoms" under each archetype. |
| **"Do not over-edit" vs. "Fix all tells"** | Gate system resolves: Gate 4 = no semantic edits. Gate 3 = targeted fixes only. Gate 2 = full rewrite. |
| **Cliché as AI tell vs. cliché as human signal** | Context-dependent: In non-fiction, clichés may signal AI padding. In fiction/narrative, clichés are human signals and MUST be preserved. |
| **Burstiness injection vs. already-bursty fiction** | If source already has high burstiness (std dev > 12), DO NOT inject additional variation. Preserve existing rhythm. |

---

## 4. Prompt Engineering Optimizations

### 4.1 Attention Management
- **Prime Directives** at the very top (first thing the LLM reads)
- **Ironclad Final Checklist** at the very bottom (recency bias anchor)
- **XML-style tags** (`<prime_directives>`, `<the_six_archetypes>`, `<fiction_protocol>`, etc.) to create parseable cognitive boundaries
- **Tables** for dense pattern matching (faster LLM scanning than prose)

### 4.2 Chain of Thought Enforcement
- The `<diagnostic_scratchpad>` is MANDATORY before any output
- The scratchpad must explicitly state the Gate decision
- If Gate 4, the scratchpad must state: "No semantic edits permitted"

### 4.3 Token Efficiency
- Target: < 4,000 tokens for the complete document
- Use compressed tables instead of verbose explanations
- Nest granular patterns as bullet points under archetypes (not standalone sections)
- Remove redundant examples (keep 1 Before/After per archetype max)

### 4.4 Anti-Hallucination Safeguards
- The Verification Loop's Step 1 explicitly asks: "Did I invent any number, name, date, or event not in the source?"
- In fiction mode, Step 1 asks: "Did I contradict any established plot fact, character name, or event?"
- The Ironclad Final Checklist repeats: "I have not invented facts" AND "In fiction, I have not contradicted the source world"

---

## 5. Structural Additions Not Present in Any Previous Version

| Addition | Rationale |
|---|---|
| **`<fiction_protocol>`** as a standalone section | v6 failure proved fiction needs its own permission structure |
| **Gate 4 hard prohibition language** | "Semantic edits are PROHIBITED at Gate 4" — not just "light polish" |
| **Cliché Protection Rule** | Explicitly states familiar metaphors in fiction are human signals |
| **Burstiness Preservation Rule** | If source already has high burstiness, do NOT inject more |
| **Genre-Gated Positive Techniques** | Each technique explicitly marked with applicable genres |
| **Forensic Tripwire as Gate 1** | Elevates artifact detection to highest priority (before archetype analysis) |
| **Diagnostic Scratchpad with Genre Field** | Forces the LLM to classify genre BEFORE applying rules |

---

## 6. Execution Roadmap

| Step | Action | Dependencies |
|---|---|---|
| 1 | Draft YAML frontmatter + Purpose + Key Insight + Operating Assumptions | None |
| 2 | Draft `<prime_directives>` with fiction exception restored | Step 1 |
| 3 | Draft `<diagnostic_scratchpad>` template | Step 2 |
| 4 | Draft `<heuristic_triage>` with 4 Logic Gates + Gate 4 hard prohibition | Step 2 |
| 5 | Draft `<the_six_archetypes>` with nested symptoms from v1/v4 | Steps 2, 4 |
| 6 | Draft `<fiction_protocol>` (NEW) | Steps 2, 5 |
| 7 | Draft `<positive_humanization_engine>` with genre gates | Steps 5, 6 |
| 8 | Draft `<voice_calibration>` + `<genre_matrix>` + `<operation_modes>` | Steps 5, 6, 7 |
| 9 | Draft `<verification_loop>` + `<quality_gates>` | Steps 2–8 |
| 10 | Draft `<ironclad_final_checklist>` (bottom anchor) | Step 9 |
| 11 | Full review: token count, redundancy check, conflict scan | Steps 1–10 |
| 12 | Test against edge cases: fiction passage, technical doc, raw ChatGPT output with artifacts | Step 11 |

---

## 7. Success Criteria

The final v7.0.0 document will be considered complete when:

- [ ] All 6 archetypes are defined with nested symptoms
- [ ] The fiction protocol is explicit and unambiguous
- [ ] Gate 4 has hard prohibition language
- [ ] No mathematical scoring is required (LLM-safe)
- [ ] The forensic artifact catalog from v1 is preserved under Archetype 5
- [ ] The Positive Humanization Engine is genre-gated
- [ ] The em-dash rule is frequency-based, not a hard ban
- [ ] The Verification Loop has fiction-adjusted Step 1
- [ ] The document is < 4,000 tokens
- [ ] Prime Directives appear at top; Ironclad Checklist at bottom
- [ ] The document passes the "fiction test": when applied to the `original-text.md` Christmas story, it should trigger Gate 4 and deliver the text unchanged (except curly → straight quote normalization)
- [ ] The document passes the "artifact test": when applied to raw ChatGPT output with `oaicite` tags, it should trigger Gate 1 and strip them
- [ ] The document passes the "corporate slop test": when applied to "vibrant tapestry nestled in breathtaking landscape" prose, it should trigger Gate 2 and perform full structural rewrite

---

## 8. Ready for Execution

This plan is complete. Upon your confirmation, I will proceed to generate the full `SKILL.md` v7.0.0 document following this architecture exactly.

**Shall I proceed with generating the complete document?**
