Audit Report — Big-Tech Research Skills Family (my-pi-agent)
Mode: C (Audit/Review — no code modified). Scope: all 17 files you named, plus directly-referenced dependencies I had to pull in to assess them honestly (postmortem-framework.md, which Skill 1's SKILL.md and bundled-resources table make load-bearing; the repo's own tests/test_repo_consistency.py, tests/test_fact_base_audit.py, tests/test_overflow_audit.py, tests/test_quant_helpers.py; .github/workflows/ci.yml; and a pre-existing docs/skills-audit/ report that the repo ships on the same three skills).

Verification ledger (what I actually did, not just read)
Check	Method	Result
fact_base_audit.py correctness	Ran --selftest; manually re-ran substring-evasion traps	Verified — exits 0, anchored matching holds (82.3 does not satisfy $282.32)
overflow_audit.mjs correctness	Installed Playwright+Chromium in a scratch dir, ran --selftest	Verified — exits 0, overflow flagged, bleed-marked element correctly skipped
quant_helpers.py correctness	Ran self-test	Verified — all worked-example figures reproduce, sign-regression guards hold
WCAG 2.2 AA contrast claims in report-design.md	Recomputed relative-luminance contrast for all 6 token pairs independently in Python	Verified exact match to the claimed ratios (15.55, 7.63, 5.80, 7.49, 5.69, 6.27, etc.)
Repo's own cross-skill consistency suite	python3 -m pytest tests/ -v	Verified — 66 passed, 1 skipped (Playwright not on root PATH at project scope)
ASC 280 segment claims in segment-maps.md (Nvidia, Amazon, Apple)	Web search against primary 10-K text	Verified accurate — matches filed 10-K language verbatim
Canonical "Alphabet Q3 2026, −12.29%" worked example used across all three skills	Web search for independent news corroboration	Verified as a real, reported event — GOOG EPS $2.12 vs $3.02 consensus, FCF −$9.07B, Search $63.4B vs ~$65B — all match multiple independent outlets (Yahoo Finance, GuruFocus, Schaeffer's, TimothySykes), with the expected cross-outlet variance (−10.9% to −12.7%) that the skills' own "record conflicts, don't silently pick" doctrine is designed to handle
Remediation commits cited in docs/skills-audit/README.md (H-1…H-4, M-2, M-6, P1/P2)	git fetch --unshallow; confirmed each hash exists; diffed the two highest-severity fixes	Verified real and substantive, not aspirational — H-4's anchoring fix and H-3's segment-map rewrite are present in the diffs I inspected
CI wiring claim	Read .github/workflows/ci.yml	Verified — runs pytest tests/ on every push/PR with Playwright provisioned
Summary verdict
This is an unusually rigorous skill family for an AI-agent "skills" repo — closer to a reviewed internal-tooling codebase than typical prompt-engineering content. It also ships its own prior Mode-C audit (docs/skills-audit/) with a rubric, 20 findings, and verifiable remediation commits, which I independently confirmed rather than took on faith. My own findings below are additive to that audit, not a re-statement of it.

Skill	Rigor (0–5)	Wall-St readiness	One-line verdict
1. analyzing-us-bigtech-stocks	4.3	Closest to IC-memo/model-governance standard	Only skill with executable, machine-verified controls (numeric audit + render audit, both proven to work); genuinely matches SR 11-7-style "the control is code, not a promise"
2. big-tech-earnings-postmortem	3.3	Sound doctrine, zero enforcement	Same analytical rigor as Skill 1 in prose, but ships no executable gate of its own — compliance depends entirely on the model's self-discipline, with no audit trail
3. bigtech-equity-research	3.6	Good quant discipline, narrower scope	Best of the three on quantitative correctness (signed waterfalls, OCF-shortfall math, ASC 280 segment fidelity) but its "audit" is a self-test on pure math, not on the actual deliverable
None of the three would pass an unconditional bulge-bracket research-controls review as a finished control framework (same conclusion the repo's own embedded audit reached), but Skill 1 is close, and all three are substantially above the bar for "AI agent skill markdown."

Findings
Critical: 0 — High: 1 — Medium: 3 — Low: 3 — Informational: 2

[H-1] Skills 2 and 3 have no executable enforcement of their own compliance gates

Location: big-tech-earnings-postmortem/SKILL.md §"Verification and delivery gates"; bigtech-equity-research/SKILL.md Definition-of-Done
Description: Skill 1 backs every hard rule (numeric traceability, no placeholders, WCAG, Assumed-on-method-page) with a script that fails closed and was proven to work (fact_base_audit.py, overflow_audit.mjs). Skills 2 and 3 state equally strict rules ("every figure sourced," "no fabrication," "WCAG-AA") but the only machinery is quant_helpers.py self-testing its own arithmetic — nothing checks that the delivered HTML note actually contains the sourced figures, has no placeholder text, or clears contrast/overflow. Skill 2 explicitly says it "ships no executable tooling of its own" and tells the agent to borrow Skill 1's script if installed — i.e., compliance is optional and environment-dependent.
Evidence: big-tech-earnings-postmortem/SKILL.md: "This skill ships no executable tooling of its own." bigtech-equity-research/SKILL.md Definition-of-Done only lists python3 scripts/quant_helpers.py self-test, which validates the worked example, not the actual report.
Impact: At an investment bank, a control that is "a described process the preparer is trusted to follow" rather than "a gate that fails the build" does not satisfy SR 11-7 / internal-audit model-risk expectations. An LLM operating under token/time pressure is exactly the actor these gates exist to constrain, and for 2 of 3 skills nothing stops a hallucinated figure or a missing disclaimer from shipping.
Severity: High
Recommended fix: Port fact_base_audit.py's placeholder-scan and --checks needle mode (it's already parameterized for an arbitrary checks.json, no fact-base required) into Skills 2 and 3 as a mandatory last step, or at minimum vendor a trimmed copy rather than an "if installed" dependency. This is explicitly flagged as open work in the repo's own remediation log (deferred items), so my finding corroborates rather than discovers it.
Confidence: Verified (ran the scripts; read the gating language in all three SKILL.md files).
[M-1] No root LICENSE file despite one skill declaring license: Apache-2.0

Location: repo root; big-tech-earnings-postmortem/SKILL.md frontmatter
Evidence: ls LICENSE* at repo root → no match. Only Skill 2's frontmatter carries a license: key; Skills 1 and 3 have none.
Impact: For a firm doing any kind of IP/compliance review before adopting third-party-authored skill content, an unresolved license claim with no actual license text is a blocker, and the inconsistency (1 of 3 skills licensed) suggests the family wasn't packaged as a single reviewed unit.
Severity: Medium
Recommended fix: Add a root LICENSE, and standardize license:/compatibility: frontmatter keys across all three SKILL.md files (same low-effort fix the repo's own audit already queued as "open convenience items").
Confidence: Verified.
[M-2] Skill 1's "Full pipeline" depends on a file not in your reviewed set but load-bearing

Location: analyzing-us-bigtech-stocks/SKILL.md Phase 4, Bundled Resources table, Adaptations section → references/postmortem-framework.md
Description: You listed 4 reference files for Skill 1; the actual folder also ships references/postmortem-framework.md, which Skill 1's own SKILL.md names as the authoritative source for its two-axis classification, and which Skill 2 explicitly defers to ("on divergence, the canonical copy wins"). Auditing the four files you named without this one would have missed that the "canonical doctrine" lives outside the set, and would have missed that a repo-level pytest suite exists specifically to police that cross-reference.
Impact: Not a defect in the skill — but it means any downstream consumer who copies only the four named files (as the install instructions literally say: "Copy this folder into your agent's skill directory" — which they would, since it's the whole folder) is fine; a consumer who cherry-picks files per a narrower file list is not.
Severity: Medium (documentation/packaging clarity, not a functional defect)
Recommended fix: None required functionally; if Skill 1 is ever distributed as individual files rather than the whole folder, call out postmortem-framework.md as non-optional in the "Bundled resources" table (it already is listed there — this is a note for whoever scoped your file list, not a skill defect).
Confidence: Verified.
[M-3] Skill 3's "signed waterfall" and Skill 1/2's "ordinal-only" doctrine are reconciled only by careful wording, and are easy to misuse under real-world pressure

Location: bigtech-equity-research/reference/formulas.md §"Root-cause driver decomposition"; scripts/quant_helpers.py::waterfall_check
Description: The methodology is honest about what it is (an arithmetic consistency check, explicitly not a regression or causal measurement), and the self-test includes real regression guards (sign-flip, unsigned-magnitude) that previously produced false "matches." That's good engineering. But the control that prevents misuse at delivery time — i.e., stopping an agent from publishing the waterfall chart without the "Reasoned allocation — not a measured decomposition" label — is prose in report-structure.md, not a check fact_base_audit.py-style tooling would enforce (because, per H-1, Skill 3 doesn't have page-level enforcement). FINRA 2241 and CFA Standard I(B) both specifically target exactly this failure mode (false precision presented as analysis).
Severity: Medium
Recommended fix: Same remediation as H-1 — a lightweight page-level placeholder/label scanner that fails if a waterfall chart appears without the literal required disclosure string.
Confidence: Reasoned (the math and docs are sound; the gap is enforcement, not doctrine).
[L-1] Minor doc duplication risk between Skill 1's postmortem-framework.md and Skill 2's standalone restatement

Location: both files
Description: This is a real, previously-identified risk (the repo's own tests/test_repo_consistency.py::TestPostmortemFrameworkFoldIn and TestSharedDatapoints exist specifically to guard it), and it currently passes. It remains structurally fragile: two human-maintained prose copies of one doctrine, guarded by regex-based tests rather than a single source of truth with an include/transclusion mechanism. The tests are necessary because the architecture allows drift, not because drift is impossible.
Severity: Low (currently compliant, structurally fragile)
Recommended fix: Low priority given the test coverage already in place; if the family grows a 4th variant, consider generating the standalone copy from the canonical file at build time instead of hand-mirroring.
Confidence: Verified (tests exist and pass; architecture is still two hand-maintained copies).
[L-2] overflow_audit.mjs and fact_base_audit.py are excellent but assume specific CLI invocation discipline with no wrapper/Makefile

Location: analyzing-us-bigtech-stocks/scripts/
Description: Both scripts are well-built (clear usage strings, --selftest, sane exit codes 0/1/2), but there's no single command (make audit, npm run audit) that runs both gates together before delivery — an agent under instruction-following pressure has two separate commands to remember to invoke in the right order, with different runtimes (python3 vs node) and different environment prerequisites (Playwright must be installed, which the skill correctly documents but cannot enforce).
Severity: Low
Recommended fix: A one-line scripts/audit_all.sh wrapping both, with a single combined exit code.
Confidence: Reasoned.
[L-3] Worked-example dates are a single real external event with no refresh mechanism

Location: all three skills' reference docs use the Oct 28–29, 2026 Alphabet print as the canonical teaching example
Description: I confirmed this is a real, correctly-cited event (not fabricated), which is a point in the skills' favor. But as the world moves past this date, the pedagogical value of a single hard-coded real event (rather than a clearly-synthetic one) will degrade, and a future maintainer might be tempted to "update" it with a new real event without re-running the full cross-skill reconciliation the current regression suite performs — reopening H-1/H-2/M-2 from the embedded audit.
Severity: Low
Recommended fix: None urgent; flag for the next doctrine refresh cycle.
Confidence: Verified the event is real; Reasoned on the future-maintenance risk.
[I-1] Compliance framing is unusually strong for this category of artifact
All three skills independently state: MNPI/Reg FD escalation discipline, "internal analytical pre-read, not sell-side research," explicit disclaimer of no Reg AC certification / no FINRA 2241 disclosure package, and "never fabricate / tag Unverifiable" discipline enforced at the taxonomy level. This is materially more careful than most AI-agent skill content and anticipates the exact objections a real compliance desk would raise. Confidence: Verified (read in full across all three; cross-checked by the repo's own TestDisclaimer test class, which passes).

[I-2] The repo's self-audit is itself a notable positive signal, with one caveat
Shipping a signed, reproducible, git-verifiable prior audit (with evidence scripts that still exit correctly against the current code) is good practice I don't often see. The caveat: the audit's own README.md states the verdict "none of the three passes a full bulge-bracket research-controls review as shipped" — my independent review reaches the same conclusion for different/additional reasons (H-1 above), so this isn't a stale or self-serving claim. Confidence: Verified.

Bottom line
If forced to green-light one of the three for an investment-committee-facing pilot today, it would be Skill 1, specifically because its controls are code that fails closed and I proved they do. Skills 2 and 3 have equally serious analytical doctrine (segment accuracy, signed-math discipline, confidence taxonomy) but currently rely on model self-discipline rather than an enforced gate for the actual deliverable — that is the one change that would move all three into genuinely audit-ready territory, and it's the single fix I'd prioritize (H-1) ahead of the smaller licensing/packaging items (M-1, M-2).
