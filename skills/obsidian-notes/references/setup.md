# Obsidian setup for agent-written markdown

Back to [SKILL.md](../SKILL.md). Sources and dates in [RESEARCH.md](../RESEARCH.md).

## Settings that make Obsidian write portable links

Settings > Files and links:

- `Use [[Wikilinks]]`: off. Obsidian then writes `[Note](path/Note.md)` when you link or drag a file, and still resolves existing wikilinks.
- "New link format": Relative path to file. "Shortest path when possible" drops the folder and breaks on rename when two files share a name (forum bug, January 2026).
- "Automatically update internal links": on.
- "Excluded files": build and cache folders (`Library/`, `Temp/`, `obj/`, `Logs/`, `Builds/`, `node_modules/`). Obsidian hides them in search, graph view and unlinked mentions, and only deprioritizes them in the quick switcher and link suggestions.
- "Show all file types" (older versions: "Detect all file extensions"; app.json `showUnsupportedFiles`): off, so a Unity or Node tree does not flood the file list.

`scripts/vault_lint.py <root> --vault-init` writes these into `.obsidian/app.json` (`useMarkdownLinks`, `newLinkFormat: relative`, `alwaysUpdateLinks`, `showUnsupportedFiles: false`, `userIgnoreFilters`).

## What to commit from `.obsidian/`

Commit `app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json`, `hotkeys.json`, `graph.json` so the vault behaves the same on every machine. Never commit `workspace.json`, `workspace-mobile.json`, `cache`, or a plugin's `data.json` (per-machine state, constant churn). The `--vault-init` command appends those ignore lines.

## Opening a code repo as a vault

"Open folder as vault" on the repo root gives one graph across `README.md`, `docs/`, `ai-docs/`, `CODEMAP.md`. Add the build folders to Excluded files first (above). Opening only `ai-docs/` as the vault is simpler but loses links to `docs/` and the README; a vault cannot span two sibling folders without their parent. Obsidian's roadmap lists "open individual markdown files outside vaults" as active work (2026), which may loosen this later.

## One vault or several

Community consensus (Obsidian forum thread 1445, 80+ posts) and the reason behind it: a vault is a link namespace. Split only when two trees have no sensible links between them, need different sync or privacy, or one is so large that indexing hurts. The cost of a split is no cross-links, no single search, no single graph, and plugin settings duplicated per vault. Folders plus tags inside one vault cover most "areas of life" cases.

For a set of separate repositories that should share one graph, either open their common parent (with ignores) or link each repo's docs into one vault folder with symlinks or junctions (the `obsidian-repo-mounts` pattern). Two copies of the same repo in one vault (a public clone beside a private fork) produce duplicate basenames; wikilinks become ambiguous there, markdown links do not.

## The official Obsidian CLI (since 1.12.4, February 2026)

Needs the 1.12.7 or newer installer (Settings > General shows the installer version; if the toggle was on before an update, turn it off and on again). Enable: Settings > General > Command line interface, then restart the terminal. Windows adds `Obsidian.com` to PATH from the install folder; macOS symlinks `/usr/local/bin/obsidian`; Linux copies a binary to `~/.local/bin/obsidian`. The CLI remote-controls a running Obsidian and launches it when closed; it is not headless. Obsidian Headless (open beta, `npm install -g obsidian-headless`, command `ob`, Node 22+) is a separate Sync client that runs without the app but only syncs a vault; use `vault_lint.py` for headless checks.

```
obsidian search query=<text> path=<folder> limit=<n>
obsidian read file=<name>
obsidian create name=<name> path=<folder> content=<text> [template=<name>] [overwrite]
obsidian append file=<name> content=<text> [inline]
obsidian links file=<name> [total]
obsidian backlinks file=<name> [counts] [format=json|tsv|csv]
obsidian tags [file=<name>] [counts] [sort=count]
obsidian property:set name=<n> value=<v> type=<t> file=<name>
obsidian vault=<name|id> <command>      # target a vault; must come first
```

Use it for questions Obsidian answers better than a script (its own link resolution, backlinks, tag counts, search across a live vault). Use `vault_lint.py` when Obsidian is closed, in CI, or on a folder that is not a vault.

## Agent integrations, ranked by real use (September 2026)

| Tool | What it is | When it is worth it |
|---|---|---|
| kepano/obsidian-skills (48k stars; obsidian-markdown, obsidian-cli, obsidian-bases, json-canvas, defuddle) | Official-author Agent Skills teaching the file grammars (Bases, JSON Canvas, callouts) | Not used by this skill: its obsidian-markdown skill prefers wikilinks and assumes a vault-only reader, the opposite of the relative-link rule here. Listed so you know it exists; nothing here depends on it |
| Obsidian CLI | Built into the app | Any live-vault question; free |
| Local REST API plugin (2.9k stars, v5 serves MCP at `https://127.0.0.1:27124/mcp/`) | HTTP and MCP access to a running vault | A long-running agent that edits the vault while Obsidian is open; the older mcp-obsidian bridge (4.4k stars, unmaintained since May 2026) wraps the same API |
| Claudian (15k stars) | Claude Code, Codex and others as a sidebar inside Obsidian, vault as cwd | Working on notes inside Obsidian rather than from a terminal; desktop only, Obsidian 1.13+ |
| Smart Connections (5k stars), Copilot for Obsidian (7k stars) | In-app related-note suggestions and chat | Human reading aid, not an agent tool |
| Karpathy "llm-wiki" pattern, breferrari/obsidian-mind, AgriciDaniel/claude-obsidian | Agent-maintained wiki with index notes, frontmatter, lint for dead links and orphans | The practice this skill follows; read for ideas, no need to install |

## Is the graph worth it

No measured study exists. Practitioner testimony converges on: the value is in lint catching inconsistencies and in backlinks surfacing forgotten context, not in the graph picture; keep raw sources immutable; keep agent scratch (plans, transcripts) out of the notes tree or in its own folder. One dissent (ssp.sh, "Keep AI out of your vault", updated September 2026): AI-written notes and auto-links dilute one's own thinking; it applies to a personal thinking vault, less to project documentation that agents write anyway.
