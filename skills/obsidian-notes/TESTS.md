# Tests: obsidian-notes

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20260918-1 · 2026-09-18 · evergreen-tester (fresh context, one run each) · DESKTOP · 4/4
- trigger-2 · trigger · obsidian-notes invoked (prompt named Obsidian, orphans, index).
- decoy-1 · trigger · everlast-capture invoked, not obsidian-notes. decoy-2 · trigger · graphify invoked, not obsidian-notes.
- action-1 · action · Bash ran `vault_lint.py` four times (report, `--fix-index`, report, report); `ls` showed `notes/INDEX.md` and `plans/INDEX.md`; reply gave before and after counts. The runner appended one line to README.md by hand so the new indexes were not orphans, which `--fix-index` now does itself.
- baseline (skill absent) · did the lint by reading files, found the ambiguous wikilink, wrote both indexes with markdown links, no script; competent but unverifiable and slower.
- Not run yet: trigger-1, outcome-1 (`--to-markdown-links` verified by hand on the fixture instead; outcome-1's evidence check was re-specified on 2026-09-18 because the fixture keeps one deliberately ambiguous wikilink).
- led to: C-20260918-2 (index files exempt from the duplicate check; new indexes linked from the parent index)
