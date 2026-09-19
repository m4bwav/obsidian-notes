# Handoff

## Current state
Skill `obsidian-notes` 0.1.0 is public at https://github.com/m4bwav/obsidian-notes (MIT, CI on three operating systems, release on `vX.Y.Z` tags), published 2026-09-18 from a single scrubbed commit after a 35-agent review (privacy, code, docs; C-20260918-3 and C-20260918-4). The script's self-test has 61 checks; the repo's own markdown passes its lint with `--exclude fixtures`. First skill test run 4/4 (TESTS.md T-20260918-1). Evergreen Protocol 1.8 and Everlast Protocol 1.2 carry the linking rule.

## In progress
Nothing open. Eval cases trigger-1 and outcome-1 have not been run through the harness (outcome-1 was re-specified).

## Decisions made this session
See [INDEX.md](INDEX.md): relative markdown links plus an index per folder; two vaults; kepano/obsidian-skills named as context only, never installed (owner preference).

## Next single action
Watch the first CI run on the public repo (the Windows job exercises the cp1252 console path); then run the two unrun eval cases with `evergreen-test`.

## Gotchas
`everlast.py note` truncates slugs at about 60 characters; write `Related:` links after the file exists or check the printed path. Bash heredocs with `'EOF'` still need Python raw strings for `\m`-style Windows paths.
