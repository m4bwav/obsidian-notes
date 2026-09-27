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
