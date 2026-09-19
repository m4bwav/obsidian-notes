---
title: Relative markdown links and an index per folder, wikilinks only inside a vault
kind: decision
status: active
date: 2026-09-18
verified: 2026-09-18
tags: [obsidian, links, protocol]
---

# Relative markdown links and an index per folder, wikilinks only inside a vault

## Context
The user reads AI-written markdown in Obsidian (installed 2026-09-18, no vaults yet) and also on GitHub and in VS Code, and wants agents to write files that navigate as a graph in all three. kepano/obsidian-skills, the official-author skill set, tells agents to use wikilinks.

## Decision
Agent-written markdown uses relative markdown links, an index per folder and a `Related:` line per entry; wikilinks are the exception, allowed only inside a vault nobody reads on GitHub. Written into the Evergreen Protocol 1.8 (§9) and the Everlast Protocol 1.2 (§8 and the DOC-TYPES rules) on 2026-09-18, plugin versions 0.8.2 and 0.2.1, and into the `obsidian-notes` skill.

## Reasons
Obsidian resolves `[Note](path/Note.md)` and `[[Note]]` identically (obsidian.md/help/links) and offers a setting to write markdown links; GitHub, VS Code and most agents render only markdown links. Relative links are path-based, so a vault that holds two copies of one repository (public clone beside private fork; 54 duplicate basenames in the Ai directory) stays unambiguous.

## Rejected
- Wikilinks first (the obsidian-skills rule): assumes a vault-only reader; breaks on GitHub and with duplicate basenames.
- No rule, rely on the everlast INDEX alone: every entry was reachable but had no edges between entries, so Obsidian's graph showed a star, not a graph.

Related: [the research behind the skill](../../skills/obsidian-notes/RESEARCH.md), [vault layout decision](2026-09-18-two-vaults-ai-directory-and-deckbuilder-repo.md).
