---
title: Two vaults: Ai directory and deckbuilder repo
kind: decision
status: active
date: 2026-09-18
verified: 2026-09-18
tags: [obsidian, vault, layout]
---

# Two vaults: Ai directory and deckbuilder repo

## Context
Obsidian 1.13.7 was installed on 2026-09-18 with no vaults. The user proposed one vault for a Unity game project and one for the Ai directory (the folder of AI-tooling repositories), and asked whether that pattern is right.

## Decision
Two Obsidian vaults for now: the Ai directory (the folder that holds the AI-tooling repositories, 632 markdown files) and a Unity game repository root (opened at the root with build folders ignored so `ai-docs/`, `docs/`, README and CODEMAP share one graph). A third vault only when a tree appears that links to neither.

## Reasons
A vault is a link namespace; the two trees never link to each other, live on different drives and would only pay the cost of a split (no cross-links, no single search) if they did. Opening the Unity repository at `ai-docs/` alone would cut it off from `docs/` and the README. Both configs were written with `vault_lint.py --vault-init` (markdown links, relative format, ignore lists, workspace.json gitignored) on 2026-09-18; the user still has to click "Open folder as vault" once per vault. The everlast vault (a separate private repository on the same machine) can be a third vault or be junctioned into the Ai vault later.

## Rejected
- One vault over the user's home folder or the projects parent: pulls in unrelated trees, and the game repository sits on another drive anyway.
- A vault per repository inside Ai: nine vaults with no cross-links, all plugin settings duplicated.

Related: [link form decision](2026-09-18-relative-markdown-links-and-an-index-per-folder-wikilinks-on.md), [setup reference](../../skills/obsidian-notes/references/setup.md).
