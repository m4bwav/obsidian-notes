# obsidian-notes

An Agent Skill that makes AI-written markdown navigable for people in Obsidian and for later agents, while it still renders on GitHub and in VS Code: an index per folder, explicit `Related:` links, relative markdown links instead of wikilinks, a lint that finds broken, mis-cased and ambiguous links, orphans, duplicate basenames and malformed frontmatter, one command to set a folder up as a vault, and the official Obsidian CLI when it is enabled. Built 2026-09-18 from the research in [skills/obsidian-notes/RESEARCH.md](skills/obsidian-notes/RESEARCH.md).

The rule it enforces, and why: Obsidian resolves `[Note](path/Note.md)` and `[[Note]]` identically and can be set to write markdown links; GitHub, VS Code and most agents render only markdown links; and relative links are path-based, so two files with the same name never collide. Wikilinks are the exception, for a vault nobody reads anywhere else.

## Layout

- [skills/obsidian-notes/](skills/obsidian-notes/SKILL.md): the skill (SKILL.md, `scripts/vault_lint.py` and its self-test, [references/setup.md](skills/obsidian-notes/references/setup.md), the evergreen companions, `evals/`).
- [ai-docs/](ai-docs/INDEX.md): what building it taught (an everlast doc set; layout in [ai-docs/README.md](ai-docs/README.md)).
- [AGENTS.md](AGENTS.md): rules for agents working in this repo; [CLAUDE.md](CLAUDE.md) and `.github/copilot-instructions.md` point at it.

The skill is an evergreen unit under the [evergreen protocol](https://github.com/m4bwav/evergreen-protocol): on a schedule it re-checks its sources (Obsidian help and changelog, the agent-integration landscape), logs findings in RESEARCH.md and edits in CHANGELOG.md, keeps lessons in LEARNINGS.md, and carries an eval suite (`evals/`, TESTS.md). The plugin is optional; without it the skill still works and MAINTENANCE.md says how to refresh by hand.

## Quick use

```
python skills/obsidian-notes/scripts/vault_lint.py <folder>                    # report (exit 1 on errors)
python skills/obsidian-notes/scripts/vault_lint.py <folder> --fix-index        # write missing INDEX.md files and link them from above
python skills/obsidian-notes/scripts/vault_lint.py <folder> --to-markdown-links
python skills/obsidian-notes/scripts/vault_lint.py <folder> --vault-init --ignore Library Temp   # only folders that exist are auto-detected; --ignore names are always written
python skills/obsidian-notes/scripts/vault_lint.py --probe                     # is the obsidian CLI on PATH
python skills/obsidian-notes/scripts/test_vault_lint.py                        # the script's own suite
```

Standard-library Python 3.9 or newer (`python` on Windows, `python3` on macOS and Linux); nothing to pip install. Obsidian does not need to be installed or running for the lint.

## Install

Clone the repo, then put `skills/obsidian-notes` where your agent looks for skills (a symlink or junction keeps it updatable with `git pull`):

- Claude Code: `~/.claude/skills/obsidian-notes` (every project) or `<repo>/.claude/skills/obsidian-notes` (one project); or add this repo as a marketplace (`/plugin marketplace add m4bwav/obsidian-notes`, then `/plugin install obsidian-notes@obsidian-notes`).
- GitHub Copilot CLI and VS Code Copilot: `~/.agents/skills/obsidian-notes` or `<repo>/.github/skills/obsidian-notes`.
- Cursor: `<repo>/.cursor/skills/obsidian-notes`. Codex, OpenCode, Windsurf: `~/.agents/skills/obsidian-notes`.

Then ask in a session, for example "lint my docs folder for Obsidian" or "make an index for these notes". Releases on the Releases page ship the skill folder as a zip.

## Versioning

Semantic version in `.claude-plugin/plugin.json`; every change is logged with its reason in [skills/obsidian-notes/CHANGELOG.md](skills/obsidian-notes/CHANGELOG.md). Tags on the repo match the plugin version. License: MIT.
