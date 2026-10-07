# Research: obsidian-notes

Findings that back [SKILL.md](SKILL.md). Changes they caused are logged in [CHANGELOG.md](CHANGELOG.md); procedural lessons live in [LEARNINGS.md](LEARNINGS.md); test runs and their evidence in [TESTS.md](TESTS.md); schedule and state in `evergreen.json`. Protocol: [MAINTENANCE.md](MAINTENANCE.md). Setup detail for the user: [references/setup.md](references/setup.md).

Topic: Obsidian-compatible markdown for AI agents: link forms that work in Obsidian, GitHub and VS Code, index and map-of-content practice, the Obsidian CLI and agent integrations, vault layout. Tier `fast`. Last refresh 2026-10-06 (next due in `evergreen.json`).

## Current understanding

Settled (high confidence, primary sources 2026-09-18):

- Obsidian treats `[[Note]]` and `[Note](Note.md)` as equivalent and documents turning `Use [[Wikilinks]]` off "to improve interoperability"; markdown links must be URL-encoded with forward slashes. GitHub does not render wikilinks (community discussion 73062 closed unanswered with no staff reply, re-checked 2026-10-06). So relative markdown links are the only form that works in Obsidian, GitHub and VS Code at once. "Shortest path" link format drops folders on rename when basenames collide (forum bug, January 2026); "relative" avoids it.
- The official Obsidian CLI shipped in 1.12.4 (2026-02-27), enabled in Settings > General and needing the 1.12.7 or newer installer; it remote-controls a running app (launches it if closed, not headless) and exposes search, read, create, append, links, backlinks, tags, properties, plugins, eval, screenshots. Obsidian's help says it exists so "agentic coding tools" can test and debug.
- kepano/obsidian-skills (49.2k stars, MIT; seven skills since knap on 2026-09-10, about 388k installs on skills.sh) is the de-facto official agent skill set. Its obsidian-markdown skill says to use wikilinks inside a vault and markdown links only for external URLs, so it assumes a vault-only reader; it does not cover GitHub compatibility or duplicate basenames. This skill takes the opposite rule (relative markdown links, an index per folder) and does not install or depend on obsidian-skills; it is recorded here as the main wikilink-first alternative.
- Obsidian has no AI features on its roadmap (May 2026 plugin platform relaunch; roadmap.md). Its AI posture is "open formats plus skills".
- MCP access: the Local REST API plugin (2.9k stars) serves MCP itself since v5 (July 2026) at `https://127.0.0.1:27124/mcp/`; the mcp-obsidian bridge (4.4k stars) wraps the same API and has had no release since about May 2026. Claudian (15.4k stars, Obsidian 1.13+) embeds Claude Code and others inside Obsidian.
- Practice: Karpathy's llm-wiki gist (April 2026) and its implementations (obsidian-mind 4.6k stars, claude-obsidian) converge on agent-maintained index and map-of-content notes, frontmatter with date, status and tags, a lint pass for dead links and orphans, and immutable raw sources.
- Testing: headless linters exist (bborbe/obsidian-lint, vault-inspector, obsidian-broken-links-cleaner); the shared baseline is: every link resolves, no duplicate basenames, no orphans outside the index, frontmatter parses. No published eval suite for agent-written Obsidian notes was found; this skill's suite is its own.
- One vault or many (forum thread 1445): split only when two trees have no sensible cross-links, need separate sync or privacy, or one is huge; the cost is lost cross-links, search and graph plus duplicated settings. Repo subfolders opened as vaults work with obsidian-git.

Contested or moving: whether the graph itself helps a reader (no measurement either way; testimony says lint and backlinks help, the picture does not); the CLI's headless story; files outside the vault (1.14 public since 2026-10-05: opens a single outside file and registers Obsidian in the OS "Open with" menu, the file's own links resolve from its folder; links from vault notes to outside files are still not documented as followable, so the skill's "link outside the root" warning stands, R-20261006-1); relative links inside a moved note are not updated by Obsidian (forum 4386, R-20261006-2); Obsidian Community capability disclosures for plugins (announced, rolling out).

## Open questions

- Does any study measure backlinks or graph view improving comprehension of agent-written docs? None found 2026-09-18; re-check.
- Will the CLI gain a headless mode? Partly answered 2026-09-18 (R-20260918-5): Obsidian Headless is a separate open-beta Sync client for servers and agents, not a headless desktop CLI; the CLI still needs the app. Watch whether Headless gains read and search commands. 2026-10-03: no change found (R-20261003-1); carried forward.
- 1.14 is public (2026-10-05); can a vault note's markdown link to a file outside the vault be followed? The docs cover only links inside the outside file (R-20261006-1). Test by hand on an install.
- Will Obsidian fix the relative-link-on-move bug (forum 4386)? (R-20261006-2)
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
- Forum sweep: `site:forum.obsidian.md` for links breaking on move or rename, AI agents writing notes, the CLI; r/ObsidianMD is rarely indexed (2026-10-06), so search the forum first. Old bugs still open are the useful finds.

Testing (what proves the job was done):

- `obsidian lint broken links orphans cli <year>`; `vault linter frontmatter duplicate basenames`
- Evidence rule for this skill: a `vault_lint.py` call in the trace or a written `INDEX.md`; exit code 0 after the fix
- `site:code.claude.com plugin eval` (the `claude plugin eval` harness and its grader types)

## Findings

Newest first. Shape: `### R-YYYYMMDD-n · date · one line`, then `source:`, `track:`, `magnitude:` (major 0.6+ / real 0.3-0.5 / cosmetic under 0.3), `applied:`.

### R-20261006-1 · 2026-10-06 · Subject track: Obsidian 1.14 public (2026-10-05) opens outside markdown files; vault-to-outside links still undocumented
- source: https://obsidian.md/changelog/2026-10-05-desktop-v1.14.4/, https://obsidian.md/changelog/
- track: subject
- magnitude: real 0.3
- applied: C-20261006-1 (SKILL §Step 2 outside-root line, setup.md "Opening a code repo as a vault"). Links in an outside file resolve from its own folder; the quick switcher is always fuzzy; 1.14 needs the latest installer.

### R-20261006-2 · 2026-10-06 · Practice track (forum sweep): with relative paths, Obsidian does not update the links inside a note that moves
- source: https://forum.obsidian.md/t/broken-links-in-relative-path-mode-on-move-rename/4386?page=2 (open since 2022, last post 2026-04-02), https://forum.obsidian.md/t/links-break-when-moving-renaming-linked-files/106794
- track: practice
- magnitude: real 0.4
- applied: C-20261006-1 (SKILL §Step 2 "lint again after moves", setup.md warning and the Consistent Attachments and Links plugin, self-test case 12d). The forum sweep found no August to October 2026 threads on agents, the CLI or map-of-content practice; r/ObsidianMD and Discord were not indexed.

### R-20261006-3 · 2026-10-06 · Tooling and testing tracks: CLI `unresolved`, `orphans`, `deadends`; `claude plugin eval`; Local REST API 5.4.0
- source: https://obsidian.md/help/cli, https://code.claude.com/docs/en/plugin-evals.md, https://github.com/coddingtonbear/obsidian-local-rest-api/releases, https://github.com/kepano/obsidian-skills/commits/main, https://registry.modelcontextprotocol.io/v0/servers?search=obsidian
- track: tooling, testing
- magnitude: real 0.35
- applied: C-20261006-1 (setup.md CLI block: the three commands as a cross-check against Obsidian's own resolver, "follow the prompt to register"; Local REST API 5.4.0 blocks `.obsidian/` by default; obsidian-skills added knap, 49k stars). `claude plugin eval` (Claude Code 2.1.269+) runs cases from a plugin-root `evals/` folder with free `tool_used` and `file_exists` graders; this unit's action cases map onto it directly. Not adopted yet: the current harness is `evergreen.py worth`; mirror the cases when the next test run is due. New MCP or in-app agent tools (Qlaude, Vault Companion for Claude, obsidian-tc) are all wikilink-first. GitHub discussion 73062 is now closed unanswered. The Agent Skills description cap is still 1,024 characters (this one is about 990).

### R-20261003-3 · 2026-10-03 · Tooling, practice and testing tracks: more wikilink-first vault linters and agent bridges, nothing that does this skill's job for relative links
- source: https://community.obsidian.md/plugins/cairn-vault-linter, https://community.obsidian.md/plugins/vault-plus, https://skillselion.com/skills/agricidaniel/claude-obsidian/wiki-lint, https://skillselion.com/skills/ar9av/obsidian-wiki/wiki-lint, https://community.obsidian.md/plugins/blackglass, https://skillselion.com/skills/kepano/obsidian-skills/obsidian-cli
- track: tooling, practice, testing
- magnitude: cosmetic 0.1
- applied: none (note only). Cairn Vault Linter and Vault Plus are in-app plugins (broken links, headings, block IDs, orphans, duplicates); the wiki-lint skills (claude-obsidian, obsidian-wiki, nanowiki) are prose procedures over wikilinks in llm-wiki vaults. None checks GitHub rendering, on-disk case or relative markdown links, so `vault_lint.py` keeps its place. Blackglass embeds Claude Code in Obsidian with its own MCP server (like Claudian). kepano/obsidian-skills last updated 2026-09-10 (aggregator star counts disagree, 43.5k to 48.6k); still context only, by the owner's preference. Testing: no published eval suite for agent-written notes; nothing new.

### R-20261003-2 · 2026-10-03 · Subject track: GitHub still renders no wikilinks
- source: https://github.com/orgs/community/discussions/73062
- track: subject
- magnitude: none 0
- applied: none. Discussion open, no staff response, last comment 2026-08-13; the relative-markdown-link rule stands.

### R-20261003-1 · 2026-10-03 · Subject track: Obsidian 1.14.0 to 1.14.4 (Catalyst) add Bases kanban, opening files outside the vault, full-path search in sidebar views; public build still 1.13.x
- source: https://obsidian.md/changelog/, https://obsidian.md/changelog/2026-09-15-desktop-v1.14.2/
- track: subject
- magnitude: cosmetic 0.2
- applied: none (Current understanding, contested line). 1.14.2 opens a single outside file and registers Obsidian as an "Open with" handler for Markdown; 1.14.4 gives such files the outline and outgoing-links views. This partly answers the roadmap item recorded on 2026-09-18 but changes no link behaviour a vault relies on, and it is early access only. Re-check when 1.14 goes public whether vault links to outside files become followable (it would soften the "link outside the root" warning in SKILL §Step 2). No CLI or Headless change in the period.

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
