# Research: obsidian-notes

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md). Setup detail for the user: [references/setup.md](references/setup.md).

Topic: Obsidian-compatible markdown for AI agents: link forms that work in Obsidian, GitHub and VS Code, index and map-of-content practice, the Obsidian CLI and agent integrations, vault layout. Tier `fast`. Last refresh 2026-09-18; next due 2026-10-02.

## Current understanding

Settled (high confidence, primary sources 2026-09-18):

- Obsidian treats `[[Note]]` and `[Note](Note.md)` as equivalent and documents turning `Use [[Wikilinks]]` off "to improve interoperability"; markdown links must be URL-encoded with forward slashes. GitHub does not render wikilinks (community discussion 73062 still open). So relative markdown links are the only form that works in Obsidian, GitHub and VS Code at once. "Shortest path" link format drops folders on rename when basenames collide (forum bug, January 2026); "relative" avoids it.
- The official Obsidian CLI shipped in 1.12.4 (2026-02-27), enabled in Settings > General and needing the 1.12.7 or newer installer; it remote-controls a running app (launches it if closed, not headless) and exposes search, read, create, append, links, backlinks, tags, properties, plugins, eval, screenshots. Obsidian's help says it exists so "agentic coding tools" can test and debug.
- kepano/obsidian-skills (48.6k stars, MIT; six skills, about 375k installs on skills.sh) is the de-facto official agent skill set. Its obsidian-markdown skill says to use wikilinks inside a vault and markdown links only for external URLs, so it assumes a vault-only reader; it does not cover GitHub compatibility or duplicate basenames. This skill takes the opposite rule (relative markdown links, an index per folder) and does not install or depend on obsidian-skills; it is recorded here as the main wikilink-first alternative.
- Obsidian has no AI features on its roadmap (May 2026 plugin platform relaunch; roadmap.md). Its AI posture is "open formats plus skills".
- MCP access: the Local REST API plugin (2.9k stars) serves MCP itself since v5 (July 2026) at `https://127.0.0.1:27124/mcp/`; the mcp-obsidian bridge (4.4k stars) wraps the same API and has had no release since about May 2026. Claudian (15.4k stars, Obsidian 1.13+) embeds Claude Code and others inside Obsidian.
- Practice: Karpathy's llm-wiki gist (April 2026) and its implementations (obsidian-mind 4.6k stars, claude-obsidian) converge on agent-maintained index and map-of-content notes, frontmatter with date, status and tags, a lint pass for dead links and orphans, and immutable raw sources.
- Testing: headless linters exist (bborbe/obsidian-lint, vault-inspector, obsidian-broken-links-cleaner); the shared baseline is: every link resolves, no duplicate basenames, no orphans outside the index, frontmatter parses. No published eval suite for agent-written Obsidian notes was found; this skill's suite is its own.
- One vault or many (forum thread 1445): split only when two trees have no sensible cross-links, need separate sync or privacy, or one is huge; the cost is lost cross-links, search and graph plus duplicated settings. Repo subfolders opened as vaults work with obsidian-git.

Contested or moving: whether the graph itself helps a reader (no measurement either way; testimony says lint and backlinks help, the picture does not); the CLI's headless story (roadmap item "open individual markdown files outside vaults" is active); Obsidian Community capability disclosures for plugins (announced, rolling out).

## Open questions

- Does any study measure backlinks or graph view improving comprehension of agent-written docs? None found 2026-09-18; re-check.
- Will the CLI gain a headless mode? Partly answered 2026-09-18 (R-20260918-5): Obsidian Headless is a separate open-beta Sync client for servers and agents, not a headless desktop CLI; the CLI still needs the app. Watch whether Headless gains read and search commands.
- Does the `obsidian` shim land on PATH on Windows without a terminal restart, and what is its exact executable name (`Obsidian.com`)? Verify on a Windows install once the CLI is enabled.

## Search plan

Four tracks; every refresh runs at least one query on each (scope each to the period since the last refresh; add the year). Protocol §4 explains the tracks and how tooling, practice and testing findings are judged.

Subject (the goal and the latest thinking on reaching it):

- `site:obsidian.md/changelog <year>` and `site:obsidian.md/help cli` (CLI commands, link settings, roadmap)
- `obsidian "use markdown links" OR "wikilinks" interoperability github <year>` and `github.com/orgs/community/discussions/73062`
- `obsidian "one vault" OR "multiple vaults" <year> forum`
- `obsidian bases OR "json canvas" changelog <year>`

Tooling (skills, plugins, MCP servers, scripts, knowledge graphs built for this subject):

- `path:SKILL.md obsidian` on GitHub code search sorted by recently updated; `npx skills find obsidian`; skills.sh install counts for kepano/obsidian-skills (weekly, not all-time)
- `https://registry.modelcontextprotocol.io/v0/servers?search=obsidian`; `obsidian mcp server site:github.com <year>` (Local REST API plugin releases, mcp-obsidian, Claudian)
- Practitioner test on each candidate: commit in the last 90 days, issues answered, author has other work in the area, ships evals
- Provenance tiebreaker: prefer skills written by the latest frontier models at their highest reasoning setting when stated

Practice (how people use agents on this goal):

- `"claude code" obsidian vault workflow <year>`; `karpathy llm-wiki obsidian`; `obsidian "map of content" agent <year>`
- `"keep AI out of" obsidian` (the dissent, for balance)

Testing (what proves the job was done):

- `obsidian lint broken links orphans cli <year>`; `vault linter frontmatter duplicate basenames`
- Evidence rule for this skill: a `vault_lint.py` call in the trace or a written `INDEX.md`; exit code 0 after the fix

## Findings

Newest first. Shape: `### R-YYYYMMDD-n · date · one line`, then `source:`, `track:`, `magnitude:` (major 0.6+ / real 0.3-0.5 / cosmetic under 0.3), `applied:`.

### R-20260918-5 · 2026-09-18 · Subject track: the CLI needs the 1.12.7+ installer; Obsidian Headless (open beta) is a Sync client, not a headless CLI; the setting is now "Show all file types"; excluded files are hidden in search and graph but only deprioritized in link suggestions
- source: https://obsidian.md/help/cli, https://obsidian.md/help/headless, https://obsidian.md/help/settings
- track: subject
- magnitude: cosmetic 0.2
- applied: C-20260918-4 (SKILL facts paragraph and §Step 5; setup.md settings, CLI and Headless notes)

### R-20260918-4 · 2026-09-18 · Testing track: headless vault linters agree on four checks; no eval suite for agent-written notes exists
- source: https://github.com/bborbe/obsidian-lint, https://github.com/rogerdigital/vault-inspector, https://atskills.one/laurigates/vault-wikilinks
- track: testing
- magnitude: real 0.4
- applied: C-20260918-1 (`scripts/vault_lint.py` implements the four checks plus folders-without-index; evals use its trace and files as evidence)

### R-20260918-3 · 2026-09-18 · Practice track: llm-wiki pattern (index notes, frontmatter, lint) is the converged practice; one dissent says keep AI out of a personal thinking vault
- source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f, https://github.com/breferrari/obsidian-mind, https://github.com/AgriciDaniel/claude-obsidian, https://www.ssp.sh/brain/using-obsidian-with-ai/, https://forum.obsidian.md/t/one-vault-vs-multiple-vaults/1445
- track: practice
- magnitude: real 0.5
- applied: C-20260918-1 (SKILL §Step 3 and §Step 4; setup.md §One vault or several, §Is the graph worth it)

### R-20260918-2 · 2026-09-18 · Tooling track: kepano/obsidian-skills is the official-author skill set (wikilink-first); Local REST API v5 serves MCP itself; Claudian embeds Claude Code in Obsidian
- source: https://github.com/kepano/obsidian-skills, https://skills.sh/kepano/obsidian-skills, https://github.com/coddingtonbear/obsidian-local-rest-api, https://github.com/MarkusPfundstein/mcp-obsidian, https://github.com/YishenTu/claudian
- track: tooling
- magnitude: major 0.6
- applied: C-20260918-1, C-20260918-3 (SKILL takes the reverse rule, relative markdown links, and names obsidian-skills only as the wikilink-first alternative; setup.md ranks the integrations)

### R-20260918-1 · 2026-09-18 · Subject track: official CLI since 1.12.4; markdown links and wikilinks equivalent in Obsidian; GitHub still has no wikilinks; "shortest path" breaks on rename with duplicate basenames
- source: https://obsidian.md/help/cli, https://obsidian.md/changelog/2026-02-27-desktop-v1.12.4/, https://obsidian.md/help/links, https://github.com/orgs/community/discussions/73062, https://forum.obsidian.md/t/renaming-file-removes-path-from-links-to-it-when-new-link-format-is-shortest/106794, https://obsidian.md/blog/future-of-plugins/, https://obsidian.md/roadmap/
- track: subject
- magnitude: major 0.6
- applied: C-20260918-1 (SKILL facts paragraph, §Step 5; `--vault-init` writes markdown links and relative format)
