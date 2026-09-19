---
name: obsidian-notes
description: Reads, writes and maintains markdown so it works as an Obsidian vault and still renders on GitHub and in VS Code - lints a folder for broken, mis-cased or ambiguous links, orphans, duplicate basenames, missing index files and malformed frontmatter (scripts/vault_lint.py), writes the missing index (map of content) files, converts wikilinks to relative markdown links, sets a folder up as a vault (.obsidian/app.json with markdown links and ignored build folders, .gitignore lines), decides one vault versus several, and drives the official Obsidian CLI (search, read, links, backlinks, tags) when it is enabled. Use whenever the user mentions Obsidian, a vault, wikilinks, backlinks, graph view, a map of content, "link these notes together", "make an index for these docs", "orphan notes", "open this folder in Obsidian", "should this be one vault or two", or asks how AI-written markdown should be linked so people and agents can both navigate it; also when writing a new set of markdown files that a person will browse. Also for "refresh obsidian-notes" and "is obsidian-notes stale". Not for capturing session knowledge (everlast-capture), skill upkeep (evergreen-*), or codebase knowledge graphs (graphify).
---

# obsidian-notes

Make a folder of markdown a navigable graph: every document reachable from an index, every dependency an explicit link, links that resolve in Obsidian, on GitHub and in VS Code alike. The script does the deterministic part (find, fix, configure); you do the judgment (what should link to what, what an index says, whether a vault split is right).

Facts this skill relies on (2026-09-18): Obsidian ships an official CLI since 1.12.4 (February 2026; the help page asks for the 1.12.7 or newer installer, shown under Settings > General): `obsidian search|read|create|append|links|backlinks|tags|property:set`, enabled in Settings > General > Command line interface; it needs the app running and launches it otherwise. Obsidian treats `[[Note]]` and `[Note](Note.md)` as equivalent; the setting `Use [[Wikilinks]]` off plus "New link format: relative" makes it write portable links. GitHub still does not render wikilinks. kepano/obsidian-skills (the Obsidian CEO's skill set) exists and prefers wikilinks because it assumes a vault-only reader; this skill does not use it and takes the opposite rule, relative markdown links. Details and sources: [RESEARCH.md](RESEARCH.md), [references/setup.md](references/setup.md).

`VL` below means `python "<this folder>/scripts/vault_lint.py"` with an absolute path (`python3` on macOS and Linux; standard library only, Python 3.9 or newer).

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run `evergreen-refresh` on this folder in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh.

## Step 1: find the root and the reader

Decide which folder is the unit of navigation: the vault root if the user has one (a `.obsidian/` folder), otherwise the folder they named, otherwise the repo's docs root (`ai-docs/`, `docs/`, or the repo root). Ask yourself who reads it: only agents (an index per folder is enough), a person in Obsidian (links must resolve there), or GitHub too (relative markdown links only, no wikilinks). When in doubt assume all three; relative markdown links satisfy all three.

## Step 2: lint, then act on the report (the core action, leaves evidence)

Run `VL <root>` (add `--json` when the folder is large; `--exclude NAME ...` skips folder names at any depth, on top of the default skips: hidden folders, `node_modules`, `__pycache__`, `venv`, `.venv`, `Library`, `Temp`, `obj`, `Logs`, `Builds`, `bin`, `dist`, `build`). The report is the evidence: it must appear in the trace before you say anything about the state of the notes. Then:

- Broken markdown links: fix the target. The script reports a missing file, a literal space in the target (write `%20` or wrap the target in `<...>`), and a target whose case differs from the file on disk (resolves on Windows and macOS, a 404 on GitHub and Linux). A link to a folder resolves to that folder's index when it has one; a bare name resolves to `name.md`; reference-style definitions count.
- Broken or ambiguous wikilinks: rename to unique basenames or replace with a relative markdown link. `VL <root> --to-markdown-links` rewrites every wikilink that resolves to exactly one file (a folder-qualified name such as `[[notes/Beta]]` counts as resolved), encodes anchors, and leaves embeds, ambiguous and unresolved names, code blocks and frontmatter alone.
- Duplicate basenames: rename when both files are yours to rename. In a vault that spans two copies of one repo (a public clone and a private fork), do not rename; that vault must use markdown links, which are path-based and unaffected.
- Folders without an index: `VL <root> --fix-index` writes an `INDEX.md` that links each file by its H1 title and each child folder by its index, then links the new index from the nearest index above it (never a generated everlast `INDEX.md`, which is rebuilt from frontmatter). A folder counts as indexed when it holds `README.md`, `INDEX.md`, `_index.md`, `MOC.md` or `SKILL.md` (any case) or a file named after the folder, or when index files anywhere in the tree link every markdown file in it (the everlast root index does this for its subfolders). Never overwrite an existing index; edit it.
- Orphans: link each from the index or from the document it belongs to. Only an index at the root is exempt, so a subfolder's index must itself be linked. Ask whether an orphan is a draft to delete before linking it.
- Frontmatter errors: the check is a quick one (opened but never closed, tab-indented, a line without a key), not a YAML parser. Fix the YAML; Obsidian shows a file with invalid frontmatter as having no properties.
- Links outside the root: a warning; Obsidian cannot follow a link that leaves the vault.

Run `VL <root>` again; exit code 0 means no error-class findings (a root that does not exist is exit 2, not a clean run). Report the before and after counts.

## Step 3: write markdown that links (when creating or editing notes)

- One index per folder a reader might enter (`README.md` on GitHub-facing repos, `INDEX.md` in doc sets); it links every document in the folder by title and every subfolder by its index. The root index is the entry point, so every document is reachable in two hops.
- Every document links its index (a `Back to [index](README.md)` line, or the index name in the first lines) and ends with a `Related:` line linking the documents it builds on, contradicts or supersedes. Those are the edges Obsidian turns into backlinks and the graph.
- Relative markdown links, URL-encoded (`[Beta](notes/Beta%20two.md)`, `../decisions/2026-09-06-x.md`, `#heading` anchors). Wikilinks only inside a vault nobody reads on GitHub, and then with unique basenames.
- Frontmatter with `title`, `date`, `tags: [a, b]` (a YAML list) and `aliases` when a note has a second name; Obsidian reads these as properties, everlast generates its index from them, GitHub shows them as a table.
- Distinct basenames within the unit (a date prefix does it). Headings and callouts as GitHub renders them (`> [!NOTE]`); Obsidian adds folding on top.
- Do not write `.obsidian/workspace.json` or other per-machine state into a repo.

## Step 4: vault setup and the one-or-many question

`VL <root> --vault-init [--ignore Folder ...]` writes `.obsidian/app.json` (markdown links on, relative link format, links updated on rename, unsupported file types hidden, build folders such as `Library/`, `Temp/`, `obj/`, `node_modules/` ignored when they exist under the root, plus every `--ignore` name) and the `.gitignore` lines that keep `workspace.json` local. Then the user opens the folder with "Open folder as vault". For a Unity or other build-heavy repo, open the repo root with those ignores rather than a subfolder, so `ai-docs/` and `docs/` share one graph.

One vault or several: one vault per tree that links inside itself and not across. Separate vaults cost cross-links, one search, one graph, and duplicated plugin settings; they pay off when two trees never reference each other, sit on different drives, need different sync or privacy, or one is huge. A vault that spans a public clone and a private fork of the same repo works only with markdown links (duplicate basenames make wikilinks ambiguous). Say which pattern fits and why, then set it up.

## Step 5: the Obsidian CLI (optional)

`VL --probe` says whether `obsidian` is on PATH. When it is, prefer Obsidian's own resolver for questions about a live vault: `obsidian search query=<text> path=<folder>`, `obsidian read file=<name>`, `obsidian links file=<name>`, `obsidian backlinks file=<name> format=json`, `obsidian tags counts`, `obsidian append file=<name> content=<text>`. Prefix `vault=<name>` to target a vault. The CLI launches the app if it is closed; do not use it in a headless run (Obsidian Headless is a separate sync client, not a headless CLI). The Local REST API plugin's built-in MCP endpoint and the mcp-obsidian bridge are alternatives; they are only worth installing for a long-running agent inside Obsidian (see [references/setup.md](references/setup.md)).

## Output

The lint report (before and after), what was changed (files renamed, indexes written, links rewritten, config written), the vault recommendation in two sentences when asked, and the remaining warnings the user should decide on (orphans to delete or link, duplicates that cannot be renamed).

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered (a resolver rule Obsidian follows that the script does not, a setting name that changed), write it to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If a learning proves a claim above wrong, fix it here, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (topic: Obsidian-compatible markdown for AI agents: link forms that work in Obsidian, GitHub and VS Code, index and map-of-content practice, the Obsidian CLI and agent integrations, vault layout; tier `fast`; interval and next due in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (a lint is proven by a Bash call running `vault_lint.py` in the trace or a written `INDEX.md`, never by the reply; `scripts/test_vault_lint.py` is the script's own suite). Protocol: [MAINTENANCE.md](MAINTENANCE.md), a pointer to the installed evergreen plugin. Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
