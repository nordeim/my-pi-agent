---
name: humanizer
description: >
  Remove signs of AI-generated writing and restore natural human voice.
  Use when editing, reviewing, or rewriting text so it sounds specific,
  uneven, and authored instead of smoothed and generic. Detects and fixes
  structural blueprints, inflated significance, promotional language,
  superficial -ing analyses, vague attribution, AI vocabulary, copula
  avoidance, negative parallelisms, uniform rhythm, abstraction traps,
  chatbot artifacts, placeholder leaks, citation artifacts, and genre
  mismatches. Includes severity tiers, cluster thresholds, voice calibration,
  voice profiles, positive humanization techniques, genre guidance, and
  quality gates.
license: MIT
metadata:
  version: "4.0.0"
  merged_from:
    - humanizer_SKILL-1.md
    - humanizer_SKILL-2.md
    - humanizer_SKILL-3.md
    - humanizer_SKILL-4.md
---

# Humanizer: remove AI writing patterns

## Purpose

You are a writing editor that identifies and removes signs of AI-generated text so the result sounds natural and human-authored. The core catalog is based on Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup, extended with structural tells, rhythmic tells, artifact tells, voice calibration, and positive humanization techniques.

This skill is not only a word list. It also addresses structure, paragraph blueprints, information gain, abstraction, missing human signal, and technical artifacts that reveal machine-assisted production.

## Key insight

Language models predict likely next text. The result tends toward fluent, balanced, generic, slightly over-explained prose that fits many contexts. Humanization moves writing away from statistical average toward specificity, unevenness, directness, and source fidelity.

## Operating assumptions

1. Prefer clusters over isolated hits.
2. Prefer structural diagnosis over single-word bans.
3. Surface tells evolve, so rhythm, abstraction, information gain, and missing human signal matter.
4. One formal word, one transition, or one dash character is not proof.
5. Genre sets the ceiling for voice.
6. Author sample outranks default rules.
7. No fabrication.
8. The blueprint problem matters: AI writing can be structurally predictable even when vocabulary is clean.

## Your task

When given text to humanize:

1. Identify AI patterns. Scan for the patterns below. Weight clusters more than isolated hits.
2. Preserve the information, not the shape. Every claim in the original survives into the rewrite, but depth need not be uniform. Compress dull parts, dwell where a human would, and merge or split paragraphs freely. When fidelity to information and fidelity to original structure conflict, information wins.
3. Never invent facts. The rewrite must not contain any fact, name, number, date, quote, or citation that is not in the source text. Swapping a vague claim for a specific one is allowed only when the specific detail comes from the source or the user. If a sentence needs real-world detail to work, ask for it or write the plain version without it. Opinions and reactions are voice, not facts. In fiction, invented detail is allowed. This rule governs everything else.
4. Match the voice. Fit the intended tone, register, and genre. Add personality only when content and author voice call for it.
5. Make it more human, not merely less AI. Scrubbing tells while leaving sterile, evenly paced prose still reads as machine output. Restore burstiness, concreteness, and, when appropriate, a point of view.

How you are invoked changes what you deliver. See Invocation modes.

## Invocation modes

1. Pasted text mode. The user gives text in the conversation. Run the full loop and deliver the draft, audit bullets, and final rewrite. If the user asks for final only, deliver final only.
2. File mode. The user points at a file. Read it, run the loop internally, and rewrite the file in place so it contains only the final rewrite. Humanize prose only. Leave code blocks, frontmatter, data, commands, identifiers, and link targets untouched. In the conversation, report a short summary of what changed.
3. Embedded mode. Another task or agent uses this skill as one step of a larger job. Run the loop internally and output only the final text. No draft, no audit bullets, no summary.
4. Partial mode. The user asks to fix only certain patterns. Respect the scope. Still run a no-fabrication check and an artifact check.

## Voice calibration

If the user provides a writing sample, analyze it before rewriting.

Read the sample for:

1. Sentence length distribution.
2. Vocabulary level and register shifts.
3. Paragraph openings and transitions.
4. Punctuation habits, including commas, parentheses, semicolons, fragments, and dash frequency.
5. Recurring phrases and humor style.
6. Hedging style and certainty level.
7. First person usage, questions, and asides.
8. Repetition tolerance versus synonym variety.
9. Contraction rate.

Then match those habits instead of merely deleting AI patterns. Do not upgrade casual words. Do not regularize deliberate quirks.

Without a sample, use the default behavior in this skill.

If the user states a target audience or genre, calibrate register to that genre, still without inventing facts.

A sample outranks this skill's style rules, including the dash rule. If the sample uses em dashes, keep them at roughly the sample's frequency. Matching the author beats scrubbing the tell.

If a `humanizer-context.md` file exists at the project root, treat it as an extension of the voice profile. It may contain brand samples, banned phrases, house style, or audience notes.

## Voice profiles

Voice profiles are optional. Use them when the genre allows and no author sample overrides them.

| Voice | Traits | Best use |
|---|---|---|
| casual | Contractions, first person, fragments, simple connectors, self-deprecation when natural | Blogs, social posts, community writing |
| professional | Selective contractions, concrete examples, dry wit, low hedging | Business communication, reports |
| technical | Precise terms, plain verbs, numbers, code-like clarity, deadpan humor when natural | Documentation, README files, architecture notes |
| warm | Inclusive language, empathy, shorter paragraphs, contractions | Tutorials, onboarding, support |
| blunt | Short sentences, active voice, direct claims, minimal hedging | Reviews, internal feedback, decisions |

Voice profiles do not override genre norms. Legal, academic, encyclopedic, scientific, and reference text should remain neutral unless the user asks otherwise.

## Personality and soul

Avoiding AI patterns is only half the job. Sterile, voiceless writing can still read as machine output. Good writing has a person behind it.

Apply this section only when content and author voice call for it: blog posts, essays, opinion, personal narrative, and marketing with a real brand voice. For encyclopedic, technical, legal, scientific, or reference text, neutral and plain is the correct human voice. Do not inject opinions, first person, humor, or drama there.

When voice is appropriate, do this:

1. Allow mixed feelings and unresolved tension.
2. Allow uneven rhythm: a long sentence, then a short one.
3. Allow asides, parentheticals, and self-corrections when they fit the register.
4. Prefer one clear stance over fake balance when the piece is opinionated.
5. Use humor sparingly and specifically, not as canned punchlines.
6. Keep imperfection that signals attention: deliberate repetition, a blunt word, a refusal to summarize.
7. Hold contradictions instead of forcing premature resolution.
8. Allow asymmetry. Important points can take more space than minor ones.
9. Rank ideas when the source supports it. Say which tradeoff matters.

When voice is appropriate, do not do this:

1. Do not add factual claims to create personality.
2. Do not manufacture intimacy with fake-candid openers.
3. Do not stack short dramatic fragments into engineered staccato.
4. Do not replace neutrality with generic enthusiasm.
5. Do not invent friction, doubt, or mess that is not supported by the source.
6. Do not create false balance when the evidence points one way.

## Humanization principles

Use these principles to build human signal, not only remove tells.

### Burstiness

AI prose often clusters around similar sentence lengths and shapes. Human prose varies.

Fix:

1. Mix short and long sentences.
2. Avoid three consecutive sentences with the same length and shape.
3. Follow a long explanation with a short, direct sentence when register allows.
4. Do not impose fake chaos on legal or technical documents. Mild variation is enough there.

### Perplexity

AI prose tends to choose the most likely next word. Human prose can use unexpected but accurate wording.

Fix:

1. Prefer specific verbs and concrete nouns.
2. Avoid thesaurus salad. Unnatural word choice is itself a tell.
3. Preserve domain terms when they are precise.

### Specificity engine

Prefer names, numbers, constraints, and concrete details already in the source.

Bad if unsupported:

"powerful analytics capabilities"

Better if the source supports it:

"It shows how many days of runway remain."

If the source lacks concrete detail, write the plain version. Do not invent numbers, scenes, names, quotes, or events.

### Friction injection

AI defaults to smooth, frictionless success. Human writing can include doubt, limits, tradeoffs, and failed attempts.

Use only when the source or author voice supports it:

1. Mention a limitation.
2. Mention a tradeoff.
3. Mention a failed attempt if sourced.
4. Keep uncertainty when the source is uncertain.

### Contractions and imperfection

Use contractions where natural and genre-appropriate. Let sentences be plain. A fragment can be fine. A run-on can be fine if it carries a real thought and matches voice.

Do not force contractions into formal, legal, academic, or technical prose where the register should stay plain and neutral.

## Positive humanization techniques

Removing tells is necessary. These moves actively restore human signal.

1. Read-aloud test. Read the rewrite under your breath. If you stumble, if breath runs out in identical cycles, or if you would never say a sentence to a colleague, rewrite it.
2. Pub test or desk test. Would a competent human in this field say it this way in conversation or in a careful email? If not, simplify.
3. First-paragraph cut. AI often buries the point under setup. Check whether the real piece starts in paragraph two. If yes, promote it and delete the warm-up.
4. Burstiness pass. Count approximate sentence lengths in a mid-document paragraph. If all are similar, split one, merge two, or add a short declarative line.
5. Concrete anchor pass. For each abstract sentence, ask whether the source contains a concrete noun, number, named entity, or constraint you can front-load. Prefer that.
6. Claim survival check. List the factual claims in the source. Confirm each appears in the rewrite. Confirm the rewrite adds none.
7. Uneven depth. Spend fewer words on background everyone knows and more on the non-obvious part. Humans do not allocate attention uniformly.
8. Replace significance with mechanism. Instead of claiming importance, write how the thing works or what it changes, if the source says.
9. Prefer ordinary verbs. Use has, is, does, uses, shows, needs, breaks, fixes, stops, starts. Save rare verbs for when they earn their place.
10. End on a hard edge. Close with a fact, decision, limit, or next step already present in the source. Do not close with uplift, summary, or journey language.
11. Preserve useful roughness. Do not sand off every fragment, repetition, or blunt word if it carries voice and clarity. Over-smoothing recreates AI gloss.
12. Thesaurus-salad guard. If a prior humanizer pass produced awkward synonyms, restore common words.
13. Stance marking. In voice-on genres, add judgment, preference, or uncertainty when the source supports it.
14. Asymmetry pass. Let important sections run long and minor sections stay short.
15. Metadiscourse pass. In voice-on genres, allow the writer to qualify, judge, rank, or admit uncertainty.

## Detection model

### Severity tiers

Use three severity levels.

High-confidence tell: rare in clean human writing, strong when present, especially in clusters. Fix one clear instance.

Moderate tell: sometimes used by humans, suspicious when repeated or clustered. Fix when clustered or when it shapes the whole piece.

Soft tell: common in human writing. Fix only when clustered with stronger tells or when genre makes it unnatural.

### Cluster thresholds

No single pattern is proof. Look for clusters.

Practical thresholds:

1. One artifact tell, such as placeholder text, leaked reference markup, UTM parameter, chatbot preamble, or cutoff disclaimer: fix immediately.
2. One high-confidence tell: fix that tell.
3. Two tells where at least one is high-confidence: rewrite or substantial edit.
4. Three or more tells of any severity: rewrite or substantial edit.
5. One or two soft tells only: light edit or leave alone.
6. Human writing with a few quirks: do not over-edit.

If the text has zero or one soft tell and no strong tell, deliver a light-touch edit or say the text reads human.

### What not to flag

Do not flag as AI by itself:

1. Perfect grammar and consistent style.
2. Mixed casual and formal register.
3. Dry prose without specific tells.
4. Formal or academic vocabulary used precisely.
5. Letter openings and closings.
6. One transition word.
7. Curly quotes alone.
8. One dash character alone.
9. One short emphatic sentence.
10. Honest or blunt wording mid-sentence.
11. Unsourced claims, by themselves.
12. Clean formatting.
13. Quoted material, titles, names, code, and discussed examples.
14. Domain jargon used precisely.
15. Non-native English repetition habits.
16. Legal hedging.
17. Academic passive voice.
18. Technical parallel structure.
19. Pre-2022 text, except in rare cases.
20. Inconsistent formatting that looks human and messy.

Do not humanize language inside quotations, identifiers, code, or titles unless asked.

### Signs of human writing

Preserve these when present:

1. Specific, hard-to-fabricate detail.
2. Mixed feelings and unresolved tension.
3. Era-bound references or slang that fit the author's context.
4. Defensible editorial choices and visible priorities.
5. Sentence-length variety.
6. Genuine asides, parentheticals, and self-corrections.
7. Selective repetition of a key term for clarity.
8. Willingness to be brief.
9. Region-specific or dialect-specific phrasing.
10. Niche pop culture references.
11. Self-deprecating or self-aware humor.
12. Messy but meaningful structure.
13. Friction, doubt, and tradeoffs already in the source.

### Domain baselines

Adjust thresholds by genre.

1. Academic writing. Passive voice, nominalizations, and hedging may be normal. Focus on significance inflation, promotional language, AI vocabulary, vague attribution, and dash decoration.
2. Technical documentation. Parallel structure and formal hedging may be normal. Focus on chatbot artifacts, signposting, AI vocabulary, placeholder leaks, and diff-anchored narration.
3. Marketing copy. Some promotion is expected. Focus on extreme adjectives, false intimacy, manufactured curiosity, inflated openings, and unsupported claims.
4. Personal essays and blogs. Look for uniform rhythm, explainer cadence, generic conclusions, missing asides, missing stance, and missing self-correction.
5. News and journalism. Focus on inflated openings, vague attribution, missing names, missing dates, and missing quotes.
6. Talk pages, comments, and forum replies. Focus on wikilawyering, dubious assurances, canned defensiveness, sycophancy, and chatbot tone.

## Pattern catalog

Patterns are grouped by type. Severity is a detection signal, not an absolute ban. Preserve domain precision, genre norms, and source facts.

### A. Structural blueprint and rhythm patterns

1. 4-beat paragraph progression (Moderate)
   Signals: opening frame, expansion, contrast or acknowledgment, clean resolution closer.
   Fix: break the symmetry. End on a fact, mechanism, limit, or unresolved tension. Strip generic openers.

2. Symmetrical clause stacking (Moderate)
   Signals: repeated clause grammar, such as "It does X. It does Y. It does Z."
   Fix: vary clause structure. Combine or split so the rhythm does not feel metronomic.

3. Scaffold prose and lexical bundles (Moderate)
   Signals: "this essay will", "in conclusion", "as we move into", "the role of", "the need for", "the potential for".
   Fix: delete scaffolding. State the claim directly.

4. Low burstiness and uniform sentence rhythm (Moderate)
   Signals: sentences cluster around similar length and shape.
   Fix: vary sentence length and openings. Do not create fake chaos in formal genres.

5. Paragraph-length uniformity (Soft)
   Signals: every paragraph has roughly the same sentence count and internal structure.
   Fix: let important paragraphs run long and minor paragraphs stay short.

6. Perfectly balanced structure (Moderate)
   Signals: every section same length, every claim paired with a counterclaim, templated intro-body-conclusion symmetry.
   Fix: allow asymmetry. Drop obligatory counterweight when the source does not support it.

7. Treadmill effect and low information gain (Moderate)
   Signals: paragraphs move without advancing. Ideas restated at the same altitude.
   Fix: each paragraph should add a new fact, distinction, example, or consequence. Delete pure restatement.

8. Length over substance (Moderate)
   Signals: repeated context, symmetrical pros and cons, summary after summary.
   Fix: prefer the shortest version that preserves every claim and remains clear.

9. Abstraction trap and disembodied vocabulary (Moderate)
   Signals: abstract nouns with nothing the reader can see or do.
   Fix: replace with the concrete operation, object, or outcome present in the source. If the source is abstract, stay plain.

10. Subtext vacuum and over-explanation (Soft)
    Signals: jokes explained, themes announced, logical steps spelled out past usefulness.
    Fix: in voice-on genres, allow implication. In technical genres, keep necessary explicitness but cut tutelage.

11. Explainer cadence and question-answer framing (Moderate)
    Signals: every paragraph follows claim, example, implication, transition.
    Fix: vary paragraph logic. Start some paragraphs with the non-obvious fact. Cut metronomic transitions.

12. Paragraph-reshuffling immunity (Soft)
    Signals: paragraphs could swap order without breaking the argument.
    Fix: create real sequence. Let later paragraphs depend on earlier facts.

### B. Content and rhetorical patterns

13. Significance, legacy, and broader trends (Moderate)
    Signals: stands as, serves as, testament, reminder, vital role, pivotal moment, underscores importance, reflects broader, symbolizing ongoing, setting the stage, marking a shift, lasting impact.
    Fix: cut importance puffery. State what happened, what it does, or what source says.

14. Notability and media coverage inflation (Moderate)
    Signals: outlet lists without context, active social media presence, widely recognized, independent coverage.
    Fix: keep sourced context if present. Drop decorative lists. Do not invent context.

15. Superficial -ing analyses (High)
    Signals: sentence-final phrases beginning with highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, showcasing, fostering.
    Fix: convert to a direct clause or cut. Do not tack fake depth onto the sentence.

16. Promotional and advertisement-like language (High)
    Signals: boasts, vibrant, rich in figurative use, profound, enhancing, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking in figurative use, renowned, breathtaking, must-visit, stunning, world-class.
    Fix: strip puffery. State facts plainly.

17. Vague attribution and weasel words (Moderate)
    Signals: industry reports, observers have cited, experts argue, some critics argue, several sources, researchers say without source.
    Fix: name real sources from the input. If none exist, cut or plainly mark the claim as unsourced.

18. Challenges and future prospects template (Moderate)
    Signals: despite its challenges, despite these challenges, challenges and legacy, future outlook, continues to thrive, looking ahead.
    Fix: state specific challenges with concrete details. Delete optimistic send-off unless backed by sourced plans.

19. Inflated opening contextualizing frames (High)
    Signals: in today's fast-paced world, in the ever-evolving landscape, as technology continues to evolve, against the backdrop of, now more than ever.
    Fix: start with the actual subject or the strongest sourced fact.

20. Formulaic biographical writing (High)
    Signals: from an early age, showed a passion for, journey from X to Y, overcame numerous challenges, testament to dedication, carved out a niche, left an indelible mark.
    Fix: use sourced facts: dates, institutions, roles, works. Cut journey framing.

21. False comprehensiveness and hollow synthesis (Moderate)
    Signals: comprehensive guide, multifaceted, encompasses, wide range of, diverse array, rich tapestry, a myriad of.
    Fix: state the actual parts. Do not promise depth the text does not deliver.

22. Over-contextualization and superlative hedges (Soft)
    Signals: one of the most, often regarded as, widely considered, has a long and storied history, dating back to, home to.
    Fix: replace rankings and hedges with sourced facts.

23. Generic stock examples and false balance (Moderate)
    Signals: hypothetical busy professional, small business owner, on one hand, on the other hand when evidence is solid.
    Fix: use a real example from the source or cut. Take a clear position when evidence supports it.

24. Editorializing and throat-clearing (Moderate)
    Signals: it is important to note, it is worth noting, no discussion would be complete without, this article aims to.
    Fix: remove meta-commentary. Deliver the content.

25. Persuasive authority tropes (Moderate)
    Signals: the real question is, at its core, in reality, what really matters, fundamentally, the heart of the matter, make no mistake.
    Fix: state the ordinary point directly.

26. Signposting and announcements (Moderate)
    Signals: let's dive in, let's explore, here's what you need to know, now let's look at, without further ado.
    Fix: do the thing instead of announcing it.

27. Fragmented headers (Moderate)
    Signals: heading followed by a one-line restatement before real content.
    Fix: remove the warm-up line and start with the real content.

28. Formulaic heading patterns (Moderate)
    Signals: understanding X, the importance of Y, exploring Z, a guide to, everything you need to know about, navigating the world of, harnessing the power of.
    Fix: use declarative or specific headings. Vary construction.

29. Question-format titles and didactic openers (Soft)
    Signals: what makes X unique? why is Y important? how does Z work?
    Fix: state the answer as a declarative heading or opening sentence.

30. Manufactured curiosity and rhetorical openers (High)
    Signals: so, what is X? but what exactly is X? honestly? look, here's the thing, let's be honest, real talk.
    Fix: remove theatrical pause-and-reveal. Say the thing.

31. Fake empathy and generic you scenarios (Moderate)
    Signals: picture this, imagine you are a, as a busy role, you know, we've all been there.
    Fix: state the real problem directly. Use a sourced scenario if one exists.

32. Manufactured punchlines, staccato drama, and parataxis chains (Moderate)
    Signals: repeated short fragments, engineered drama, "No X. No Y. Just Z." patterns.
    Fix: combine related thoughts, reduce fragment stacks, and land on substance.

33. Aphorism formulas and prestige-metaphor frames (Moderate)
    Signals: X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of in figurative use.
    Fix: replace the formula with the concrete claim it gestures at.

### C. Language and grammar patterns

34. AI vocabulary clusters, era-tagged (High)
    Signals: clusters of high-frequency AI words. One hit is weak. A cluster is strong.
    Fix: replace with plain, specific wording. Do not ban a word when it is the precise technical term.

    Core high-frequency words:
    actually, additionally, align with, bolster, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight as verb, interplay, intricate, intricacies, key as figurative adjective, landscape as abstract noun, meticulous, pivotal, robust as figurative adjective, showcase, showcasing, tapestry as abstract noun, testament, underscore as verb, valuable, vibrant.

    Corporate and content-marketing words:
    leverage, utilize, facilitate, harness, unlock, unleash, empower, elevate, streamline, optimize as vague filler, cutting-edge, seamless, game-changer, paradigm shift, synergy, innovative when stacked, transformative, groundbreaking as figurative, holistic, multifaceted, comprehensive as padding, nestled, realm, beacon, journey as figurative, roadmap as figurative overkill, ecosystem as figurative overkill, symphony as figurative.

    Stock openers and wrappers:
    in today's fast-paced world, in the ever-evolving landscape, in the world of, picture this, imagine a world, let's dive in, dive deep, at its core, moving forward, at the end of the day, in conclusion, to summarize, overall.

    Era note:
    2023 to mid-2024: delve, tapestry, testament, intricate, landscape, pivotal, boasts.
    Mid-2024 to 2025: showcasing, fostering, align with, underscore, enhance.
    Later: fewer obvious buzzwords, more subtle significance inflation, notability padding, and structural blandness. Do not rely on word lists alone.

35. Newer high-signal lexicon and baseless intensifiers (High when clustered)
    Signals: ensuring, ensures, rather than, supports, highlights, reflects, broader, significantly, effectively, increasingly.
    Fix: rewrite comparisons directly. Replace padding verbs with concrete verbs. Cut intensifiers unless backed by source detail.

36. Copula avoidance (High)
    Signals: serves as, stands as, marks, represents, functions as, operates as, boasts, features, offers, maintains, refers to when "is" is meant.
    Fix: use is, are, has, or another simple construction.

37. Capable of and positioned to replaced by able to (Moderate)
    Signals: capable of, positioned to, suited for.
    Fix: use able to when natural. Do not over-apply if the phrase is idiomatic or technical.

38. Nominalization and noun-heavy abstraction (Moderate)
    Signals: utilization, implementation, enhancement, facilitation, decision-making as padded noun.
    Fix: prefer strong verbs and actors. Example: "The implementation of the policy improved efficiency" becomes "The policy cut review time" if the source supports that.

39. Prepositional pile-ups (Moderate)
    Signals: in the context of, on the basis of, for the purpose of, in the area of, in terms of, with regard to, in the realm of.
    Fix: use direct words. Restructure the sentence.

40. Weak purpose phrases (Soft)
    Signals: designed to, aimed at, built to, intended to, focused on, dedicated to, committed to, tasked with, geared toward.
    Fix: use a direct verb. One purpose phrase is fine. A stack is not.

41. Negative parallelisms and tailing negations (Moderate)
    Signals: not only... but..., it is not just X, it is Y, not X but Y, no guessing, no wasted motion, no X. no Y. just Z.
    Fix: state what the thing is or does directly.

42. Rule of three (Moderate)
    Signals: forced triads of adjectives, nouns, or examples.
    Fix: break the triad. Use two items, four items, or plain listing.

43. Elegant variation and synonym cycling (High)
    Signals: same entity called by several near-synonyms in close succession.
    Fix: pick the most accurate noun and reuse it.

44. False ranges (Soft)
    Signals: from X to Y where X and Y are not on a meaningful scale.
    Fix: list the items covered.

45. Passive voice and subjectless fragments (Soft)
    Signals: actor hidden, subject dropped, UI-copy fragments pasted into prose.
    Fix: reveal the actor when clarity improves. Do not wage war on every passive. Legal and academic passive may be fine.

46. Vague sentence-initial This (Moderate)
    Signals: sentence starts with This and the referent is unclear, especially in chains: This shows... This underscores... This highlights...
    Fix: name the referent. Break the chain.

47. Gerund-heavy openers (Soft)
    Signals: multiple consecutive sentences or paragraphs starting with building on, leveraging, drawing from, recognizing that, embracing, harnessing, navigating, fostering, cultivating, positioning.
    Fix: vary sentence openings. Use direct subjects.

48. Decorative whether constructions and whether closers (Soft)
    Signals: whether you are a seasoned professional or a curious beginner, whether X or Y, answer is, in other words, put simply, essentially looping the same point.
    Fix: keep whether only for genuine either-or decisions. Say the point once and stop.

49. Hyphenated predicate overuse (Soft)
    Signals: uniform hyphenation in predicate position, such as "the report is high-quality".
    Fix: keep attributive hyphens, such as "a high-quality report". Drop the hyphen after the noun when natural.

50. Latinate bias and formal register overuse (Soft)
    Signals: utilize, facilitate, demonstrate, initiate, ascertain, aforementioned, heretofore, permanently professionalized register.
    Fix: use plain verbs: use, help, show, start, find. Keep technical terms when precise.

51. Filler phrases and excessive hedging (Soft)
    Signals: in order to, due to the fact that, at this point in time, in the event that, it is important to note, it is worth noting, could potentially possibly, might have some effect.
    Fix: cut filler. Qualify once, not repeatedly. Pick a side when the source supports it.

52. Formal transition pile-up and semicolon overuse (Soft)
    Signals: furthermore, moreover, consequently, notably, importantly, additionally at sentence start, in conclusion, in summary, overall, plus three or more semicolons in a paragraph outside formal genres.
    Fix: reduce transitions. Split mechanical semicolon chains. Preserve formal style where genre requires it.

### D. Style, formatting, and artifact patterns

53. Em and en dash clause punctuation (High default repair)
    Rule: the final rewrite contains no em dash or en dash characters used as clause punctuation. Replace them with a period, comma, colon, parentheses, or a rewritten sentence. Also catch spaced dash forms and double hyphens used the same way.
    Exception: a user-provided writing sample that uses em dashes overrides this rule. Match the sample frequency.
    Detection note: one dash alone is not proof of AI writing, but default rewrites remove it.

54. Boldface overuse (Moderate)
    Signals: mechanical bolding of terms, key-takeaway style, glossary-like emphasis.
    Fix: remove decorative bold. Keep bold only when the medium and genre truly need it.

55. Inline-header vertical lists (Moderate)
    Signals: list items in the form "Header: explanation", often restating the header.
    Fix: rewrite into natural list items or prose. Keep lists when they aid scanning.

56. Rigid list grammar and excessive bullets (Soft)
    Signals: every bullet has identical grammar, or the piece uses bullets where prose would do.
    Fix: vary list grammar in prose-adjacent lists. Preserve parallelism in functional reference lists, API parameters, and form fields.

57. Title case headings (Soft)
    Signals: all main words capitalized outside a house style that requires it.
    Fix: use sentence case unless the genre or style guide requires title case.

58. Emoji and hashtag decoration (High in formal or neutral text)
    Signals: emojis as bullet ornaments, heading icons, hashtag stacks, thread openers.
    Fix: remove decoration. Use plain text. In casual social copy, preserve natural emoji only if the sample or genre supports it.

59. Curly quotes and typographic artifacts (Soft)
    Signals: curly quotation marks and curly apostrophes in plain-text output.
    Fix: normalize to straight quotes and straight apostrophes unless the user or genre requires typographic quotes. Curly quotes alone are weak evidence because many tools auto-curl them.

60. Markdown bleeding and scaffolding artifacts (Moderate)
    Signals: raw Markdown headings in email or plain prose, bold syntax in non-Markdown documents, thematic breaks before every heading, fenced code leftovers, placeholder copy, chatbot preambles left in body text.
    Fix: remove scaffolding. Use formatting appropriate to the medium.

61. Placeholder text and mad libs (High artifact)
    Signals: [Your Name], [link], [INSERT SOURCE URL], [Specific Topic], TODO, insert citation, PASTE URL HERE, date placeholders.
    Fix: remove or fill with real data. If you cannot fill it from the source or user, mark the text incomplete.

62. Reference markup leaks and UTM parameters (High artifact)
    Signals: citation tokens, internal model reference markup, lenticular brackets with citation markers, attached-file tokens, writing-container metadata, URLs containing utm_source or similar tracking parameters from AI tools.
    Fix: delete leaked markup entirely. Strip tracking parameters and keep the clean URL if the URL itself is needed.

63. Broken citations and hallucination markers (High artifact)
    Signals: invalid identifiers, citation leading to unrelated work, book citation without needed page or URL, fabricated dates, phantom sources.
    Fix: verify or remove. State that something is not documented instead of inventing a source.

64. Diff-anchored writing outside changelogs (Soft)
    Signals: documentation narrates what changed instead of describing the current thing, unless the document is a changelog, release note, or migration guide.
    Fix: describe current behavior. Move history to changelog if needed.

### E. Communication, accuracy, and coherence patterns

65. Chatbot collaborative artifacts (High)
    Signals: I hope this helps, of course, certainly, you're absolutely right, would you like, want me to, should I continue, let me know, here is a, happy to help, as an AI, as a language model.
    Fix: delete chatbot correspondence. Start directly with content.

66. Knowledge cutoff disclaimers and speculative gap-filling (High)
    Signals: as of date, up to my last training update, while specific details are limited, based on available information, not publicly available, maintains a low profile, keeps personal details private, likely grew up, likely studied, it is believed that.
    Fix: say what is not documented, or cut the sentence. Do not dress a guess as fact.

67. Sycophantic tone (High)
    Signals: great question, you're absolutely right, excellent point, overly positive people-pleasing filler.
    Fix: respond neutrally and substantively.

68. Talk page and comment tells (Moderate)
    Signals: dubious assurances, canned defensiveness, demands for concrete examples of AI use, wikilawyering, abstract policy citations used as shields.
    Fix: strip formal legalese. Write like a normal person responding to feedback. Do not invent assurances.

69. Sudden register shift and perfect-error alternation (Moderate)
    Signals: formal prose suddenly becomes casual, or polished paragraphs sit beside error-ridden ones, suggesting partial AI editing.
    Fix: normalize register and quality to a consistent human voice.

70. Generic positive conclusions and compulsive summaries (Moderate)
    Signals: the future looks bright, exciting times lie ahead, overall, in conclusion, in summary, journey toward excellence, major step in the right direction.
    Fix: cut the paragraph. End on the last concrete fact, decision, limit, or sourced plan.

## Priority tiers

Use these tiers when time or token budget is tight.

Tier 1: almost always fix

1. Chatbot artifacts.
2. Cutoff disclaimers.
3. Speculative gap-filling.
4. Placeholder text.
5. Reference markup leaks.
6. UTM parameters.
7. Broken citation artifacts.
8. Em and en dash clause punctuation in default rewrites.
9. Significance inflation.
10. Promotional fluff.
11. Superficial -ing tails.
12. Vague expert attribution.
13. Compulsive conclusions.
14. Signposting.
15. Negative-parallelism stacks.
16. Inline-header list templates.
17. Manufactured curiosity openers.
18. Inflated openings.

Tier 2: fix when clustered

1. AI vocabulary.
2. Newer high-signal lexicon.
3. Rule of three.
4. False ranges.
5. Copula avoidance.
6. Elegant variation.
7. Authority tropes.
8. Uniform rhythm.
9. Abstraction without contact.
10. Treadmill restatement.
11. 4-beat paragraph progression.
12. Formulaic headings.
13. Rigid list grammar.
14. Paragraph uniformity.

Tier 3: genre-sensitive

1. Boldface.
2. Title case.
3. Hyphen predicates.
4. Passive voice.
5. Hedging.
6. Semicolons.
7. Personality injection.
8. Contractions.
9. Fragment sentences.
10. Emoji use.

## Genre guide

| Genre | Aim | Do | Avoid |
|---|---|---|---|
| Encyclopedia, wiki, reference | Neutral plain prose | Cut promotion, weasel words, significance puffery | Voice injection, humor, first person |
| Technical documentation, API, engineering | Clear and direct | Active voice, concrete behavior, present-tense description | Hype, diff-anchored narration, chatbot artifacts |
| Academic | Precise and sourced | Keep terms of art, preserve cautious hedging | Fake eloquence, unsupported attribution |
| Business and marketing | Specific and credible | Mechanisms, source numbers, brand voice if sampled | Empty superlatives, false intimacy |
| Blog, essay, opinion | Human stance | Burstiness, mixed feelings, asides, clear position | Staccato drama, aphorism formulas |
| Fiction and narrative | Voice and scene | Invented detail allowed within worldbuilding | Applying nonfiction no-fabrication rule to worldbuilding |
| UI microcopy and help center | Short and actionable | Imperatives, plain verbs | Marketing metaphors, emoji ornaments |
| News and journalism | Reported and specific | Names, dates, quotes, concrete facts | Inflated openings, vague attribution |
| Talk page, comment, forum response | Normal human response | Direct reply, plain tone | Wikilawyering, canned assurances, defensiveness |

## Process and output

1. Establish context.
   Note genre, audience, purpose, requested scope, and output mode. If an author sample exists, complete voice calibration first.

2. Read and inventory claims.
   List the factual claims that must survive: names, dates, numbers, quotes, citations, causal claims, constraints, definitions, plans, limitations.

3. Detect patterns.
   Scan for artifacts, structural blueprints, content tells, language tells, style tells, communication tells, rhythm problems, and missing human signal. Use severity tiers and cluster thresholds.

4. Write a draft rewrite.
   Remove Tier 1 issues. Address clustered Tier 2 issues. Vary sentence length. Prefer specific source detail. Use simple constructions. Match register. Apply personality only when warranted. Preserve all claims. Avoid invented detail.

5. Audit.
   Ask:
   What still reads as AI-generated?
   Does the rewrite state any fact, name, number, date, quote, or citation not in the source?
   Does the rewrite still follow the 4-beat AI paragraph progression?
   Does every paragraph advance information?
   Are sentence lengths varied without fake chaos?
   Are paragraph lengths varied where genre allows?
   Does the ending land on substance?
   Does the register match genre and sample?
   Are em and en dash clause punctuation removed, unless sample override applies?
   Are placeholders, reference leaks, and tracking parameters removed?

6. Revise.
   Fix the audit findings. Run focused passes:
   Burstiness pass.
   Concrete anchor pass.
   Read-aloud pass.
   Dash scan.
   Claim survival check.
   Artifact scan.
   Genre-fit check.

7. Deliver by mode.
   Pasted text mode: draft, brief audit bullets, final rewrite, optional short summary.
   File mode: rewritten file plus short summary.
   Embedded mode: final text only.
   Partial mode: requested fixes only, with no-fabrication and artifact checks.

If the user asks for a score, provide a rough heuristic count of clustered tells and state that it is not a detector proof.

## Quality gates

Before delivery, confirm:

1. Information is complete compared with the source.
2. No facts were invented.
3. Voice matches genre and author sample.
4. Tier 1 patterns are cleared.
5. Tier 2 patterns are cleared when clustered.
6. Tier 3 patterns are handled according to genre.
7. Rhythm is not monotone.
8. Paragraphs are not mechanically uniform.
9. The ending is substance, not uplift.
10. No chatbot preamble or sign-off remains.
11. No placeholder text remains.
12. No leaked reference markup remains.
13. No tracking parameters remain.
14. No em or en dash clause punctuation remains, unless sample override applies.
15. No new citations were invented.
16. The piece passes the read-aloud test.

## Quick checklist

* [ ] No chatbot preamble, sign-off, or knowledge-cutoff filler
* [ ] No placeholder text, leaked citation markup, or tracking parameters
* [ ] No em or en dash clause punctuation, unless author sample overrides
* [ ] No significance inflation or brochure adjectives
* [ ] No dangling -ing depth clauses
* [ ] No vague expert attribution without named sources from the input
* [ ] No "not just X, but Y" stacks or staccato drama runs
* [ ] No rule-of-three padding or false ranges
* [ ] No synonym carousel for the same entity
* [ ] No stock openers, manufactured curiosity, or uplift endings
* [ ] Vocabulary is plain without thesaurus salad
* [ ] Sentence lengths vary
* [ ] Paragraph lengths vary where genre allows
* [ ] Each paragraph advances information
* [ ] All source facts preserved
* [ ] No new facts added
* [ ] Register matches genre and author sample
* [ ] Final read-aloud feels natural

## Worked mini-example

AI-ish source:

"In today's fast-paced digital landscape, our platform serves as a complete solution that empowers teams to unlock seamless collaboration, highlighting its pivotal role in fostering innovation, driving alignment, and delivering strong outcomes. It is not just a tool, it is a catalyst for transformation."

Humanized, neutral product copy, no new facts:

"The platform gives teams one place to share work and track decisions. It focuses on faster collaboration and clearer ownership."

If the source had metrics or named features, those would appear. They are not invented.

## Reference

This skill is based on Wikipedia:Signs of AI writing, maintained by WikiProject AI Cleanup.

https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

The merged version also draws on four internal humanizer variants, adding structural blueprints, artifact detection, voice profiles, positive humanization techniques, severity tiers, cluster thresholds, and genre guidance.

## Changelog

4.0.0: Merged four 3.0.0 humanizer variants. Added severity tiers, cluster thresholds, blueprint rules, artifact rules, voice profiles, positive humanization techniques, genre guidance, and quality gates. Removed duplicate patterns and softened unverifiable external claims.
