# Tests: obsidian-notes

Test runs for [SKILL.md](SKILL.md). Cases live in `evals/evals.json`. A failure that taught something is a lesson in [LEARNINGS.md](LEARNINGS.md); a fix it caused is logged in [CHANGELOG.md](CHANGELOG.md) with `because: T-...`; research it triggered is in [RESEARCH.md](RESEARCH.md); counts and the failing list are in `evergreen.json` under `tests`. Rules: MAINTENANCE.md (testing section) and the plugin's `protocol/TESTING.md`.

A test passes on evidence (a tool call in the trace, a file, a marker, a log line), never on the transcript's claim that something was done.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`, then one line per failing case (`id · kind · class · what the evidence showed`), then `led to:` (L-, C-, R- ids or none). Newest first. Budget 150 lines; archive older runs to `TESTS-ARCHIVE.md`.

## Runs

### T-20261006-1 · 2026-10-06 · evergreen-tester (fresh context, one run, skill read from the working copy of C-20261006-1) · DESKTOP native Windows · 1/1
- action-1 · action · pass: the text report ran three times (before, `--fix-index`, after hand edits); no `--json`. The script's purpose clauses were in place and the runner rewrote them as "when to read it" lines, as Step 2 now asks. `check_vault.py --task index` exits 0. The reply gave before and after counts and left nope.md, the ambiguous `[[Beta]]` and the duplicate basename for the user. 12 tool calls.
- Script suites the same day: `test_vault_lint.py` (cases 12a to 12d added) and the new `tests/test_repo.py` pass.
- led to: none (C-20261006-1 kept)

### T-20261001-2 · 2026-10-01 · evergreen.py worth --ab --arm with --append (claude -p, sonnet, the trimmed SKILL.md of C-20261001-2) · DESKTOP native Windows · with 10/10, without 8/10 (baseline from T-20261001-1)
- Isolation: `--setting-sources project --no-session-persistence`; the owner's global CLAUDE.md loads in both arms (fair, not blind). The without arm is T-20261001-1's ten runs, unchanged because only the skill changed.
- action-3 5/5 with, outcome-2 5/5 with. Delta +20 points, inside the 25-point margin; cost x0.99 (was x1.24), turns x1.15 (was x1.33), time x0.87. Verdict UNPROVEN (no gain beyond noise at the same cost). Mean with-arm run $0.25, was $0.31. Results: Ai/skill-worth-study/runs/obsidian-notes/trimmed-2026-10-01.
- led to: C-20261001-2 kept (the trim holds the pass rate at no extra cost)

### T-20261001-1 · 2026-10-01 · evergreen.py worth --heavy (claude -p, sonnet; evergreen 0.13.0 branch) · DESKTOP native Windows · with 10/10, without 8/10
- Isolation: `--setting-sources project --no-session-persistence`; the owner's global CLAUDE.md loads in both arms (fair, not blind). The skill fired in all 10 with-arm runs and in no without-arm run.
- action-3 · action · without 4/5: one run wrote both indexes as wikilinks (`[[notes/README|Notes]]`), which the checker's relative-markdown-link rule fails and GitHub does not render.
- outcome-2 · outcome · without 4/5: one run left `[[gamma]]` unconverted and never named `nope.md`.
- Delta +20 points, inside the 25-point noise margin (5 runs per arm after the heavy top-up); cost x1.24, turns x1.33, time x0.87. Verdict CUT by the §8 thresholds (no gain beyond noise at 1.15x the cost or more). Cost $5.63 for 20 runs. Knowledge probe the same day: the skill-less answer named 7 of 28 anchors and would write wikilink indexes. Results: Ai/skill-worth-study/runs/obsidian-notes/heavy-2026-10-01.
- An earlier A/B the same day (ab-2026-10-01-action-3, $1.67) measured the harness, not the skill: a relative skill path gave `--plugin-dir .`, so the skill never loaded and writes were refused; evergreen-protocol L-030.
- led to: L-002, L-003, L-004, C-20261001-1, C-20261001-2

### T-20260918-1 · 2026-09-18 · evergreen-tester (fresh context, one run each) · DESKTOP · 4/4
- trigger-2 · trigger · obsidian-notes invoked (prompt named Obsidian, orphans, index).
- decoy-1 · trigger · everlast-capture invoked, not obsidian-notes. decoy-2 · trigger · graphify invoked, not obsidian-notes.
- action-1 · action · Bash ran `vault_lint.py` four times (report, `--fix-index`, report, report); `ls` showed `notes/INDEX.md` and `plans/INDEX.md`; reply gave before and after counts. The runner appended one line to README.md by hand so the new indexes were not orphans, which `--fix-index` now does itself.
- baseline (skill absent) · did the lint by reading files, found the ambiguous wikilink, wrote both indexes with markdown links, no script; competent but unverifiable and slower.
- Not run yet: trigger-1, outcome-1 (`--to-markdown-links` verified by hand on the fixture instead; outcome-1's evidence check was re-specified on 2026-09-18 because the fixture keeps one deliberately ambiguous wikilink).
- led to: C-20260918-2 (index files exempt from the duplicate check; new indexes linked from the parent index)
