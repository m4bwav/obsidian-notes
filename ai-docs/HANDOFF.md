# Handoff

## Current state
Skill `obsidian-notes` 0.3.0 (2026-10-06, C-20261006-1) is public at https://github.com/m4bwav/obsidian-notes (MIT; CI runs on three operating systems; releases on `vX.Y.Z` tags). It is listed in the Claude plugin directory with auto-publish on: the scheduled check picks master up, so each merge to master is a deployment. `tests/test_repo.py` guards what that listing depends on (both plugin.json files agree, the description cap, the directory URLs, the icon).

0.3.0 made the lint about 2x faster (one walk, cached listings and resolves). `--fix-index` now writes a purpose clause on each line, `--json` honours `--max`, and a self-link no longer rescues an orphan. The research pass of 2026-10-06 included a forum sweep (R-20261006-1 to -3). Eval action-1 passed on evidence (T-20261006-1).

## In progress
Nothing open. trigger-1 has never run through the harness.

## Decisions made this session
See [INDEX.md](INDEX.md). 2026-10-06: SKILL.md now steers agents to the capped text report instead of `--json` (586 KB on a 3,000-file tree). The repo checks are a separate `tests/test_repo.py` so the skill zip stays the skill.

## Next single action
After the merge, check the directory listing (https://claude.ai/directory/manage/plugins/3cacb896-b02d-4989-a5d5-c71a3d264347) for when it shows 0.3.0, record the lag in log.md, and tag `v0.3.0`. Optional, from R-20261006-3: mirror the action cases in `claude plugin eval` format (`tool_used` input_match vault_lint.py, `file_exists` INDEX.md).

## Gotchas
`everlast.py note` truncates slugs at about 60 characters; write `Related:` links after the file exists, or check the printed path. Bash heredocs with `'EOF'` still need Python raw strings for `\m`-style Windows paths. Inline `python -c` with nested quotes fails in PowerShell; write a scratch .py file instead.
