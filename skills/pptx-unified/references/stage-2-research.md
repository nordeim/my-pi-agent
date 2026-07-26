# Stage 2: RESEARCH

> Gather facts and image assets in parallel. Never serialize what can be batched.

---

## Fact gathering

### From a repo (most common case)
Read these files IN PARALLEL (single turn, multiple Read calls):
- `README.md` — the project's self-description
- `package.json` — dependencies, scripts, project type
- Directory listings of key folders (`ls skills/`, `ls extensions/`, etc.)
- `CHANGELOG.md` or recent git log if version history matters
- Any existing catalog/index files (`skills-catalog.md`, `INVENTORY.txt`)

### From a product/website
- Use `web_search` to gather facts. Batch 2-3 queries in a single turn.
- Use `web-reader` to extract full content from the top 2-3 result URLs.
- Cross-reference claims across 2+ sources before quoting.

### From user-provided material
- Read the uploaded document(s) fully.
- Extract: key stats, feature list, audience signals, competitor comparisons, quotes.

---

## Image search (when photos are needed)

### The `z-ai image-search` CLI

```bash
z-ai image-search --query "<natural-language sentence>" --count 3
```

- The query MUST be a natural-language sentence, NOT keywords.
  - ✅ "A photograph of a modern minimalist home office with natural light"
  - ❌ "home office modern minimalist"
- The response contains `results[].original_url` (OSS-hosted, embeddable) and `results[].caption`.
- Print output goes to stdout — pick the best URL and bake it into the slide's `task_brief`.

### The 6-call hard limit

**HARD LIMIT: invoke the image-search CLI at most 6 times total across the whole deck trajectory.**

Plan image needs up front:
- Cover hero image (1 call)
- Section divider backgrounds (2-3 calls)
- Key content slide heroes (2-3 calls)
- Reuse URLs across multiple slides where possible.

If you hit the limit, do NOT attempt more searches — switch to photo-free design for remaining slides.

### When photos are NOT needed

**Photo-free decks are valid and often superior.** Linear-style dark decks rely on:
- Typography (massive numbers, tight tracking)
- Whitespace as structure
- Accent color for emphasis
- CSS grid backgrounds (subtle, decorative)
- Material Icons for visual variety

The my-pi-agent 12-slide reference build used **zero photos** by design. Don't force image searches when the visual reference doesn't call for them.

---

## Batching strategy

### Parallel-safe operations (emit in ONE turn)
- Multiple `Read` calls on different files
- Multiple `Bash` calls for `z-ai image-search` (up to 4 per turn)
- Multiple `web_search` calls (2-3 per turn)
- Mix of Read + Bash + web_search in the same turn

### Serial-only operations
- `web-reader` calls (each depends on a prior `web_search` result URL)
- Any operation whose input depends on a prior operation's output

**Rule of thumb:** if operation B doesn't need operation A's output, emit them in the same turn.

---

## Anti-patterns

### Anti-pattern: serial research calls
Never emit one `web_search` per turn. Batch 2-3 queries — they run concurrently and save 30-60 seconds of wall time.

### Anti-pattern: fabricating stats
If you can't verify a number, say so explicitly in the slide ("estimated", "as of last update", "not verified") rather than inventing one. Fabricated stats destroy credibility when the user fact-checks.

### Anti-pattern: forcing photos on every slide
Photo-free decks are valid. A Linear-style slide with a massive number + accent line is more impactful than the same slide with a stock photo behind it.

### Anti-pattern: ignoring the 6-call limit
The limit is real. If you hit it, switch to photo-free design — don't try to "borrow" URLs from other decks or fabricate them.

### Anti-pattern: keyword-style image queries
`z-ai image-search --query "office minimalist"` returns worse results than `z-ai image-search --query "A photograph of a modern minimalist home office with natural light"`. The ranking model is semantic — feed it sentences.

---

## Output of Stage 2

A mental (or scratchpad) list of:
- Verified facts to feature in the deck
- Image URLs (if any) with the slide they belong to
- Source citations for any external data

Proceed to Stage 3: PLAN.
