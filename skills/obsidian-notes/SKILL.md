---
name: obsidian-notes
description: "Makes a folder of markdown work as an Obsidian vault that still renders on GitHub and in VS Code: lints for broken, mis-cased or ambiguous links, orphans, duplicate basenames, missing indexes and bad frontmatter (scripts/vault_lint.py), writes missing index (map of content) files, converts wikilinks to relative links, sets a folder up as a vault, decides one vault versus several, and drives the official Obsidian CLI. Use whenever the user mentions Obsidian, a vault, wikilinks, backlinks, graph view or a map of content, says \"link these notes together\", \"make an index for these docs\", \"orphan notes\", \"open this folder in Obsidian\" or \"should this be one vault or two\", or asks how AI-written markdown should be linked for people and agents; also when writing markdown files a person will browse. Also for \"refresh obsidian-notes\" and \"is obsidian-notes stale\". Not for capturing session knowledge (everlast-capture), skill upkeep (evergreen-*), or codebase knowledge graphs (graphify)."
---

# obsidian-notes

Make a folder of markdown a navigable graph: every document reachable from an index, every dependency an explicit link, links that resolve in Obsidian, on GitHub and in VS Code alike. The script does the deterministic part (find, fix, configure); you do the judgment (what should link to what, what an index says, whether a vault split is right).

Obsidian treats `[[Note]]` and `[Note](Note.md)` alike, and GitHub does not render wikilinks, so this skill writes relative markdown links (kepano/obsidian-skills prefers wikilinks for vault-only readers; this skill takes the opposite rule). Sources: [RESEARCH.md](RESEARCH.md); Obsidian settings, the CLI and agent integrations: [references/setup.md](references/setup.md).

`VL` below means `python "<this folder>/scripts/vault_lint.py"` with an absolute path: `python` on Windows (Git Bash and PowerShell alike; `python3` there is often a Store stub), `python3` on macOS and Linux. Standard library only, Python 3.9 or newer. `VL --help` holds the rules the script applies (how links resolve, what counts as an index, which folders it skips); read it only when a finding surprises you.

## Step 0: freshness (every use, one read)

Read `evergreen.json` next to this file. If `contradiction` is set or today is on or after `next_due`, tell the user in one line, do the task with the current content, then run `evergreen-refresh` on this folder in the same session. If `tests.failing` is non-empty, say so in one line and run `evergreen-tune` after the task. Never block the task on a refresh.

## Step 1: find the root and the reader

The unit of navigation is the vault root (a `.obsidian/` folder), else the folder the user named, else the repo's docs root. Unless the user says the notes are read only in Obsidian, assume GitHub and VS Code readers too: relative markdown links serve all three.

## Step 2: lint, then act on the report (the core action, leaves evidence)

Run `VL <root>` (`--exclude NAME ...` for more folders to skip). The text report gives every count and the first 15 items per list (`--max N`); prefer it to `--json`, which lists everything unless `--max` is given (586 KB on a 3,000-file tree). The report must appear in the trace before you say anything about the state of the notes. Then, per finding:

- Broken markdown link (missing file, a space in the target, a case that differs from the file on disk, which is a 404 on GitHub and Linux): fix the target when the right one is clear; otherwise leave the link and name it for the user. Never invent the missing file.
- Ambiguous or broken wikilink: `VL <root> --to-markdown-links` rewrites every wikilink that resolves to exactly one file and leaves ambiguous ones alone; name each ambiguous link and its candidates for the user instead of guessing, or qualify it (`[[notes/Beta]]`) only when the context makes the target certain.
- Duplicate basenames: rename when both files are yours; never in a vault spanning a public clone and a private fork (markdown links are path-based and unaffected).
- Folder without an index: `VL <root> --fix-index` writes `INDEX.md` linking each file by its H1 title with a purpose clause (frontmatter `description`, else the first sentence of prose) and links it from the nearest index above, so the new index is not itself an orphan. Rewrite a clause that does not say when to read the file. Never overwrite an existing index; edit it.
- Orphan: link it from its folder's index or the document it belongs to; say which orphans may be drafts to delete.
- Frontmatter error: fix the YAML (Obsidian shows invalid frontmatter as no properties). Link outside the root: a warning; Obsidian 1.14 opens single files from outside a vault, but following a vault link to one is undocumented.
- After notes were moved inside Obsidian, lint again: with relative paths Obsidian updates links to a moved note but not the links inside it (forum thread 4386, open since 2022).

The fix flags combine in one call (`VL <root> --fix-index --to-markdown-links`) and print the after-report themselves, so that is the after count; run `VL <root>` again only after hand edits. Exit 0 means no error-class findings (exit 1 is normal while a broken or ambiguous link is left for the user; exit 2: the root does not exist). Report the before and after counts.

## Step 3: write markdown that links (when creating or editing notes)

- One index per folder a reader might enter (`README.md` on GitHub-facing repos, `INDEX.md` in doc sets); it links every document in the folder by title and every subfolder by its index, one line each in the form `[title](path): when to read it` (a bare path is the one index shape agents measurably ignore or load whole). Keep an index under about 200 lines and read on demand; skip a folder index when the parent already lists every file in it. The root index is the entry point, so every document is reachable in two hops.
- Every document ends with a `Related:` line linking the documents it builds on, contradicts or supersedes; those edges carry meaning and Obsidian turns them into backlinks and the graph. A link back to the index is optional: the index-to-document edge is what Obsidian shows, so add at most one `Up:` line, and only for readers without a backlinks pane (GitHub).
- Relative markdown links, URL-encoded (`[Beta](notes/Beta%20two.md)`, `../decisions/2026-09-06-x.md`, `#heading` anchors). Wikilinks only inside a vault nobody reads on GitHub, and then with unique basenames.
- Frontmatter with `title`, `date`, `tags: [a, b]` (a YAML list) and `aliases` when a note has a second name; Obsidian reads these as properties, everlast generates its index from them, GitHub shows them as a table.
- Distinct basenames within the unit (a date prefix does it). Headings and callouts as GitHub renders them (`> [!NOTE]`); Obsidian adds folding on top.
- Do not write `.obsidian/workspace.json` or other per-machine state into a repo.

## Step 4: vault setup, one vault or several, the Obsidian CLI (only when asked)

- Setup: `VL <root> --vault-init [--ignore Folder ...]` writes `.obsidian/app.json` (markdown links, relative paths, build folders ignored) and the `.gitignore` lines that keep `workspace.json` local; then "Open folder as vault". For a build-heavy repo open the repo root with ignores, so `ai-docs/` and `docs/` share one graph.
- One vault or several: one vault per tree that links inside itself; split only for trees that never cross-link, need different sync or privacy, or are huge. Say which and why in two sentences; the reasoning is in [references/setup.md](references/setup.md).
- CLI: `VL --probe` says whether `obsidian` (or the Windows shim `Obsidian.com`) is reachable and which vaults exist. It drives a running app and launches it when closed, so never use it in a headless run; commands and integrations: [references/setup.md](references/setup.md).

## Output

The lint report (before and after), what was changed (files renamed, indexes written, links rewritten, config written), the vault recommendation in two sentences when asked, and the remaining warnings the user should decide on (orphans to delete or link, duplicates that cannot be renamed).

## While working: capture learnings

If the user corrects you, the same error happens twice, a workaround is found, or an environment fact is discovered (a resolver rule Obsidian follows that the script does not, a setting name that changed), write it to [LEARNINGS.md](LEARNINGS.md) now (check existing entries first). If a learning proves a claim above wrong, fix it here, log it in [CHANGELOG.md](CHANGELOG.md), and set `contradiction` in `evergreen.json`.

## Maintenance

This skill is evergreen (topic: Obsidian-compatible markdown for AI agents: link forms that work in Obsidian, GitHub and VS Code, index and map-of-content practice, the Obsidian CLI and agent integrations, vault layout; tier `fast`; interval and next due in `evergreen.json`). Files: `evergreen.json` (state), [RESEARCH.md](RESEARCH.md) (findings and search plan), [CHANGELOG.md](CHANGELOG.md) (every change, with reasons), [LEARNINGS.md](LEARNINGS.md) (lessons), [TESTS.md](TESTS.md) and `evals/evals.json` (a lint is proven by a Bash call running `vault_lint.py` in the trace or a written `INDEX.md`, never by the reply; `scripts/test_vault_lint.py` is the script's own suite). Protocol: [MAINTENANCE.md](MAINTENANCE.md), a pointer to the installed evergreen plugin. Refresh with `evergreen-refresh`; test with `evergreen-test`; fix a failure with `evergreen-tune`; audit with `evergreen-audit`.
