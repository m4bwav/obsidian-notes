# Learnings: obsidian-notes

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first (add / update / retire / none). Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-010 · 2026-10-13 · In a remote session the script is not on the user's machine; copy it to a scratch folder there and poll long runs (`remote-session-copy-and-poll`)
- Trigger: Claude Desktop marketplace test, 2026-10-13: the chat ran in a cloud sandbox linked to the PC through Desktop Commander. The agent had to gzip and base64 `vault_lint.py`, decode it into `%TEMP%\obsidian-notes\` on the PC and check its sha256; then a foreground run on a 6,442-file tree passed the device's 60 s reply timeout and was rerun with `Start-Process -Wait` and output to a file
- Hypothesis: the skill assumed the script and the notes share a filesystem, which is false for Desktop-with-linked-computer and Cowork sessions
- Rule: SKILL.md Step 1 "Remote or cloud sessions": copy to a scratch folder on the device (never the user's folders), verify the sha256, start large runs in the background with output to a file and poll
- Evidence: C-20261013-1
- Scope: env:remote-device
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-13

### L-009 · 2026-10-13 · A cp1252 console garbles titles; the script writes UTF-8 itself (`utf8-stdout-on-windows`)
- Trigger: Claude Desktop marketplace test, 2026-10-13: H1 titles with em dashes read through PowerShell came out as mojibake; the script's own `errors="backslashreplace"` kept it from crashing but printed escapes
- Hypothesis: Windows consoles and pipes default to the ANSI code page, so any non-ASCII title or path is lost unless the script picks the encoding
- Rule: `main()` reconfigures stdout and stderr to UTF-8 (`errors="replace"`); every read and write names UTF-8; the test forces `PYTHONIOENCODING=cp1252` and expects the em dash back
- Evidence: C-20261013-1; test 13e
- Scope: env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-13

### L-008 · 2026-10-13 · "One index at the root" is a common ask the per-folder writer cannot serve (`root-only-index`)
- Trigger: Claude Desktop marketplace test, 2026-10-13: the user asked for one INDEX.md at `D:\m4bwa` only; `--fix-index` writes into every folder (687 here), so the agent wrote the root index by hand, linking each top folder's README by H1 title and listing folders without one as plain text with counts
- Hypothesis: on a big personal tree people want an entry point, not hundreds of generated files
- Rule: `--root-index [--group PATH ...]` writes `<root>/INDEX.md` alone (frontmatter, one line per folder, never over an existing one); offer it whenever the root is large or personal
- Evidence: C-20261013-1; test 13d; the hand-written reference at the user's profile root
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-13

### L-007 · 2026-10-13 · Nothing stopped a bulk fix on a whole user profile (`guard-home-folder`)
- Trigger: Claude Desktop marketplace test, 2026-10-13: the root named was the user's whole Windows profile (6,442 markdown files); the skill gave no warning and `--fix-index` would have written INDEX.md into hundreds of folders under tool caches and backups
- Hypothesis: the skill was written for vaults and repos; a profile root looks like any other folder to the script
- Rule: the script refuses `--fix-index` and `--to-markdown-links` on a profile (NTUSER.DAT, USERPROFILE, HOME) or a tree over 1,000 markdown files unless `--yes`, printing what it would touch (exit 3); SKILL.md Step 1 says ask for a subfolder first
- Evidence: C-20261013-1; test 13c
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-13

### L-006 · 2026-10-13 · Never walk AppData unless the user approves (`skip-appdata-by-default`)
- Trigger: Claude Desktop marketplace test, 2026-10-13: the scan of a profile had to be given `--exclude AppData "Application Data" "Local Settings"` by hand; the owner's standing rule is that AppData is not indexed without approval
- Hypothesis: profile data folders hold app and tool caches, never notes, and are large enough to dominate the run
- Rule: the three names are skipped at any depth by default; `--include-appdata` walks them, only after the user says yes
- Evidence: C-20261013-1; test 13b
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-13

### L-005 · 2026-10-13 · One unreadable file ended the whole lint (`unreadable-file-not-fatal`)
- Trigger: Claude Desktop marketplace test, 2026-10-13: `PermissionError: [Errno 13]` on one SKILL.md under a scheduled-task folder, raised from `read()` inside `scan()`, killed the run on 6,442 files
- Hypothesis: real trees hold files locked by running apps or with denied ACLs; the lint read every file with no guard
- Rule: `scan()` catches `OSError` per file (and per folder in the walk), keeps going, and reports "unreadable files N" with paths in the text report and `--json` (cut by `--max`)
- Evidence: C-20261013-1; test 13a (denies read with icacls on Windows, chmod 0 elsewhere)
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-13

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
