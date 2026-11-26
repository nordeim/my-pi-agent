# Todos
[✓] Baseline offline verification: py_compile, hashes, --version, --self-test, reproduce v3.0 failure
[✓] Promote _2.py to canonical github_folder_downloader.py; preserve v3.0 as _v3.0.py
[✓] Surgically update SKILL.md file list and identity note (no guard/logic edits)
[✓] Re-verify documented commands against canonical script (help/self-test/version)
[✓] Live validation: dry-run then download mattpocock/skills .../skills/productivity into /Home1/project/audit/
[✓] Verify downloaded tree and deliver audit findings with evidence
Audit / validation complete.
Findings
- Critical (fixed): SKILL.md documented v3.1.0 but pointed at the v3.0 script (1266 lines); every documented command failed with exit 2. Promoted github_folder_downloader_2.py → canonical scripts/github_folder_downloader.py; v3.0 preserved as scripts/github_folder_downloader_v3.0.py.
- Identity drift (documented): q4 ledger claims 2121 lines / 94 305 B / SHA 957484af…; shipped script is 2123 / 94 351 / 2f2e4716…563d9de18a — recorded in SKILL.md:244. File list corrected at SKILL.md:246-255.
- New defect (triage only, no code edit per skill hard rule F209): bare tree/REF/PATH URLs fail. commit_for_ref (github_folder_downloader.py:740-752) treats only HTTP 404 as a missing ref; GitHub returns 422 for commits/main/skills/productivity, aborting the slash-split loop at :875-897. Fix proposal: treat 422 "No commit found for SHA" as a miss + add a self-test regression. Workaround: root URL with --ref main --path skills/productivity.
Validation evidence
- Offline: py_compile clean; --version → 3.1.0; --self-test → Ran 5 tests ... OK, exit 0; all 27 documented flags present; --path without --ref → 2; bad URL → 1 + URLParseError.
- Live dry-run: exit 0, 20 files / 14 dirs / 40 492 B, commit 6f7f7831a625….
- Live execute: exit 0, ok:true, tier:api, zero skipped symlinks/submodules and zero LFS pointers.
- Independent verification: all 20 files in /Home1/project/audit/ match GitHub's tree by path, size, and Git blob SHA-1 — INDEPENDENT_VERIFY=PASS.
No commits made; pre-existing working-tree changes were untouched.
