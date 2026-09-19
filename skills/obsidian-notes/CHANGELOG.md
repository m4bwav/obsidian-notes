# Changelog: obsidian-notes

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20260918-5 · 2026-09-18 · `--probe` finds the Windows shim beside the app and lists the registered vaults
- because: L-001 (the CLI worked by full path before the shell saw the new PATH)
- files: scripts/vault_lint.py (`probe`), SKILL.md §Step 5, LEARNINGS.md
- The CLI was exercised for the first time: `vaults`, `version`, `links ... total`, `backlinks`, `search`, `tags counts`, `read` all answered on a live vault.

### C-20260918-4 · 2026-09-18 · Pre-publication review: 22 script defects fixed, docs matched to the code and to Obsidian's help, self-test added; version 0.1.0 published at https://github.com/m4bwav/obsidian-notes
- because: a 35-agent review before the public release (privacy, code, docs; every code and docs finding confirmed by reproduction and by a "does it matter" judge); R-20260918-5
- files: scripts/vault_lint.py (rewritten: UTF-8-safe console output on Windows; markdown link targets checked for on-disk case, literal spaces and `<...>` destinations; reference-style links; folder links resolve to any index name; wikilink resolution shared by the lint and the converter, with a real suffix test instead of `rstrip(".md")`, escaped pipes, attachments and `[[#heading]]`; anchors percent-encoded; frontmatter never rewritten; CRLF and BOM preserved; fences tracked by length, also inside blockquotes; HTML comments ignored; `--fix-index` links each child once, walks up to the nearest index and links pass-through folders through the index below them; `--json` stays parseable with fixers; a missing root is exit 2; links leaving the root reported; `--ignore` names always written; gitignore compared by whole lines; probe paths from the environment; Python 3.9 compatible writes), scripts/test_vault_lint.py (61 checks, one per fixed defect), SKILL.md (facts paragraph, §Step 2 rules restated to match the code), references/setup.md (installer requirement, "Show all file types", excluded-files wording, Obsidian Headless), RESEARCH.md (R-20260918-5, open questions), evals/evals.json (outcome-1 evidence check made satisfiable), AGENTS.md (self-lint command excludes the fixture), README.md (install per tool, evergreen explained, license, Python version), ai-docs (local paths and project names removed before publishing), LICENSE, .claude-plugin, .github workflows
- Published from a single scrubbed commit, like the sibling public repos. The first CI run failed on Python 3.9 (the test helper used `Path.write_text(newline=)`, a 3.10 addition) and on Linux (a mis-cased link is missing there, so the report lacked the case note); links are now resolved component by component on every OS, and the suite runs under 3.9 locally as well.

### C-20260918-3 · 2026-09-18 · kepano/obsidian-skills is named as context only, never recommended or installed
- because: user request (the owner prefers relative markdown links to wikilinks and declined the wikilink-first skill set)
- files: SKILL.md (facts paragraph), README.md, references/setup.md (integrations table), RESEARCH.md §Current understanding and R-20260918-2
- The skill takes the opposite rule and depends on nothing from obsidian-skills.

### C-20260918-2 · 2026-09-18 · `--fix-index` links each new index from the parent index; index names exempt from the duplicate-basename check
- because: T-20260918-1 (the action run had to append a README line by hand so the new indexes were not orphans, and reported `INDEX.md x2` as a duplicate)
- files: scripts/vault_lint.py (`fix_index`, duplicate check), TESTS.md
- A generated everlast INDEX.md is never edited (it is rebuilt from frontmatter); any other parent index gets one `- [folder/](folder/INDEX.md)` line.

### C-20260918-1 · 2026-09-18 · Created as an evergreen unit: lint script, index writer, wikilink converter, vault init, CLI probe
- because: user request (Obsidian as the reader for AI-written markdown; a skill that reads and maintains Obsidian-compatible notes; decide one vault or several); R-20260918-1 to R-20260918-4
- files: SKILL.md (five steps; core action is `scripts/vault_lint.py` whose report is the evidence), scripts/vault_lint.py (checks: broken markdown links, broken and ambiguous wikilinks, duplicate basenames, orphans, folders without an index unless an ancestor index covers them, frontmatter; fixes: `--fix-index`, `--to-markdown-links`, `--vault-init`, `--probe`), references/setup.md (settings, gitignore, CLI reference, integrations ranked, one-vault-or-many), evals/evals.json (two triggers, two decoys, one action, one outcome; fixture under evals/fixtures/vault), RESEARCH.md, evergreen.json (tier `fast`, pointer mode)
- Design choice: relative markdown links are the rule and wikilinks the exception, the reverse of kepano/obsidian-skills, because the user's notes are also read on GitHub and by agents in VS Code (R-20260918-1, R-20260918-2). Tested on the fixture, on two everlast doc sets (no errors, no false index warnings) and on a 632-file tree (54 duplicate basenames from public/private repo pairs, which is why the vault rule in §Step 4 says markdown links only there).
