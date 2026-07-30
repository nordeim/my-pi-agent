Summary of Updates to nextjs-typescript_SKILL.md 
 
File: /home/project/maison/nextjs-typescript_SKILL.md 
Net addition: 264 lines (4260 → 4524) 
 
### 12 Integration Points 
 
┌────┬───────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────┐ 
│ #  │ Section                                                       │ Addition                                                                            │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 1  │ §2.4 Distinguish infrastructure failure from source-code debt │ New "Third category: construction-time validation failures" concept with rule       │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 2  │ §4.2 TypeScript Handbook — Mistake 16                         │ New tRPC reserved word procedure mistake with fix, lesson, prevention, and patterns │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 3  │ §4.2 TypeScript Troubleshooting Checklist — Step 8            │ New step for "check-types passes but build fails" scenario                          │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 4  │ §4.7 Third-Party SDK Handbook — tRPC Lessons                  │ New subsection with 2 mistakes (reserved words + generic naming)                    │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 5  │ §4.7 SDK Integration Checklist — Step 11                      │ New step for tRPC reserved word verification                                        │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 6  │ §5.3 TypeScript Patterns                                      │ New pattern: "Name tRPC procedures with domain-specific verb-noun pairs"            │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 7  │ §6.3 TypeScript Anti-Patterns                                 │ 2 new rows in table (reserved word + generic names)                                 │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 8  │ §7 Playbook 14                                                │ New playbook: "tRPC build failure — Reserved words used in router({}) call"         │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 9  │ §8.1 General Verification Matrix                              │ 2 new rows for tRPC router change and procedure rename                              │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 10 │ §10 Condensed Case Index                                      │ 2 new entries (TRPC-1, TRPC-2)                                                      │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 11 │ §12 Most Important Lessons — #11                              │ New lesson: "Build gate catches what type-check misses"                             │ 
├────┼───────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤ 
│ 12 │ §13 One-Page Agent Field Card — Line 16                       │ New line: "If tRPC build fails: check procedure names for JS reserved words"        │ 
└────┴───────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘ 
 
### Key Knowledge Captured 
 
Anti-pattern learned: 
- tRPC v11 rejects JavaScript reserved words (apply, call, bind, constructor, toString, valueOf, hasOwnProperty, __proto__) as procedure names at router construction time 
- This error only surfaces at pnpm build, not pnpm check-types, because the router constructor runs at module load (runtime), not during static type analysis 
- Generic procedure names (get, create, update, delete) are ambiguous in logs and error paths 
 
Pattern established: 
- Use domain-specific verb-noun pairs: submitApplication, listOrders, getProfile, createOrder, updateAddress, deleteItem 
- The tRPC procedure path is visible in network logs, error messages, and analytics — make it self-documenting 
 
Concept formalized: 
- "Construction-time validation failures" as a third category distinct from infrastructure failures and source-code debt 
- Framework contract violations that only surface at module load time (build/runtime), not during static analysis 
 
The skill document is now a comprehensive reference for the exact failure mode we just fixed, with diagnostic guidance, remediation steps, prevention patterns, and verification requirements for future agents.
