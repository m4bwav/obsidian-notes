# Handoff

## Current state
Skill `obsidian-notes` 0.4.0 (2026-10-13, C-20261013-1) is on branch `fix/2026-10-13-desktop-test-gaps`, PR open for the owner. Master is 0.3.0 and is public at https://github.com/m4bwav/obsidian-notes (MIT; CI on three operating systems; releases on `vX.Y.Z` tags). It is listed in the Claude plugin directory with auto-publish on: the scheduled check picks master up, so merging the PR deploys 0.4.0. `tests/test_repo.py` guards what that listing depends on.

0.4.0 fixes what the Claude Desktop marketplace test of 2026-10-13 hit on a whole user profile: a PermissionError traceback (unreadable files are now a warning), AppData walked (skipped by default, `--include-appdata`), no guard on bulk fixes (refused on a profile or >1,000 md files without `--yes`, exit 3), no root-only index (`--root-index [--group ...]`), mojibake on a cp1252 console (UTF-8 stdout), and no instructions for a remote session (SKILL.md Step 1).

## In progress
PR for 0.4.0 waits for the owner's merge. trigger-1 has never run through the harness.

## Decisions made this session
See [INDEX.md](INDEX.md). 2026-10-06: SKILL.md now steers agents to the capped text report instead of `--json` (586 KB on a 3,000-file tree). The repo checks are a separate `tests/test_repo.py` so the skill zip stays the skill.

## Next single action
After the owner merges the 0.4.0 PR, check the directory listing (https://claude.ai/directory/manage/plugins/3cacb896-b02d-4989-a5d5-c71a3d264347) for when it shows 0.4.0, record the lag in log.md, and tag `v0.4.0` with the owner's go-ahead. Then update the marketplace install in Claude Desktop and rerun the profile test (expect a stop-and-ask in Step 1). Optional, from R-20261006-3: mirror the action cases in `claude plugin eval` format (`tool_used` input_match vault_lint.py, `file_exists` INDEX.md).

## Gotchas
`everlast.py note` truncates slugs at about 60 characters; write `Related:` links after the file exists, or check the printed path. Bash heredocs with `'EOF'` still need Python raw strings for `\m`-style Windows paths. Inline `python -c` with nested quotes fails in PowerShell; write a scratch .py file instead.
