# Log

Append-only. One line per operation: `## [YYYY-MM-DD] op | title` where op is one of add, update, supersede, prune, handoff, index. Newest at the bottom. Never edited, only appended; this is the history the entries themselves do not carry.

## [2026-09-18] init | scaffolded
## [2026-09-18] add | decision: Relative markdown links and an index per folder, wikilinks only inside a vault
## [2026-09-18] add | decision: Two vaults: Ai directory and deckbuilder repo
## [2026-09-18] add | solution: Lint a markdown folder for Obsidian and GitHub without Obsidian running
## [2026-09-18] handoff | 16 lines
## [2026-09-18] index | rebuilt (3 entries)
## [2026-09-18] handoff | 16 lines
## [2026-09-18] index | rebuilt (3 entries)
## [2026-09-23] update | CLAUDE.md imports AGENTS.md with an @AGENTS.md line (Claude Code 2.1.277+ loads nothing from a prose pointer); .github/copilot-instructions.md kept as the Copilot pointer
## [2026-09-26] update | 0.1.1: SKILL.md description shortened from about 1,200 to 992 characters (spec cap 1,024), every trigger phrase kept (skill-tidy check OK); C-20260926-1; test_vault_lint and self-lint pass; installed copies in ~/.claude/skills and ~/.agents/skills refreshed by copy
## [2026-09-26] update | installed copies in ~/.claude/skills/obsidian-notes and ~/.agents/skills/obsidian-notes replaced by junctions to skills/obsidian-notes (diff showed no differences; old copies moved to a session scratchpad); skill-tidy scan lists it once, lint clean
## [2026-10-03] refresh | evergreen refresh, m 0.2, quiet: Obsidian 1.14.x Catalyst (outside-vault files, Bases kanban) and new wikilink-first linters noted as R-20261003-1 to -3; GitHub still no wikilinks; SKILL.md unchanged, skill stays parked; next due 2026-10-16
## [2026-10-03] update | prepared for the Claude plugin directory: README Privacy section (no network, no credentials), plugin.json documentationUrl, supportUrl and privacyPolicyUrl; checklist clean (34 files, none over 256 KiB, no binaries, validate passes)
## [2026-10-04] update | the plugin icon (icon.png in .claude-plugin) for the Claude directory, chosen from two Z-Image candidates. Z-Image Turbo bf16, 9 steps, cfg 1, res_multistep/simple, seed 3652960074, prompt "flat vector app icon, bold simple shapes, minimal, centered single motif, thick clean outlines, high contrast, readable at small size, no text, no letters, no numbers, no words, no logos, square composition, a single note page with a chain link symbol, white page and gold link on deep purple background"; white corners painted to the background (47, 15, 93)
## [2026-10-04] update | submitted to the Claude plugin directory, https://claude.ai/directory/manage/plugins/3cacb896-b02d-4989-a5d5-c71a3d264347 (validated master@fb83a87, Scheduled check only, auto-publish on); no holds; status after submit: scan passed, waiting for an Anthropic reviewer
## [2026-10-05] update | 0.2.1: root plugin.json for GitHub Copilot CLI and the awesome-copilot external-plugin listing (C-20261005-1); Copilot CLI 1.0.92 installs it, vally lint passes
## [2026-10-06] update | 0.3.0 (C-20261006-1): lint 5.2 s to 2.7 s on 3,124 files, --fix-index purpose clauses, --json honours --max (586 KB to 6.6 KB at --max 10), self-links no longer rescue orphans, SECURITY.md linked from README; tests/test_repo.py in CI and the release job; research pass with a forum sweep (R-20261006-1 to -3, m 0.4, next due 2026-10-20); eval action-1 1/1 (T-20261006-1)
## [2026-10-06] handoff | rewritten for 0.3.0 and the directory auto-publish check
