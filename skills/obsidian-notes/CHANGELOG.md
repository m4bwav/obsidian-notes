# Changelog: obsidian-notes

Every change to [SKILL.md](SKILL.md) and its companions, newest first, each with the reason. Reasons cite findings in [RESEARCH.md](RESEARCH.md) (`R-`), lessons in [LEARNINGS.md](LEARNINGS.md) (`L-`), and test runs in [TESTS.md](TESTS.md) (`T-`). State in `evergreen.json`. Protocol: MAINTENANCE.md.

Entry shape: `### C-YYYYMMDD-n · date · one-line summary`, then `because:` (IDs or "user request"), `files:` (file and section), and a sentence on what changed. Cite section headings, not line numbers.

### C-20261005-1 · 2026-10-05 · Root plugin.json for GitHub Copilot CLI and awesome-copilot; version 0.2.1
- because: user request (list the plugin in github/awesome-copilot, whose intake gates never read `.claude-plugin/`)
- files: ../../plugin.json (new), .claude-plugin/plugin.json (0.2.1)
- The skill is unchanged. Copilot CLI 1.0.92 installs it from the root manifest and `vally lint` passes; the release tag v0.2.1 is the ref awesome-copilot pins.

### C-20261001-2 · 2026-10-01 · Body trimmed 26 percent with no loss on the A/B; `python` on Windows; one combined fix call; version 0.2.0
- because: the owner's request (update the tested skill with every token saving found); T-20261001-1 (cost x1.24 for a gain inside the noise), L-002, L-003, L-004; T-20261001-2 (the trimmed skill: 10/10, cost x0.99)
- files: SKILL.md (intro: the facts paragraph cut to the link-form rule and a pointer to RESEARCH.md and references/setup.md; the `VL` line; Step 1 cut to two sentences; Step 2 keeps the judgement per finding and points at `VL --help` for the rules the script applies; Steps 4 and 5 merged into one short step pointing at references/setup.md, which already held the vault-split reasoning, the CLI and the integrations), .claude-plugin/plugin.json (0.2.0)
- Body about 2,633 to 2,003 estimated tokens. The description is unchanged, so triggering is unchanged.

### C-20261001-1 · 2026-10-01 · Value cases graded on the result: action-3, outcome-2 and `evals/check_vault.py`; outcome-1 retired
- because: the skill worth study (action-1 passes only through `vault_lint.py`, and outcome-1's pseudo-code check cannot run under `evergreen.py worth --ab`); T-20261001-1
- files: evals/evals.json (action-3, outcome-2 with answer regexes, dated baselines; outcome-1 removed), evals/check_vault.py (new: grades the fixture's end state for the index and convert tasks, `--loose` for any resolving link; proven on hand-made right and wrong copies and on the script's own output)
- A run without the skill can now pass by producing the right vault, so a gain means a better result, not the skill's route.

### C-20260926-1 · 2026-09-26 · Description shortened to 992 characters (was about 1,200, over the 1,024 spec cap); version 0.1.1
- because: user request (the description exceeded the Agent Skills spec's 1,024-character limit, which some hosts enforce by dropping the skill)
- files: SKILL.md front matter `description`, .claude-plugin/plugin.json (0.1.1)
- Every quoted trigger phrase and every capability is kept; the CLI subcommand list and the vault setup details moved out of the description (they are in the body). The key use case now comes first.

### C-20260918-6 · 2026-09-18 · Step 3 follows Evergreen Protocol 1.9: index lines carry a purpose clause, an index stays under about 200 lines, a link back to the index is optional
- because: user request (indexes as a net positive for agents and people, back-links only where they earn their place) and the research logged as evergreen-protocol:R-20260918-2 (on-demand maps help, always-on overviews do not, bare-path index lines are a measured smell)
- files: SKILL.md §Step 3
- `--fix-index` still writes title-only lines; adding the first sentence of each file as the purpose clause is the next script change.

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
