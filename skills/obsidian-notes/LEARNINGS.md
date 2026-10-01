# Learnings: obsidian-notes

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first (add / update / retire / none). Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-004 · 2026-10-01 · Without the skill the model already lints and indexes competently; what it misses is portable links and full conversion (`baseline-knows-lint-misses-portable-links`)
- Trigger: the worth study of 2026-10-01 (T-20261001-1): with no skill, sonnet passed the result checker 8 of 10 times on action-3 and outcome-2. Unprompted it found the broken `nope.md`, named the ambiguous `[[Beta]]` instead of guessing, linked the orphan and wrote both folder indexes (the knowledge probe said the same in prose). Its two failures were the two things the skill's rules and script exist for: indexes written as wikilinks (`[[notes/README|Notes]]`), which GitHub does not render, in 2 of 6 action-3 baseline runs counted by hand across both A/Bs; and a conversion that left `[[gamma]]` unconverted and never mentioned `nope.md`
- Hypothesis: lint-and-index is general markdown practice; the choice of link form is a convention the model resolves toward Obsidian's default (wikilinks) when the folder looks like a vault, and a hand conversion misses links a script would not
- Rule: keep the relative-markdown-link rule and the script's `--to-markdown-links` and `--fix-index` in the body; general lint advice (find broken links, list orphans, do not guess ambiguous links) is already known and is the first thing to cut
- Evidence: T-20261001-1; Ai/skill-worth-study/runs/obsidian-notes (owner's study folder: probe answer, transcripts, aggregate-result.json)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-01

### L-003 · 2026-10-01 · The fix flags print the after-report; a separate re-run of the lint is a wasted turn (`fix-flags-print-after-report`)
- Trigger: in the 2026-10-01 A/B the with-skill runs took 1.33 times the baseline's turns; the SKILL.md told them to run `VL <root>` again after fixing, though `--fix-index` and `--to-markdown-links` already end with the full report, and the two flags combine in one call
- Hypothesis: the step was written before the fix modes reported, and nobody compared the trace against the script's output
- Rule: one call, `VL <root> --fix-index --to-markdown-links` when both are wanted; its report is the after count; re-run only after hand edits
- Evidence: C-20261001-2; `vault_lint.py` main (the fix branches fall through to `report`)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-01

### L-002 · 2026-10-01 · On Windows call the script with `python`, also from Git Bash; `python3` there may be a Store stub (`windows-python-not-python3`)
- Trigger: one with-skill A/B run on 2026-10-01 (action-3-with-2 in the heavy run) read "`python3` on macOS and Linux" from SKILL.md but was in Git Bash, ran `python3`, which failed, then spent 13 turns (`which`, `where`, `Get-Command`, `find`, PATH dumps) before `py` worked
- Hypothesis: Git Bash looks like Linux to the model, so it took the Linux branch of the instruction
- Rule: the `VL` line says `python` on Windows, Git Bash and PowerShell alike
- Evidence: C-20261001-2; transcript action-3-with-2.jsonl in the study's heavy-2026-10-01 folder
- Scope: env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-01

### L-001 · 2026-09-18 · On Windows the CLI toggle adds the install folder to the user PATH; shells opened earlier must call `Obsidian.com` by full path
- Trigger: after the user enabled the CLI, `--probe` still reported `cli_on_path: null` in the running session while `Obsidian.com` existed in `<install folder>` and the user PATH already listed that folder.
- Hypothesis: the toggle edits the persistent user PATH; an existing shell keeps the PATH it started with.
- Rule: the probe reports `cli_shim` (the shim's full path) and runs `version` and `vaults` through it; `vault=<name>` takes the vault's display name and file arguments are vault-relative `path=`.
- Evidence: `Obsidian.com version` printed `1.13.7 (installer 1.13.7)`; `vaults` listed both vaults; `links path=README.md total` printed 33, the same count the lint found. Confirmed 2026-09-18.
- Scope: env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-18

<!-- Example (delete once you have a real entry):
### L-001 · 2026-09-18 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20260918-1, T-20260918-1, confirmed 2026-09-18
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-09-18
-->
