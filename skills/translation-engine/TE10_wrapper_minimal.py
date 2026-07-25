```python
#!/usr/bin/env python3
"""
Translation Engine v10.1 — Minimal Wrapper
Implements: scratchpad stripping (§3.2), mode-flag injection (§3.4),
few-shot injection (§3.5), domain pack injection (§14.4),
domain pre-classification (§14.4 two-stage protocol),
size-aware Draft-Lock tier signaling (§4.7), and payload
segmentation at section/paragraph boundaries for oversized inputs.

Usage:
    python TE10_wrapper_minimal.py --domain=engineering --scratchpad=full < input.md > output.md

Requires: openai>=1.0 (or any OpenAI-compatible SDK)
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CORE_PROMPT_FILE = "Translation_Engine_v10_Prompt.md"
FEWSHOTS_FILE = "TE10_FewShots.md"
PACK_DIR = "."  # directory containing TE10_Pack_*.md

PACK_FILES = {
    "engineering": "TE10_Pack_Engineering.md",
    "legal": "TE10_Pack_Legal.md",
    "medical": "TE10_Pack_Medical.md",
    "financial": "TE10_Pack_Financial.md",
    "academic": "TE10_Pack_Academic.md",
}

# Domain keyword heuristic (§14.4 Stage 1)
DOMAIN_KEYWORDS = {
    "legal": [
        "合同", "诉讼", "条款", "仲裁", "违约", "管辖",
        "contract", "liability", "indemnify", "jurisdiction",
        "arbitration", "lawsuit", "plaintiff", "defendant",
    ],
    "medical": [
        "患者", "临床", "剂量", "禁忌", "不良反应", "预后",
        "patient", "dosage", "contraindicated", "adverse event",
        "clinical trial", "prognosis", "symptom",
    ],
    "financial": [
        "营收", "披露", "每股收益", "前瞻性", "净利润", "毛利率",
        "revenue", "EPS", "forward-looking", "material adverse",
        "non-GAAP", "earnings", "guidance",
    ],
    "engineering": [
        "API", "部署", "框架", "协议", "端点", "延迟", "吞吐",
        "deploy", "framework", "RFC", "endpoint", "latency",
        "throughput", "microservice", "kubernetes", "docker",
    ],
    "academic": [
        "论文", "引用", "审稿", "他引", "自引", "组会", "预印本",
        "影响因子", "同行评审", "文献综述", "消融实验",
        "paper", "citation", "peer review", "manuscript", "journal",
        "preprint", "impact factor", "bibliometric", "ablation",
        "literature review", "state of the art",
    ],
}


# ---------------------------------------------------------------------------
# Domain Pre-Classification (§14.4 Stage 1)
# ---------------------------------------------------------------------------
def classify_domain(payload_head: str, explicit_domain: str | None = None) -> str:
    """Classify domain from first 300 chars of payload.
    If explicit_domain is provided and valid, use it directly.
    """
    if explicit_domain and explicit_domain in PACK_FILES:
        return explicit_domain
    if explicit_domain == "general":
        return "general"

    head = payload_head[:300].lower()
    scores = {
        domain: sum(1 for kw in keywords if kw.lower() in head)
        for domain, keywords in DOMAIN_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)  # type: ignore[arg-type]
    # Specific domain beats generic engineering fallback:
    # when academic and engineering both score >= 2, prefer academic.
    if scores["academic"] >= 2 and scores["engineering"] >= 2:
        return "academic"
    return best if scores[best] >= 2 else "engineering"  # default


# ---------------------------------------------------------------------------
# Token Estimation & Size Thresholds (§4.7) — CJK-aware
# ---------------------------------------------------------------------------
SEGMENT_WORD_THRESHOLD = 800  # Segmented Draft-Lock threshold (effective words)


def _is_cjk_ideograph(ch: str) -> bool:
    """True if ch is a CJK ideograph (a word-bearing character).
    Covers the Unified Ideographs plus the Extension A, Compatibility,
    and Extension B+ ranges. Full-width CJK punctuation (U+FF00–U+FFEF)
    is intentionally excluded — it is punctuation, not a word unit, so
    counting it would over-count effective words.
    """
    o = ord(ch)
    return (
        0x4E00 <= o <= 0x9FFF      # CJK Unified Ideographs
        or 0x3400 <= o <= 0x4DBF   # CJK Unified Ideographs Extension A
        or 0xF900 <= o <= 0xFAFF   # CJK Compatibility Ideographs
        or 0x20000 <= o <= 0x2A6DF  # CJK Unified Ideographs Extension B+ (B/C/D/E)
    )


def count_effective_words(payload: str) -> int:
    """Count 'words' for the segmentation threshold, accounting for CJK.
    Unspaced CJK text is undercounted by str.split(), so each CJK ideograph
    is weighted ~0.6 'words' (one char roughly carries one word of meaning).
    Full-width CJK punctuation is not counted (see _is_cjk_ideograph).
    """
    cjk_chars = sum(1 for c in payload if _is_cjk_ideograph(c))
    latin_words = len(re.findall(r"[a-zA-Z][a-zA-Z0-9'-]*", payload))
    return int(cjk_chars * 0.6 + latin_words)


def estimate_tokens(payload: str) -> int:
    """Estimate token count accounting for CJK characters.
    CJK ideographs: ~1.5 tokens/char; Latin: ~1.3 tokens/word; inline
    code span: ~0.5 tokens/pair. Full-width punctuation excluded.
    """
    cjk_chars = sum(1 for c in payload if _is_cjk_ideograph(c))
    latin_words = len(re.findall(r"[a-zA-Z][a-zA-Z0-9'-]*", payload))
    inline_code = len(re.findall(r"`[^`]+`", payload))
    return int(cjk_chars * 1.5 + latin_words * 1.3 + inline_code * 0.5)


def should_segment(payload: str) -> bool:
    """Determine if payload should be segmented for Draft-Lock (§4.7)."""
    return count_effective_words(payload) > SEGMENT_WORD_THRESHOLD


def segment_payload(payload: str, max_words: int = SEGMENT_WORD_THRESHOLD) -> list[str]:
    """Segment payload at section/paragraph/sentence boundaries for Draft-Lock.
    Three-pass progressive fallback:
      Pass 1: H1/H2 headings and horizontal rules (---)  — preserves structure
      Pass 2: Paragraph boundaries (blank lines)           — preserves prose
      Pass 3: Sentence boundaries (。！？.!?)              — last resort, grammar intact
    Returns at least [payload] (a single sentence longer than max_words stays
    oversized rather than being split mid-sentence).
    """
    if count_effective_words(payload) <= max_words:
        return [payload]

    def _pack(parts: list[str]) -> list[str]:
        segments: list[str] = []
        current = ""
        for part in parts:
            if current and count_effective_words(current + part) > max_words:
                segments.append(current.strip())
                current = part
            else:
                current += part
        if current.strip():
            segments.append(current.strip())
        return segments or [payload.strip()]

    # Pass 1: split at H1/H2 headings and horizontal rules
    parts = re.split(r"\n(?=#{1,2}\s)|\n(?=---\s*\n)", payload)
    segments = _pack(parts)
    if len(segments) > 1:
        return segments

    # Pass 2 (fallback): split at paragraph (blank-line) boundaries
    parts = re.split(r"\n\s*\n", payload)
    segments = _pack(parts)
    if len(segments) > 1:
        return segments

    # Pass 3 (last resort): a single oversized segment with no section/
    # paragraph boundaries. Split at sentence boundaries (Sino-Tibetan and
    # Latin sentence-final punctuation). Cannot split below the sentence — a
    # single sentence longer than max_words stays oversized (grammar intact).
    if count_effective_words(segments[0]) > max_words:
        sentences = re.split(r"(?<=[\u3002\uFF01\uFF1F.!?])\s*", segments[0])
        sentence_segments = _pack([s for s in sentences if s.strip()])
        if len(sentence_segments) > 1:
            return sentence_segments
    return segments


# ---------------------------------------------------------------------------
# File Loading
# ---------------------------------------------------------------------------
def load_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        print(f"[WARNING] File not found: {path}", file=sys.stderr)
        return ""
    return p.read_text(encoding="utf-8")


def load_domain_pack(domain: str) -> str:
    if domain == "general" or domain not in PACK_FILES:
        return ""
    return load_file(os.path.join(PACK_DIR, PACK_FILES[domain]))


# ---------------------------------------------------------------------------
# Few-Shot Selection (§3.5)
# ---------------------------------------------------------------------------
def select_fewshots(domain: str, count: int = 3) -> list[int]:
    """Return the selected few-shot example indices for a domain.
    Indices refer to numbered `## Example N:` blocks in FEWSHOTS_FILE.
    """
    selection = {
        "legal": [1, 4, 5, 8],
        "medical": [1, 4, 5, 8],
        "financial": [1, 4, 5, 8],
        "engineering": [2, 3, 6, 9],
        "academic": [1, 4, 7, 10],
        "general": [1, 3, 5, 8],
    }
    indices = selection.get(domain, selection["general"])[:count]
    return indices


def parse_fewshot_examples(content: str) -> dict[int, dict[str, str]]:
    """Parse FEWSHOTS_FILE content into {N: {"user": ..., "assistant": ...}}.

    The few-shots file format is externally controlled, so this parser is
    label-tolerant: it accepts both plain and bold-Markdown labels and
    content that begins on the same line as the label or on the next line.

    Recognized block shapes (header `## Example N:` is fixed):
        ## Example N: ...title...
        user:                 (or **User:**, case-insensitive, bold-or-plain)
        <source>
        assistant:            (or **Assistant:**)
        <target>
    The next `## Example` header (or a stand-alone `---` rule) closes the
    block. Returns {} for empty/unrecognized content (callers degrade to []).
    """
    examples: dict[int, dict[str, str]] = {}
    pattern = re.compile(
        r"^##\s*Example\s+(\d+):.*?$(.*?)(?=^##\s*Example\s+\d+:|^---\s*$|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        body = m.group(2).strip()
        user_text = _extract_label_block(body, "user")
        assistant_text = _extract_label_block(body, "assistant")
        if user_text and assistant_text:
            examples[idx] = {"user": user_text, "assistant": assistant_text}
    return examples


# A few-shot directive line: an optional leading indent, up to two stars,
# the word 'user' or 'assistant', then a colon/colon+stars in any common
# order. Recognizes user:/User:/**User:**/assistant:/**Assistant:** and
# tolerates surrounding Markdown bold and optional trailing colons/stars.
# Shared by both the label matcher and the lookahead terminator BELOW so the
# two cannot drift out of sync.
_DIRECTIVE_LINE = r"^[ \t]{0,3}\*{0,2}(?:user|assistant)[:*]{0,4}\*{0,2}"


def _extract_label_block(
    body: str, label: str, terminator: str | None = None
) -> str:
    """Extract content following a labelled directive within a few-shot body.

    Matches a line-anchored `label:` / `Label:` / `**Label:**` directive
    (case-insensitive, optional Markdown bold), then captures whatever follows
    — on the same line after the label and/or on subsequent lines — until a
    terminator (the next `user`/`assistant`/`**User:**`/`**Assistant:**`
    directive, or block end). Returns "" when the label is absent.
    """
    if terminator is None:
        terminator = r"(?=" + _DIRECTIVE_LINE + r"|\Z)"
    # Match this specific label line; group(2) is everything after it (same +
    # following lines, DOTALL spans newlines).
    label_pat = re.compile(
        rf"(?im)^[ \t]{{0,3}}\*{{0,2}}{label}[:*]{{0,4}}\*{{0,2}}:?\s*(.*)",
        re.DOTALL,
    )
    m = label_pat.search(body)
    if not m:
        return ""
    rest = m.group(1)
    rest = re.sub(r"^\s*\n", "", rest)  # drop a single leading blank line
    stop = re.search(terminator, rest, re.DOTALL | re.MULTILINE | re.IGNORECASE)
    captured = rest[: stop.start()] if stop else rest
    return captured.strip()


def load_fewshot_messages(domain: str, count: int = 3) -> list[dict]:
    """Load and inject selected few-shot examples as prior conversation turns.
    Returns a list of {'role': 'user'/'assistant', 'content': str} pairs ready
    to extend the OpenAI messages list. Returns [] when the few-shots file is
    absent or when selected examples are not present in the file.
    """
    content = load_file(FEWSHOTS_FILE)
    if not content:
        return []
    examples = parse_fewshot_examples(content)
    if not examples:
        return []
    messages: list[dict] = []
    for idx in select_fewshots(domain, count):
        ex = examples.get(idx)
        if ex:
            messages.append({"role": "user", "content": ex["user"]})
            messages.append({"role": "assistant", "content": ex["assistant"]})
    return messages


# ---------------------------------------------------------------------------
# Mode-Flag Rule Injection (§3.4)
# ---------------------------------------------------------------------------
MODE_RULES = {
    "--scratchpad=light": "Use a light scratchpad: concise reasoning only; no verbose commentary.",
    "--scratchpad=none": "Omit the <engine_logs> scratchpad entirely; emit the translated payload directly.",
}


def inject_mode_rules(mode_flags: list[str]) -> str:
    """Return newline-joined mode-specific rules for flags actually present.
    Flags not listed in MODE_RULES are silently ignored (no speculative rules).
    """
    rules = [MODE_RULES[f] for f in mode_flags if f in MODE_RULES]
    return "\n".join(rules)


# ---------------------------------------------------------------------------
# Scratchpad Stripping (§3.2)
# ---------------------------------------------------------------------------
def strip_scratchpad(raw_output: str) -> tuple[str, str]:
    """Split raw model output into (scratchpad, payload).
    Returns (scratchpad_content, translated_payload).
    """
    match = re.search(
        r"<engine_logs>(.*?)</engine_logs>\s*(.*)",
        raw_output,
        re.DOTALL,
    )
    if match:
        scratchpad = match.group(1).strip()
        payload = match.group(2).strip()
        # Handle stand-alone fallback: strip leading ---
        payload = re.sub(r"^---\s*\n", "", payload)
        return scratchpad, payload
    else:
        # No scratchpad found (--scratchpad=none or parse failure)
        return "", raw_output.strip()


# ---------------------------------------------------------------------------
# System Prompt Assembly
# ---------------------------------------------------------------------------
def assemble_system_prompt(domain: str) -> str:
    """Assemble: core prompt (§1–§13) + domain pack (semi-static zone).
    Fails fast with a [FATAL] message if the core prompt is missing or empty —
    translating without a system prompt would silently produce garbage.
    """
    core = load_file(CORE_PROMPT_FILE)
    if not core:
        print(
            f"[FATAL] Core prompt file '{CORE_PROMPT_FILE}' not found or empty. "
            f"Translation cannot proceed without the system prompt.",
            file=sys.stderr,
        )
        sys.exit(1)
    pack = load_domain_pack(domain)
    if pack:
        return core + "\n\n" + pack
    return core


# ---------------------------------------------------------------------------
# Main Translation Call
# ---------------------------------------------------------------------------
def translate(
    payload: str,
    domain: str,
    scratchpad_tier: str = "full",
    mode_flags: list[str] | None = None,
    model: str = "gpt-4o",
    api_base: str | None = None,
) -> tuple[str, str]:
    """Execute a single translation call.
    Returns (scratchpad, translated_payload).
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: pip install openai", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=api_base,
    )

    system_prompt = assemble_system_prompt(domain)

    # Build message list: system, few-shot prior turns (§3.5), user request.
    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    messages.extend(load_fewshot_messages(domain))

    # Build user message with mode flags, domain advisory, and token budget
    user_parts = []

    # Mode-flag rules block (§3.4): real rules, not just flag names.
    if mode_flags:
        rules = inject_mode_rules(mode_flags)
        if rules:
            user_parts.append(f"[Mode rules]\n{rules}")
        # Always record the active flags even when no rule text is defined.
        user_parts.append(f"[Active mode flags: {', '.join(mode_flags)}]")

    # Scratchpad tier signal (§3.2/§3.4) — communicate the requested tier to the model.
    if scratchpad_tier != "full":
        user_parts.append(f"[Scratchpad tier: {scratchpad_tier}]")

    # Domain advisory flag
    user_parts.append(f"[Domain pre-classification: {domain}]")

    # Token budget & Draft-Lock tier (§4.7, CJK-aware)
    estimated_tokens = estimate_tokens(payload)
    eff_words = count_effective_words(payload)
    draft_lock_tier = "Full" if eff_words < SEGMENT_WORD_THRESHOLD else "Segmented"
    user_parts.append(
        f"[Token budget: ~{estimated_tokens} tokens. "
        f"Draft-Lock tier: {draft_lock_tier}. "
        f"Effective words: {eff_words}]"
    )

    # Source payload
    user_parts.append(payload)

    user_message = "\n\n".join(user_parts)
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            top_p=0.1,
            messages=messages,
        )
    except Exception as e:
        print(f"[ERROR] API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Detect truncation: an incomplete <engine_logs> block would make
    # strip_scratchpad() return the whole raw output as 'payload'.
    finish_reason = response.choices[0].finish_reason
    if finish_reason == "length":
        print(
            "[WARNING] Output truncated (finish_reason=length). "
            "Consider segmenting the payload or using a model with a higher output limit.",
            file=sys.stderr,
        )

    raw = response.choices[0].message.content or ""
    scratchpad, translated = strip_scratchpad(raw)

    # Truncation safety: if the model hit its output token limit, the closing
    # </engine_logs> tag is likely missing. In that case strip_scratchpad()
    # returns the entire raw output as 'payload' (the regex didn't match),
    # exposing garbled scratchpad fragments to the user. Replace with a
    # clear notice instead.
    if finish_reason == "length" and not scratchpad:
        print(
            "[WARNING] Output truncated before </engine_logs>; "
            "emitting Notice Channel instead of garbled payload.",
            file=sys.stderr,
        )
        translated = (
            "[NOTICE] Output truncated before closing </engine_logs>. "
            "The scratchpad is incomplete. Please segment the payload or "
            "use a model with a higher output limit."
        )

    return scratchpad, translated


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Translation Engine v10.1 — Minimal Wrapper"
    )
    parser.add_argument(
        "--domain",
        choices=["engineering", "legal", "medical", "financial", "academic", "general"],
        default=None,
        help="Force domain pack (default: auto-detect from payload)",
    )
    parser.add_argument(
        "--scratchpad",
        choices=["full", "light", "none"],
        default="full",
        help="Scratchpad tier (default: full)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="Model name (default: gpt-4o)",
    )
    parser.add_argument(
        "--api-base",
        default=None,
        help="OpenAI-compatible API base URL",
    )
    parser.add_argument(
        "--save-scratchpad",
        default=None,
        help="Path to save scratchpad for audit",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input file (default: stdin)",
    )
    args = parser.parse_args()

    # Read payload
    if args.input == "-":
        payload = sys.stdin.read()
    else:
        payload = Path(args.input).read_text(encoding="utf-8")

    if not payload.strip():
        print("[NOTICE] Empty payload. No translation emitted.")
        sys.exit(0)

    # Domain classification
    domain = classify_domain(payload, args.domain)
    print(f"[INFO] Domain: {domain}", file=sys.stderr)

    # Mode flags
    mode_flags = []
    if args.scratchpad != "full":
        mode_flags.append(f"--scratchpad={args.scratchpad}")

    # Size-aware Draft-Lock (§4.7): segment oversized payloads at section/
    # paragraph boundaries and translate each segment in its own API call,
    # concatenating results. NOTE: §4.7's carry-over glossary state machine
    # is NOT yet implemented — segments are translated independently.
    segments = segment_payload(payload)
    if len(segments) > 1:
        print(
            f"[INFO] Draft-Lock tier: Segmented — {len(segments)} segments, "
            f"~{count_effective_words(payload)} effective words "
            f"(carry-over glossary NOT yet implemented; segments translated independently)",
            file=sys.stderr,
        )

    scratchpad_parts = []
    translated_parts = []
    for i, segment in enumerate(segments, 1):
        if len(segments) > 1:
            print(f"[INFO] Translating segment {i}/{len(segments)}...", file=sys.stderr)
        sp, translated = translate(
            payload=segment,
            domain=domain,
            scratchpad_tier=args.scratchpad,
            mode_flags=mode_flags,
            model=args.model,
            api_base=args.api_base,
        )
        if sp:
            scratchpad_parts.append(sp)
        translated_parts.append(translated)

    scratchpad = "\n\n--- segment boundary ---\n\n".join(s for s in scratchpad_parts if s)
    translated = "\n\n".join(t for t in translated_parts if t is not None)

    # Save scratchpad if requested
    if args.save_scratchpad and scratchpad:
        Path(args.save_scratchpad).write_text(scratchpad, encoding="utf-8")
        print(f"[INFO] Scratchpad saved to {args.save_scratchpad}", file=sys.stderr)

    # Output translated payload only (§3.2)
    print(translated)


if __name__ == "__main__":
    main()
```
