```markdown
# Domain Pack Authoring Guide (Translation Engine v9.0)

## Purpose

Domain Packs extend the Translation Engine with register-specific terminology, modality markers, collocation pairs, and anti-translationese rules — without modifying the core prompt.

## When to Create a Custom Pack

Create a custom pack when:
- Your domain has specialized modality markers not covered by the four built-in packs (Engineering, Legal, Medical, Financial).
- Your organization has a proprietary terminology standard.
- You need entity overrides for domain-specific proper nouns.

Examples: patent prosecution, clinical trial protocols, crypto-assets regulation, aerospace engineering, pharmaceutical labeling.

## Pack Format

```
--- DOMAIN PACK: <name> (v9) ---
VERSION: <semver>
TRIGGER: <comma-separated keywords for auto-detection>

## MODALITY TABLE
| Source Term | Target Term | Direction | Note |
|---|---|---|---|
| <term> | <term> | EN→CN / CN→EN / BIDIR | <usage note> |

## COLLOCATION TABLE
| Source Phrase | Target Phrase | Direction | Note |
|---|---|---|---|
| <phrase> | <phrase> | EN→CN / CN→EN / BIDIR | <usage note> |

## ENTITY OVERRIDES (optional)
| Source Entity | Target Entity | Note |
|---|---|---|
| <entity> | <entity> | <context> |

## ANTI-TRANSLATIONESE PAIRS
| Wrong | Correct | Note |
|---|---|---|
| <wrong rendering> | <correct rendering> | <why> |

--- END DOMAIN PACK ---
```

## Rules

1. **Direction column is mandatory.** Use `EN→CN`, `CN→EN`, or `BIDIR`.
2. **Note column is mandatory.** Explain WHY this mapping is correct (e.g., "Never X because Y").
3. **Pack entries are adopted as `locked-context`** by default. To promote to `locked-standard`, add `[LOCKED-STANDARD]` to the Note column.
4. **Packs do NOT override:** the Four Axioms, the three Universal Modal Rules (§8.3), Quality Priorities (§12.2), or the Terminology Precedence Ladder (§12.3).
5. **Multiple packs:** If multiple packs are injected, later packs win on conflicts.
6. **TRIGGER keywords:** Used by the wrapper's `classify_domain()` heuristic. Include both English and Chinese keywords. Aim for 8–15 keywords.
7. **Size budget:** Keep each pack under 600 words. Larger packs cause attention dilution.

## Injection

- **Wrapper injection:** Append the pack content after §13 of the core prompt (semi-static cache zone).
- **User-message injection:** If no wrapper, paste the pack content at the head of the user message, before the source payload.
- **`--domain` flag:** `--domain=patent` tells the wrapper to inject `TE9_Pack_Patent.md`.

## Validation

After creating a pack, test with:
1. A representative source text in the target domain.
2. Verify modality markers are applied correctly (check Phase 5 Modality Check).
3. Verify collocations are used (check Phase 5 Collocation Check).
4. Verify no conflicts with built-in packs (if multiple packs active).

## Example: Patent Pack (Skeleton)

```
--- DOMAIN PACK: Patent (v9) ---
VERSION: 1.0
TRIGGER: patent, claims, prosecution, prior art, 专利, 权利要求, 现有技术

## MODALITY TABLE
| Source Term | Target Term | Direction | Note |
|---|---|---|---|
| comprises | 包括 | EN→CN | Open-ended; never 由……组成 (closed) |
| consisting of | 由……组成 | EN→CN | Closed-ended; never 包括 |
| wherein | 其中 | EN→CN | |
| 权利要求 | "claims" | CN→EN | Never "rights requirements" |
| 现有技术 | "prior art" | CN→EN | Never "existing technology" |

## COLLOCATION TABLE
| Source Phrase | Target Phrase | Direction | Note |
|---|---|---|---|
| file a patent application | 提交专利申请 | EN→CN | |
| prior art search | 现有技术检索 | EN→CN | |
| 侵权 | "infringement" | CN→EN | |

--- END DOMAIN PACK ---
```
```

---
