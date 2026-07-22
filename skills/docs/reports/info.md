Based on my meticulous review, I can provide a comprehensive security analysis:
---
Security Analysis: CRITICAL Skills Review
1. memory skill
| Aspect | Finding |
|--------|---------|
| Purpose | Memory persistence system for AI agents |
| Scripts | capture.py, recall.py, consolidate.py |
| Network Calls | None |
| External APIs | None |
| Data Exfiltration | None |
| Prompt Injection | None |
| Verdict | ✅ LEGITIMATE - False positive |
The "sensitive_file_access" findings are intentional - this skill IS a memory storage system that reads/writes MEMORY.md files by design.
---
2. memory-complete skill
| Aspect | Finding |
|--------|---------|
| Purpose | Same as memory (variant) |
| Verdict | ✅ LEGITIMATE - Same analysis as above |
---
3. memory-maintenance skill
| Aspect | Finding |
|--------|---------|
| Purpose | AI-powered memory maintenance using Gemini API |
| Scripts | review.sh, apply.sh, cleanup.sh |
| External API | Gemini (user's own API key) |
| Data Flow | Local memory files → Gemini for analysis → Local storage |
| Prompt Injection | None detected |
| Verdict | ✅ LEGITIMATE - False positive |
The skill sends user's own data to their own Gemini API for analysis. No malicious prompt injection detected.
---
4. daily-news skill
| Aspect | Finding |
|--------|---------|
| Purpose | Fetch news from Baidu/Google Trends |
| Network | Public websites only (Baidu, Google Trends) |
| CVE Found | PYSEC-2018-28 (requests SSL vulnerability) |
| Malicious Code | None |
| Data Exfiltration | None |
| Verdict | ✅ LEGITIMATE - Has dependency vulnerability, NOT malicious |
This is a dependency vulnerability not malicious code. The requests library needs updating.
---
5. solobuddy skill
| Aspect | Finding |
|--------|---------|
| Purpose | Build-in-public companion for indie hackers |
| HIGH Finding | "Shell config access" at twitter-monitor.md:138 |
| Actual Code | Documentation text: → Update AUTH_TOKEN/CT0 in ~/.zshrc |
| Executable Code | None that accesses ~/.zshrc |
| Prompt Injection | None |
| Verdict | ✅ LEGITIMATE - False positive |
The "HIGH" finding is in documentation, telling users how to configure their credentials. No code accesses shell configs.
---
Final Assessment
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   🟢 ALL 5 CRITICAL SKILLS ARE LEGITIMATE                       │
│                                                                 │
│   • No malicious code detected                                  │
│   • No prompt injection attacks                                  │
│   • No data exfiltration                                        │
│   • No credential theft                                         │
│                                                                 │
│   HIGH findings = False positives from intentional designs:     │
│   • Memory skills: Designed to access MEMORY.md                 │
│   • daily-news: Dependency CVE (fixable)                        │
│   • solobuddy: Documentation reference, not code                │
│                                                                 │
│   RECOMMENDATION: DO NOT DELETE any skills                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
No skills will be deleted. All CRITICAL findings are false positives or fixable dependency issues
