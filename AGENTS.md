# Agent rules for obsidian-notes

Read [README.md](README.md) first. The skill is [skills/obsidian-notes/SKILL.md](skills/obsidian-notes/SKILL.md); its evidence, changes and lessons are the evergreen companions beside it (RESEARCH, CHANGELOG, LEARNINGS, TESTS, `evergreen.json`).

- Evergreen unit in pointer mode: before editing the skill read `skills/obsidian-notes/evergreen.json`; if `next_due` has passed or `contradiction` is set, say so and refresh after the task. Every edit to SKILL.md gets a CHANGELOG entry with its reason and a re-run of `evals/evals.json` (evergreen-test).
- `scripts/vault_lint.py` stays stdlib-only and cross-platform (pathlib, UTF-8, LF). Test it on the fixture under `skills/obsidian-notes/evals/fixtures/` before committing.
- Links in this repo are relative markdown links; no wikilinks; every folder of markdown has an index. The repo must pass its own lint: `python skills/obsidian-notes/scripts/vault_lint.py . --exclude fixtures` from the repo root reports no errors and no warnings (the fixture under `evals/fixtures/` is deliberately broken and is excluded). `python skills/obsidian-notes/scripts/test_vault_lint.py` must pass.
- No AI attribution in commits or files.

## everlast (session knowledge, load on demand)

- `ai-docs/INDEX.md` lists what past sessions learned here (solutions with verified commands, decisions with reasons, plans). At the start of a task, scan it and open only the entries whose title or tags match; read `ai-docs/HANDOFF.md` when continuing unfinished work (everlast-resume skill).
- Before finishing a task that hit a dead end, verified a non-obvious command, made a design choice, or taught you something about the user, record it (everlast-capture skill, or `everlast.py note` / `handoff`); rewrite `HANDOFF.md` when work is left unfinished. Say "nothing to record" when that is true.
- Anything naming a person, an internal host or name, a credential, or an opinion about people goes to the private sidecar (`--private`), never here. Lessons about the user or this machine go to the user tier (`--user`).
- Link documents together with relative markdown links: every markdown folder has an index that links its files, every entry links its index and the entries it builds on (a `Related:` line). No wikilinks in the repo.
