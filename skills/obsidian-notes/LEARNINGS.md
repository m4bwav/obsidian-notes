# Learnings: obsidian-notes

Procedural lessons for [SKILL.md](SKILL.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first (add / update / retire / none). Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

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
